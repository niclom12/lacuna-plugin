#!/usr/bin/env python3
"""lacuna test suite: stdlib unittest, no network, no third-party packages.

    python3 test/run_tests.py

Groups:
  * memo fixtures driven through bin/lacuna_verify.run_verify with a fake `net`
  * the disarm paths a review found, each one asserted to block now
  * Bash, WebFetch, Write and Edit fixtures driven through the PreToolUse wall in bin/lacuna
  * the Stop gate and the profile gate, driven through bin/lacuna with real payloads
The bin/lacuna groups skip themselves, loudly, when bin/lacuna is not on disk yet.
"""
import importlib.machinery
import importlib.util
import inspect
import io
import json
import os
import hashlib
import re
import shlex
import shutil
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIX = os.path.join(HERE, "fixtures")
VERIFY_PATH = os.path.join(ROOT, "bin", "lacuna_verify.py")
LACUNA_PATH = os.path.join(ROOT, "bin", "lacuna")
TOKEN = re.compile(r"\{\{NOW(?:([+-])(\d+)([mhd]))?\}\}")
CONFIG = {"contact_email": "desk@example.com", "courtlistener_token": "tok-abc123",
          "venues": ["securities class actions"], "watch_tickers": ["ACME"],
          "restricted_tickers": [], "restricted_parties": [], "ca_bundle": None,
          "allowlist_extra": []}


def _import(path, name):
    """Import a file by path, including bin/lacuna, which carries no .py suffix."""
    loader = importlib.machinery.SourceFileLoader(name, path)
    spec = importlib.util.spec_from_loader(name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


verify = _import(VERIFY_PATH, "lacuna_verify")


def stamp(text, now):
    def one(m):
        if not m.group(1):
            d = now
        else:
            n, unit = int(m.group(2)), m.group(3)
            delta = timedelta(minutes=n) if unit == "m" else (
                timedelta(hours=n) if unit == "h" else timedelta(days=n))
            d = now + delta if m.group(1) == "+" else now - delta
        return d.strftime("%Y-%m-%dT%H:%M:%SZ")
    return TOKEN.sub(one, text)


def read(path):
    with io.open(path, encoding="utf-8") as fh:
        return fh.read()


def write(path, text):
    with io.open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


class FakeNet(object):
    """Stands in for bin/lacuna's HTTP legs. No sockets are opened anywhere."""

    DOCKETS = {"1:26-cv-04471": {"exists": True, "court": "S.D.N.Y.",
                                 "case_name": "Roe v. Acme Robotics, Inc.",
                                 "assigned_to": "Chen",
                                 "parties": ["Roe", "Acme Robotics, Inc."]}}
    CITES = {"402 F.4th 1188": {"status": 404, "case_name": None}}

    def __init__(self, fail=(), dockets=None, cites=None):
        self.fail = set(fail)
        self.dockets = dict(self.DOCKETS if dockets is None else dockets)
        self.cites = dict(self.CITES if cites is None else cites)
        self.cite_calls, self.docket_calls = [], []

    def cite_lookup(self, text_blob):
        self.cite_calls.append(text_blob)
        if "cite" in self.fail:
            return None
        return [dict(citation=c, status=v["status"], case_name=v["case_name"])
                for c, v in self.cites.items() if c in text_blob]

    def docket_lookup(self, docket_number, court_hint=None):
        self.docket_calls.append((docket_number, court_hint))
        if "docket" in self.fail:
            return None
        return self.dockets.get(docket_number, {"exists": False, "court": "", "case_name": "",
                                                "assigned_to": None, "parties": []})


class Harness(object):
    """Fixture plumbing shared by the memo group and the policy group."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="lacuna-test-")
        self.now = datetime.now(timezone.utc).replace(microsecond=0)
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def case(self, memo, ledger="base"):
        state = os.path.join(self.tmp, ".lacuna")
        if not os.path.isdir(state):
            shutil.copytree(os.path.join(FIX, "ledgers", ledger), state)
            path = os.path.join(state, "ledger.jsonl")
            write(path, stamp(read(path), self.now))
        memo_path = os.path.join(self.tmp, "memo.md")
        write(memo_path, stamp(read(os.path.join(FIX, "memos", memo)), self.now))
        return memo_path, state

    def run_one(self, memo, ledger="base", blocking=True, net=None, config=None, edit=None):
        memo_path, state = self.case(memo, ledger)
        if edit is not None:
            write(memo_path, edit(read(memo_path)))
        res = verify.run_verify(memo_path, state, config or CONFIG, net or FakeNet(), blocking)
        res["path"], res["state"] = memo_path, state
        return res

    def blocks(self, res):
        return [f for f in res["findings"] if f["severity"] == "block"]

    def assertBlocked(self, res, check_id, needle):
        self.assertEqual(res["exit_code"], 2, "expected a blocking exit code, got %r for %s"
                         % (res["exit_code"], [f["message"] for f in res["findings"]]))
        hits = [f for f in self.blocks(res) if f["check_id"] == check_id]
        self.assertTrue(hits, "%s raised no blocking finding; got %s"
                        % (check_id, [(f["check_id"], f["message"]) for f in res["findings"]]))
        joined = " || ".join(f["message"] + " " + f["remedy"] for f in hits)
        self.assertIn(needle, joined)

    def assertClean(self, res):
        self.assertEqual(res["exit_code"], 0, [f["message"] for f in self.blocks(res)])
        self.assertEqual(self.blocks(res), [], [f["message"] for f in self.blocks(res)])


class MemoCase(Harness, unittest.TestCase):
    """Every memo fixture asserts an exact exit code and a finding substring."""

    # 1
    def test_01_clean_memo_passes(self):
        res = self.run_one("01-clean.md")
        self.assertClean(res)
        self.assertEqual(res["infra_failures"], [])

    # 2
    def test_02_entity_curly_and_wrapped_quote_passes(self):
        res = self.run_one("02-quote-normalisation.md")
        self.assertClean(res)

    # 3
    def test_03_fabricated_quote_blocks_with_the_span_echoed(self):
        res = self.run_one("03-fabricated-quote.md")
        self.assertBlocked(res, "C6", "quoted run not found")
        self.assertIn("The company admitted the internal review",
                      " ".join(f["message"] for f in self.blocks(res)))

    # 4
    def test_04_deleting_the_quote_blocks_again(self):
        first = self.run_one("03-fabricated-quote.md")
        self.assertEqual(first["exit_code"], 2)
        write(first["path"], stamp(read(os.path.join(FIX, "memos", "04-quote-deleted.md")),
                                   self.now))
        res = verify.run_verify(first["path"], first["state"], CONFIG, FakeNet(), True)
        self.assertEqual(res["exit_code"], 2)
        hits = [f for f in res["findings"] if f["check_id"] == "C6" and f["severity"] == "block"]
        self.assertTrue(hits)
        self.assertIn("deleted rather than sourced", " ".join(f["message"] for f in hits))

    # 5
    def test_05_fabricated_holding_blocks_on_attribution(self):
        res = self.run_one("05-fabricated-holding.md")
        self.assertBlocked(res, "C6", "attribution with no ledgered accession")

    # 6
    def test_06_unverified_citation_as_a_premise_blocks(self):
        net = FakeNet()
        res = self.run_one("06-unverified-premise.md", net=net)
        self.assertBlocked(res, "C3", "used as a premise")
        self.assertTrue(net.cite_calls, "the citation blob was never submitted")

    # 7
    def test_07_stale_docket_blocks_with_a_refetch_remedy(self):
        res = self.run_one("07-stale-source.md", ledger="stale")
        self.assertBlocked(res, "C2", "refetch")
        self.assertIn("stale source", " ".join(f["message"] for f in self.blocks(res)))

    # 8
    def test_08_hallucinated_docket_blocks(self):
        res = self.run_one("08-hallucinated-docket.md")
        self.assertBlocked(res, "C4", "1:26-cv-99999 does not exist")

    # 9
    def test_09_wrong_court_parenthetical_blocks(self):
        res = self.run_one("09-wrong-court.md")
        self.assertBlocked(res, "C4", "resolves to court S.D.N.Y.")

    # 10
    def test_10_constructed_sec_archive_url_passes(self):
        res = self.run_one("10-constructed-sec-url.md")
        self.assertClean(res)

    # 11
    def test_11_unsourced_base_rate_blocks(self):
        res = self.run_one("11-unsourced-base-rate.md")
        self.assertBlocked(res, "C7", "reference class has no ledgered source")

    # 12
    def test_12_verbal_probability_blocks(self):
        res = self.run_one("12-verbal-probability.md")
        self.assertBlocked(res, "C7", "three in four")

    # 13
    def test_13_nonpublic_material_in_the_thesis_blocks(self):
        res = self.run_one("13-nonpublic-in-thesis.md")
        self.assertBlocked(res, "C8", "repeated in ## Thesis")

    # 15
    def test_15_an_estimate_split_across_two_lines_still_blocks(self):
        """The estimate and the outcome verb sit on separate list items, so wrapped-line
        merging never joins them. C7 reads the whole paragraph block instead."""
        res = self.run_one("15-cross-line-estimate.md")
        self.assertBlocked(res, "C7", "75%")
        self.assertIn("is missing", " ".join(f["message"] for f in self.blocks(res)))

    # 16
    def test_16_negative_retrieval_about_an_unresolved_case_blocks_in_verified_facts(self):
        """Reproduces the live eval-1 memo, which recorded 'a CourtListener opinion search for
        "Karlsson Meridian Bioscience securities" returned 0 results' under ## Verified facts.
        A search outcome is not a verified fact, and naming the unresolved case there reads to
        a skimming reader as a case this desk checked."""
        res = self.run_one("16-negative-retrieval-in-verified.md", ledger="karlsson")
        self.assertBlocked(res, "C3", "move search-outcome records to ## What was searched")
        joined = " ".join(f["message"] + " " + f["remedy"] for f in self.blocks(res)
                          if f["check_id"] == "C3")
        self.assertIn("Karlsson", joined)
        self.assertIn("## Verified facts", joined)
        self.assertIn("## Rejected and unverified claims", joined)

    # 14
    def test_14_third_fire_writes_the_failure_banner_and_stops_blocking(self):
        memo_path, state = self.case("14-third-fire.md")
        for attempt in (1, 2):
            res = verify.run_verify(memo_path, state, CONFIG, FakeNet(), True)
            self.assertEqual(res["exit_code"], 2, "attempt %d should still block" % attempt)
        third = verify.run_verify(memo_path, state, CONFIG, FakeNet(), True)
        self.assertEqual(third["exit_code"], 0)
        body = read(memo_path)
        self.assertIn("VERIFICATION FAILED, DO NOT RELY ON THIS MEMO", body)
        self.assertIn("## Verification failures", body)
        fourth = verify.run_verify(memo_path, state, CONFIG, FakeNet(), True)
        self.assertEqual(fourth["exit_code"], 0, "the banner must not start a new block cycle")


def after(heading, block):
    """Return an edit callable that inserts `block` immediately under `heading`."""
    return lambda t: t.replace(heading + "\n", heading + "\n" + block + "\n", 1)


class GuardrailCase(Harness, unittest.TestCase):
    """The disarm paths a review found in the first build. Each one passed before the fix."""

    def test_a_repeated_heading_does_not_hide_its_body_from_the_checks(self):
        res = self.run_one("01-clean.md", edit=lambda t: t + (
            "\n## Speculation\n"
            "We put the probability the case survives the motion to dismiss at 80%.\n"))
        self.assertBlocked(res, "C1", "duplicate section heading")
        self.assertTrue([f for f in self.blocks(res) if f["check_id"] == "C7"],
                        "the duplicated block must still be reachable by the other checks")

    def test_a_public_docket_permalink_satisfies_the_provenance_check(self):
        """Memos cite https://www.courtlistener.com/docket/<id>/<slug>/ because a reader without a
        CourtListener token gets 401 from the v4 API URL. C5 has to read the docket id out of that
        path, or the readable form would be the one the checker rejects."""
        res = self.run_one("01-clean.md", edit=after(
            "## Inference", "Counsel of record was read from the docket sheet. [CourtListener] "
            "https://www.courtlistener.com/docket/70000001/roe-v-acme-robotics-inc/"))
        self.assertEqual([f["message"] for f in self.blocks(res) if f["check_id"] == "C5"], [])
        self.assertClean(res)

    def test_a_pruned_cache_blocks_rather_than_silently_disarming_the_quote_check(self):
        memo_path, state = self.case("03-fabricated-quote.md")
        shutil.rmtree(os.path.join(state, "cache"))
        res = verify.run_verify(memo_path, state, CONFIG, FakeNet(), True)
        res["path"], res["state"] = memo_path, state
        self.assertBlocked(res, "C6", "no longer readable")
        self.assertTrue(res["infra_failures"])

    def test_a_cache_body_far_down_the_ledger_is_still_indexed(self):
        pad = "\n".join(json.dumps({"ts": stamp("{{NOW-1h}}", self.now), "case_id": "acme-sec-2026",
                                    "tool": "news", "argv": ["news", "pad"], "url": "https://x/%d" % i,
                                    "sha256": "missing%d" % i, "identifiers": []})
                        for i in range(80))
        memo_path, state = self.case("03-fabricated-quote.md")
        path = os.path.join(state, "ledger.jsonl")
        write(path, pad + "\n" + read(path))
        res = verify.run_verify(memo_path, state, CONFIG, FakeNet(), True)
        self.assertEqual(res["exit_code"], 2)
        self.assertIn("quoted run not found", " ".join(f["message"] for f in res["findings"]))

    def test_an_untagged_quote_in_verified_facts_blocks(self):
        res = self.run_one("01-clean.md", edit=after("## Verified facts", '- The filing said "the '
                                                     'internal review found no evidence of wrongdoing '
                                                     'and is now closed".'))
        self.assertBlocked(res, "C6", "untagged quoted run in ## Verified facts")

    def test_a_blockquote_is_checked_like_any_other_quote(self):
        res = self.run_one("01-clean.md", edit=after(
            "## Counter-evidence",
            "> the internal review has been closed with no findings adverse to the company "
            "[SEC EDGAR]"))
        self.assertIn("quoted run not found",
                      " ".join(f["message"] for f in res["findings"] if f["check_id"] == "C6"))

    def test_a_case_name_with_no_reporter_citation_still_blocks(self):
        res = self.run_one("01-clean.md", edit=after(
            "## Inference", "Under Karlsson v. Meridian Biosciences (3d Cir. 2024), the controlling "
            "scienter standard governs this complaint."))
        self.assertBlocked(res, "C3", "Karlsson v. Meridian")

    def test_a_retrieved_docket_caption_is_not_treated_as_a_bare_case_name(self):
        self.assertClean(self.run_one("01-clean.md"))

    def test_the_word_ambiguous_elsewhere_does_not_disarm_the_ambiguity_label(self):
        net = FakeNet(cites={"402 F.4th 1188": {"status": 300, "case_name": "two candidates"}})
        res = self.run_one("06-unverified-premise.md", net=net,
                           edit=after("## Coverage limits", "Nothing here is ambiguous."))
        self.assertBlocked(res, "C3", "is ambiguous and is not labelled so")

    def test_a_judge_surname_is_not_blocked_when_the_docket_leg_is_down(self):
        res = self.run_one("01-clean.md", net=FakeNet(fail=("docket",)), edit=after(
            "## Situation", "Judge Chen has not yet set a briefing schedule."))
        self.assertFalse([f for f in self.blocks(res) if f["check_id"] == "C4"])
        self.assertTrue(res["infra_failures"])

    def test_a_judge_surname_still_blocks_when_the_docket_leg_is_up(self):
        res = self.run_one("01-clean.md", edit=after(
            "## Situation", "Judge Marsden has not yet set a briefing schedule."))
        self.assertBlocked(res, "C4", "Marsden")

    def test_an_unreadable_ledger_is_infrastructure_rather_than_a_block(self):
        memo_path, state = self.case("01-clean.md")
        os.remove(os.path.join(state, "ledger.jsonl"))
        res = verify.run_verify(memo_path, state, CONFIG, FakeNet(), True)
        self.assertFalse([f for f in res["findings"]
                          if f["check_id"] == "C2" and f["severity"] == "block"])
        self.assertTrue(res["infra_failures"])

    def test_an_unknown_attribution_stamp_is_refused_and_a_version_stamp_is_not(self):
        stamp_it = lambda v: (lambda t: t.replace("generated_by: lacuna@a1b2c3d",
                                                  "generated_by: lacuna@" + v, 1))
        self.assertBlocked(self.run_one("01-clean.md", edit=stamp_it("unknown")),
                           "C1", "lacuna@unknown")
        self.assertClean(self.run_one("01-clean.md", edit=stamp_it("v0.1.0")))

    def test_a_symlinked_root_shares_the_attempt_cap_rather_than_resetting_it(self):
        memo_path, state = self.case("03-fabricated-quote.md")
        os.symlink(self.tmp, os.path.join(self.tmp, "linked"))
        via_link = os.path.join(self.tmp, "linked", "memo.md")
        codes = [verify.run_verify(p, state, CONFIG, FakeNet(), True)["exit_code"]
                 for p in (memo_path, via_link, via_link)]
        self.assertEqual(codes, [2, 2, 0], "the link must not hand the memo a fresh attempt count")
        store = json.loads(read(os.path.join(state, "verified.json")))
        self.assertEqual(list(store), [os.path.realpath(memo_path)])

    def test_a_price_figure_with_no_ledgered_price_retrieval_blocks(self):
        res = self.run_one("01-clean.md", edit=after(
            "## Price evidence", "return_0d 0.4%, return_1d 0.1%, return_5d 0.9%."))
        self.assertBlocked(res, "C9", "no ledgered price retrieval")

    def test_the_searched_block_survives_the_quoting_the_generator_emits(self):
        block = "\n".join("- %s | %s | `%s` | results: 1 | %s"
                          % ("2026-01-01T00:00:00Z", r["tool"],
                             " ".join(shlex.quote(x) for x in r["argv"]), r["url"])
                          for r in [json.loads(l) for l in
                                    read(os.path.join(FIX, "ledgers", "base", "ledger.jsonl")).splitlines()
                                    if l.strip()])
        res = self.run_one("01-clean.md", edit=lambda t: re.sub(
            r"(?s)(## What was searched\n).*?(\n\n## Action items)", r"\1" + block + r"\2", t))
        self.assertFalse([f for f in self.blocks(res) if f["check_id"] == "C10"],
                         [f["message"] for f in self.blocks(res)])


class PolicyCase(Harness, unittest.TestCase):
    """The blocking policy itself: infrastructure, budget, sentinel, --explain."""

    def test_infrastructure_failure_never_blocks(self):
        res = self.run_one("06-unverified-premise.md", net=FakeNet(fail=("cite", "docket")))
        self.assertEqual(res["exit_code"], 0)
        self.assertTrue(res["infra_failures"])
        self.assertFalse([f for f in self.blocks(res) if f["check_id"] in ("C3", "C4")])

    def test_explain_mode_never_blocks_and_leaves_state_untouched(self):
        res = self.run_one("03-fabricated-quote.md", blocking=False)
        self.assertEqual(res["exit_code"], 0)
        self.assertTrue(self.blocks(res))
        self.assertFalse(os.path.exists(os.path.join(res["state"], "verified.json")))

    def test_sentinel_is_cleared_on_completion(self):
        res = self.run_one("01-clean.md")
        self.assertFalse(os.path.exists(os.path.join(res["state"], "last-verify.json")))

    def test_verified_json_records_the_hash_and_resets_attempts_on_a_pass(self):
        res = self.run_one("01-clean.md")
        store = json.loads(read(os.path.join(res["state"], "verified.json")))
        rec = store[res["path"]]
        self.assertEqual(rec["attempts"], 0)
        self.assertEqual(len(rec["sha256"]), 64)
        self.assertIn("checked_at", rec)

    def test_budget_overrun_is_infrastructure_rather_than_a_block(self):
        saved = verify.BUDGET_SECONDS
        verify.BUDGET_SECONDS = -1.0
        try:
            res = self.run_one("03-fabricated-quote.md")
        finally:
            verify.BUDGET_SECONDS = saved
        self.assertEqual(res["exit_code"], 0)
        self.assertIn("budget", " ".join(res["infra_failures"]))

    def test_restricted_name_blocks_and_is_appended_to_the_hit_log(self):
        cfg = dict(CONFIG, restricted_tickers=["acme"])
        res = self.run_one("01-clean.md", config=cfg)
        self.assertBlocked(res, "C8", "restricted name, escalate to compliance")
        self.assertTrue(os.path.exists(os.path.join(res["state"], "restricted-hits.jsonl")))

    def test_missing_courtlistener_token_inserts_the_off_banner(self):
        cfg = dict(CONFIG, courtlistener_token=None)
        res = self.run_one("01-clean.md", config=cfg)
        self.assertIn("Case-law verification: OFF", read(res["path"]))

    def test_run_verify_signature_matches_the_pinned_contract(self):
        names = list(inspect.signature(verify.run_verify).parameters)
        self.assertEqual(names, ["memo_path", "state_dir", "config", "net", "blocking"])


def _load_lacuna():
    if not os.path.exists(LACUNA_PATH):
        return None, "bin/lacuna is not on disk yet"
    try:
        return _import(LACUNA_PATH, "lacuna_cli"), None
    except Exception as exc:                                    # pragma: no cover
        return None, "bin/lacuna could not be imported: %s: %s" % (type(exc).__name__, exc)


def _deny_fn(mod):
    """Find the PreToolUse decision in bin/lacuna without pinning a single name."""
    for name in ("hook_pre_tool", "pre_tool_decision", "pre_tool", "deny_decision",
                 "decide_pre_tool", "pre_tool_deny", "evaluate_pre_tool"):
        fn = getattr(mod, name, None)
        if callable(fn):
            return fn, name
    for name in sorted(dir(mod)):
        fn = getattr(mod, name)
        if callable(fn) and not name.startswith("__") and (
                "deny" in name.lower() or "pre_tool" in name.lower()):
            return fn, name
    return None, None


def _envelope(text):
    try:
        env = json.loads(text)
    except ValueError:
        return None
    if not isinstance(env, dict):
        return None
    return env.get("hookSpecificOutput") if "hookSpecificOutput" in env else env


def _decide(fn, payload):
    """Normalise however bin/lacuna signals a denial into (denied, reason, envelope).

    The pinned contract is: print the envelope on stdout and exit 0. Older or simpler
    shapes (a returned dict, a reason string, a bool, a pair) are accepted too so the
    suite fails on policy rather than on style.
    """
    errors = []
    for args in ((payload,), (payload.get("tool_name"), payload.get("tool_input", {}))):
        buf, saved = io.StringIO(), sys.stdout
        sys.stdout = buf
        try:
            out = fn(*args)
        except SystemExit:
            out = None
        except TypeError as exc:
            sys.stdout = saved
            errors.append("%s%r: %s" % (getattr(fn, "__name__", "fn"), args, exc))
            if "argument" not in str(exc):
                raise
            continue
        finally:
            sys.stdout = saved
        printed = buf.getvalue().strip()
        if printed:
            block = _envelope(printed)
            if block is not None:
                return (str(block.get("permissionDecision", "")).lower() == "deny",
                        block.get("permissionDecisionReason", ""), block)
        if out is None or out is False or out == 0:
            return False, "", None
        if out is True:
            return True, "", None
        if isinstance(out, str):
            return bool(out.strip()), out, None
        if isinstance(out, dict):
            block = _envelope(json.dumps(out)) or {}
            return (str(block.get("permissionDecision", "")).lower() == "deny",
                    block.get("permissionDecisionReason", ""), block)
        if isinstance(out, (tuple, list)) and out:
            return bool(out[0]), (out[1] if len(out) > 1 else ""), None
        raise AssertionError("unrecognised return shape from %r: %r" % (fn, out))
    raise AssertionError("the pre-tool function rejected every call shape tried: %s"
                         % "; ".join(errors))


class CommandCase(unittest.TestCase):
    """Twenty command fixtures against the PreToolUse wall in bin/lacuna."""

    @classmethod
    def setUpClass(cls):
        cls.mod, cls.why = _load_lacuna()
        fn, cls.fn_name = (_deny_fn(cls.mod) if cls.mod else (None, None))
        cls.deny_fn = (fn,)   # tucked in a tuple so it is not bound as a method
        cls.allow = json.loads(read(os.path.join(FIX, "commands", "must-allow.json")))
        cls.deny = json.loads(read(os.path.join(FIX, "commands", "must-deny.json")))

    def setUp(self):
        if self.mod is None:
            self.skipTest("%s, so the command wall cannot be exercised yet" % self.why)
        if self.deny_fn[0] is None:
            self.skipTest("bin/lacuna exposes no pre-tool function this suite can find")
        self.tmp = tempfile.mkdtemp(prefix="lacuna-cmd-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        os.makedirs(os.path.join(self.tmp, ".lacuna"))
        write(os.path.join(self.tmp, ".lacuna", "bin-path"), LACUNA_PATH + "\n")
        data = os.path.join(self.tmp, "plugin-data")
        os.makedirs(data)
        write(os.path.join(data, "config.json"), json.dumps(CONFIG))
        self.saved_env = os.environ.get("CLAUDE_PLUGIN_DATA")
        os.environ["CLAUDE_PLUGIN_DATA"] = data
        self.addCleanup(self._restore_env)
        if hasattr(self.mod, "config"):
            self.mod.config(reload=True)
        self.cwd = os.getcwd()
        os.chdir(self.tmp)
        self.addCleanup(os.chdir, self.cwd)

    def _restore_env(self):
        if self.saved_env is None:
            os.environ.pop("CLAUDE_PLUGIN_DATA", None)
        else:
            os.environ["CLAUDE_PLUGIN_DATA"] = self.saved_env
        if hasattr(self.mod, "config"):
            self.mod.config(reload=True)

    def payload(self, fx):
        raw = json.dumps(fx["tool_input"]).replace("{{LACUNA}}", LACUNA_PATH)
        return {"session_id": "test", "transcript_path": "/dev/null", "cwd": self.tmp,
                "hook_event_name": "PreToolUse", "tool_name": fx["tool_name"],
                "tool_input": json.loads(raw)}

    def test_legitimate_commands_are_allowed(self):
        self.assertGreaterEqual(len(self.allow), 10)
        for fx in self.allow:
            denied, reason, _ = _decide(self.deny_fn[0], self.payload(fx))
            self.assertFalse(denied, "wrongly denied (%s): %s -> %s"
                             % (fx["why"], fx["tool_input"], reason))

    def test_egress_order_and_state_tampering_commands_are_denied(self):
        self.assertGreaterEqual(len(self.deny), 10)
        for fx in self.deny:
            denied, reason, _ = _decide(self.deny_fn[0], self.payload(fx))
            self.assertTrue(denied, "wrongly allowed (%s): %s" % (fx["why"], fx["tool_input"]))
            self.assertTrue(str(reason).strip(), "a denial must carry a one sentence reason")

    def test_the_deny_envelope_matches_the_pinned_shape(self):
        denied, reason, block = _decide(self.deny_fn[0], self.payload(self.deny[0]))
        self.assertTrue(denied)
        if block is None:
            self.skipTest("bin/lacuna signals denial without emitting the envelope from this entry")
        self.assertEqual(block["hookEventName"], "PreToolUse")
        self.assertEqual(block["permissionDecision"], "deny")
        self.assertTrue(block["permissionDecisionReason"].strip())
        self.assertEqual(sorted(block), ["hookEventName", "permissionDecision",
                                         "permissionDecisionReason"])

    def test_every_denial_is_appended_to_the_denials_log(self):
        _decide(self.deny_fn[0], self.payload(self.deny[0]))
        log = os.path.join(self.tmp, ".lacuna", "denials.jsonl")
        if not os.path.exists(log):
            self.skipTest("bin/lacuna does not write denials.jsonl from this entry point")
        rows = [json.loads(l) for l in read(log).splitlines() if l.strip()]
        self.assertTrue(rows)


class StopHookCase(Harness, unittest.TestCase):
    """The Stop gate itself, driven with real payloads. No sockets: Net is swapped out."""

    def setUp(self):
        Harness.setUp(self)
        self.mod, why = _load_lacuna()
        if self.mod is None:
            self.skipTest(why)
        state = os.path.join(self.tmp, ".lacuna")
        shutil.copytree(os.path.join(FIX, "ledgers", "base"), state)
        path = os.path.join(state, "ledger.jsonl")
        write(path, stamp(read(path), self.now))
        os.makedirs(os.path.join(self.tmp, "cases", "acme-sec-2026"))
        self.memo = os.path.join(self.tmp, "cases", "acme-sec-2026", "memo.md")
        self.put(self.memo, "03-fabricated-quote.md")
        data = os.path.join(self.tmp, "plugin-data")
        os.makedirs(data)
        write(os.path.join(data, "config.json"), json.dumps(CONFIG))
        self.saved_env = os.environ.get("CLAUDE_PLUGIN_DATA")
        os.environ["CLAUDE_PLUGIN_DATA"] = data
        self.mod.config(reload=True)
        self.saved_net, self.mod.Net = self.mod.Net, lambda *a, **k: FakeNet()
        self.cwd = os.getcwd()
        os.chdir(self.tmp)
        self.addCleanup(self._restore)

    def _restore(self):
        os.chdir(self.cwd)
        self.mod.Net = self.saved_net
        if self.saved_env is None:
            os.environ.pop("CLAUDE_PLUGIN_DATA", None)
        else:
            os.environ["CLAUDE_PLUGIN_DATA"] = self.saved_env
        self.mod.config(reload=True)

    def put(self, path, fixture):
        write(path, stamp(read(os.path.join(FIX, "memos", fixture)), self.now))

    def stop(self, **extra):
        payload = {"cwd": self.tmp, "hook_event_name": "Stop"}
        payload.update(extra)
        err, sys.stderr = sys.stderr, io.StringIO()
        try:
            return self.mod.hook_stop(payload)
        finally:
            sys.stderr = err

    def test_an_untouched_failing_memo_keeps_blocking_until_the_banner_lands(self):
        self.assertEqual(self.stop(), 2)
        self.assertEqual(self.stop(), 2, "an unchanged failing memo must re-enter the suite")
        self.assertEqual(self.stop(), 0, "the third fire converts the block into a banner")
        self.assertIn("VERIFICATION FAILED, DO NOT RELY ON THIS MEMO", read(self.memo))
        self.assertIn("## Verification failures", read(self.memo))

    def test_a_clean_memo_is_skipped_on_the_second_stop(self):
        self.put(self.memo, "01-clean.md")
        self.assertEqual(self.stop(), 0)
        self.assertEqual(self.stop(), 0)

    def test_stop_hook_active_does_not_switch_the_gate_off(self):
        self.assertEqual(self.stop(stop_hook_active=True), 2)

    def test_a_memo_written_outside_cases_is_still_scanned(self):
        os.remove(self.memo)
        os.makedirs(os.path.join(self.tmp, "research"))
        self.put(os.path.join(self.tmp, "research", "memo.md"), "03-fabricated-quote.md")
        self.assertEqual(self.stop(), 2)

    def test_a_memo_reached_through_a_symlinked_directory_is_still_scanned(self):
        os.remove(self.memo)
        outside = os.path.join(self.tmp, "elsewhere")
        os.makedirs(outside)
        self.put(os.path.join(outside, "memo.md"), "03-fabricated-quote.md")
        os.symlink(outside, os.path.join(self.tmp, "cases", "linked"))
        self.assertEqual(self.stop(), 2)

    def test_only_the_desk_profile_is_skipped_not_every_file_named_profile(self):
        os.remove(self.memo)
        self.put(os.path.join(self.tmp, "cases", "acme-sec-2026", "profile.md"),
                 "03-fabricated-quote.md")
        self.assertEqual(self.stop(), 2, "cases/<id>/profile.md is not the desk profile")
        self.put(os.path.join(self.tmp, "cases", "profile.md"), "03-fabricated-quote.md")
        os.remove(os.path.join(self.tmp, "cases", "acme-sec-2026", "profile.md"))
        self.assertEqual(self.stop(), 0, "the desk profile is not a memo")

    def test_a_forged_pass_record_keyed_by_basename_does_not_clear_a_memo(self):
        write(os.path.join(self.tmp, ".lacuna", "verified.json"), json.dumps(
            {"memo.md": {"sha256": hashlib.sha256(
                read(self.memo).encode("utf-8")).hexdigest(), "attempts": 0}}))
        self.assertEqual(self.stop(), 2)


class ProfileGateCase(unittest.TestCase):
    """The shipped desk profile must not brick the desk it configures."""

    def setUp(self):
        self.mod, why = _load_lacuna()
        if self.mod is None:
            self.skipTest(why)
        self.tmp = tempfile.mkdtemp(prefix="lacuna-profile-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        os.makedirs(os.path.join(self.tmp, "cases"))
        self.path = os.path.join(self.tmp, "cases", "profile.md")

    def test_the_shipped_template_reads_as_unfilled(self):
        write(self.path, read(os.path.join(ROOT, "templates", "profile.md")))
        self.assertTrue(self.mod.profile_unfilled(self.tmp))

    def test_a_filled_template_does_not_trip_on_its_own_prose(self):
        text = read(os.path.join(ROOT, "templates", "profile.md"))
        text = re.sub(r"(?m)^([ \t]*(?:[-*][ \t]+)?[^:\n]*:[ \t]*)\[PLACEHOLDER\][ \t]*$",
                      r"\1filled in", text)
        text = re.sub(r"(?m)^([ \t]*[-*][ \t]*)\[PLACEHOLDER\][ \t]*$", r"\1none", text)
        write(self.path, text)
        self.assertFalse(self.mod.profile_unfilled(self.tmp),
                         "a correctly filled profile still reads as unfilled: %s" % text)
        self.mod.require_profile(self.tmp)


if __name__ == "__main__":
    unittest.main(verbosity=2, buffer=False)
