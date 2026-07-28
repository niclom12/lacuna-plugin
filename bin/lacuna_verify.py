"""lacuna_verify: the ten deterministic memo checks. Python 3 stdlib only.
Imported by bin/lacuna via importlib. One public entry point, its signature pinned:
    run_verify(memo_path, state_dir, config, net, blocking) -> dict
`net` is injected by the caller and exposes cite_lookup(text_blob) and docket_lookup(number,
court_hint). Either may return None, meaning infrastructure failure, which never blocks."""
import hashlib, html, json, os, re, time, unicodedata
from datetime import datetime, timezone

BUDGET_SECONDS, MAX_BLOCKING_ATTEMPTS = 90.0, 2
BANNER = "VERIFICATION FAILED, DO NOT RELY ON THIS MEMO"
CAVEAT_HEAD, CAVEAT_TAIL = "Citations resolve to real cases:", "NOT CHECKED: whether each case"
FOOTER = "Internal research only. Not legal advice. Not investment advice. Not a"
REJECTED, NO_BASE = "## Rejected and unverified claims", "[no empirical base rate, judgment only]"
SECTIONS = ("Situation|Thesis|Verified facts|Inference|Speculation|Rejected and unverified claims|"
            "Catalyst calendar|Price evidence|Counter-evidence|Falsification conditions|Provenance|"
            "What was searched|Action items|Coverage limits").split("|")
GUARDED = ["Thesis", "Verified facts", "Catalyst calendar", "Price evidence"]
FM_KEYS = ("case_id subject tickers status distribution contains_nonpublic generated_by model "
           "operator").split()
ALLOW_HOSTS = ("sec.gov data.sec.gov efts.sec.gov courtlistener.com gdeltproject.org "
               "api.gdeltproject.org").split()
FRESH_HOURS = [("court", 24), ("price", 24), ("edgar", 168), ("news", 720)]
CONF_LINES = ("Reference class:", "Decision point:", "What would change my mind:")
WORDNUM = "one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve"
WORDVAL = dict((w, i + 1) for i, w in enumerate(WORDNUM.split("|")))
_REP = (r"U\.S\.|S\. ?Ct\.|L\. ?Ed\. ?2d|F\.(?:2d|3d|4th)|F\. ?Supp\.(?: ?[23]d)?|A\.[23]d|"
        r"P\.[23]d|N\.E\.[23]d|N\.W\.[23]d|S\.E\.[23]d|S\.W\.[23]d|So\. ?[23]d|B\.R\.")
RE_CITE = re.compile(r"\b(?:\d{1,4})\s+(?:" + _REP + r")\s+(?:\d{1,5})\b")
_P = r"[A-Z][A-Za-z&.'-]+(?: [A-Z][A-Za-z&.'-]+){0,3}"
RE_CASE = re.compile(_P + r"\s+v\.?\s+" + _P)
RE_DOCKET, RE_ACC = re.compile(r"\b\d:\d{2}-[a-z]{2}-\d{4,6}\b"), re.compile(r"\b\d{10}-\d{2}-\d{6}\b")
RE_URL, RE_LEAD = re.compile(r"https?://[^\s<>\"'\)\]]+"), re.compile(r"^\s*(-|\*|#|\||>|\d+\.)\s")
RE_TAG = re.compile(r"\[(?:CourtListener|SEC EDGAR|GDELT|market data|web, verify|"
                    r"model knowledge, UNVERIFIED|user provided)\]")
RE_QUOTE = re.compile(u"\u201c([^\u201d]{12,600})\u201d|\"([^\"]{12,600})\"")
RE_BQ = re.compile(r"^\s*>\s*(.+?)\s*$", re.M)
RE_PREMISE = re.compile(r"\b(controlling|governs|holds|held|requires|standard|under|applying|"
                        r"establishes)\b", re.I)
RE_ATTRIB = re.compile(r"\b(said|stated|disclosed|held|holds|alleges|alleged|requires|ordered|"
                       r"ruled|concluded|announced|reported|admitted)\b", re.I)
RE_SRC = re.compile(r"\b(8-K|10-K|10-Q|13D|13G|court|complaint|order|filing|opinion|judge|SEC|"
                    r"the company)\b", re.I)
RE_OUT = re.compile(r"\b(surviv\w*|prevail\w*|settl\w*|grant\w*|den(?:y|ies|ied)|affirm\w*|"
                    r"dismiss\w*)\b", re.I)
RE_EST = re.compile(r"(\d{1,3}(?:\.\d+)?\s?%)|(\b0\.\d+\b)|(\b(?:\d{1,2}|" + WORDNUM +
                    r")\s+(?:in|out of)\s+(?:\d{1,2}|" + WORDNUM + r")\b)|"
                    r"(\bmore likely than not\b)|(\bcoin flip\b)|(\bnear certain\w*\b)", re.I)
RE_COURT = re.compile(r"\b(?:[NSEWMD]\.? ?D\.? ?[A-Z]|Cir\.|Ch\.|Bankr\.|Court|Chancery)")
RE_TIME = re.compile(r"\d{1,2}:\d{2}\s*(?:[A-Z]{2,4}|[+-]\d{2}:?\d{2})")
RE_ENTRY, RE_JUDGE = re.compile(u"entry:\\s*[\"\u201c]"), re.compile(r"\bJudge\s+([A-Z][a-z]{2,20})\b")
RE_RET = re.compile(r"\breturn_\d|[-+]?\d+(?:\.\d+)?\s?%")
def _now(): return datetime.now(timezone.utc)
def _iso(dt): return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
def _toks(s): return re.findall(r"[a-z0-9']+", _norm(s))
def _clean(url): return url.rstrip(".,);\"'")
def _unq(s): return _norm(s).replace('"', "").replace("'", "")
def _qhash(q): return hashlib.sha256(" ".join(_toks(q)).encode("utf-8")).hexdigest()[:16]
def _grams(t, n=6): return set(tuple(t[i:i + n]) for i in range(max(0, len(t) - n + 1)))
def _ts(s):
    try: d = datetime.fromisoformat(str(s).strip().replace("Z", "+00:00"))
    except (ValueError, AttributeError): return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
def _load(path, default):
    try:
        with open(path, encoding="utf-8") as fh: return json.load(fh)
    except (OSError, ValueError): return default
def _save(path, obj, mode="w"):
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, mode, encoding="utf-8") as fh:
            fh.write(json.dumps(obj, sort_keys=True) + ("\n" if mode == "a" else ""))
    except OSError: pass
def _norm(s):
    s = unicodedata.normalize("NFKC", html.unescape(s)).replace(u"\u00ad", "")
    s = re.sub(u"[\u2018\u2019\u201a\u201b\u2032]", "'", re.sub(r"<[^>]+>", " ", s))
    s = re.sub(u"[\u2010-\u2015\u2212]", "-", re.sub(u"[\u201c\u201d\u201e\u2033]", '"', s))
    return re.sub(r"\s+", " ", s).strip().lower()
def _allowed(url):
    m = re.match(r"https?://([^/:]+)", url)
    h = re.sub(r"^www\.", "", (m.group(1).lower() if m else ""))
    return any(h == d or h.endswith("." + d) for d in ALLOW_HOSTS)

def _quotes(text):
    """Straight quotes, curly quotes and markdown blockquotes, 6+ tokens."""
    for m in RE_QUOTE.finditer(text):
        q = m.group(1) or m.group(2) or ""
        if len(_toks(q)) >= 6: yield q
    for m in RE_BQ.finditer(text):
        q = re.sub(RE_TAG, "", m.group(1)).strip()
        if len(_toks(q)) >= 6 and not RE_QUOTE.search(m.group(1)): yield q
def _overlap(quote, bodies):
    """Best normalised token-window overlap of `quote` against any cached body."""
    q, best = _toks(quote), 0.0
    for toks, idx in bodies:
        starts = set(idx.get(q[0], []))
        starts.update(p - 1 for p in idx.get(q[1], []) if p >= 1)
        for s in sorted(starts)[:400]:
            w = toks[s:s + len(q)]
            if w: best = max(best, sum(1 for a, b in zip(q, w) if a == b) / float(len(q)))
            if best >= 0.95: return best
    return best
def _value(s):
    s = s.strip().lower()
    m = re.match(r"^(\d{1,3}(?:\.\d+)?)\s?%$", s)
    if m: return float(m.group(1)) / 100.0
    if re.match(r"^0\.\d+$", s): return float(s)
    try:
        m = re.match(r"^(\S+)\s+(?:in|out of)\s+(\S+)$", s)
        a, b = WORDVAL.get(m.group(1)) or int(m.group(1)), WORDVAL.get(m.group(2)) or int(m.group(2))
        return a / float(b) if b else None
    except (AttributeError, TypeError, ValueError): return None

class Ctx(object):
    """Memo, ledger and cache parsed once, plus the finding sink."""

    def __init__(self, path, raw, state_dir, config, net):
        self.path, self.raw, self.state, self.cfg = path, raw, state_dir, config or {}
        self.net, self.infra, self.findings, self.lines = net, [], [], raw.split("\n")
        self.inserts, self.appends, self.pending_quotes = [], [], []
        self.fm, self.fm_line, self.fm_end, self._bodies = {}, {}, 0, None
        if self.lines and self.lines[0].strip() == "---":
            for i, ln in enumerate(self.lines[1:], start=1):
                if ln.strip() == "---": self.fm_end = i; break
                m = re.match(r"^([a-z_]+):\s*(.*)$", ln)
                if m: self.fm[m.group(1)], self.fm_line[m.group(1)] = m.group(2).strip(), i
        self.spans, cur, start = {}, None, 0
        for i, ln in enumerate(self.lines):
            m = re.match(r"^##\s+(.+?)\s*$", ln)
            if not m: continue
            if cur: self.spans.setdefault(cur, []).append((start, i))
            cur, start = m.group(1), i + 1
        if cur: self.spans.setdefault(cur, []).append((start, len(self.lines)))
        self.sec = dict((k, v[0]) for k, v in self.spans.items())
        self.dupes = sorted(k for k, v in self.spans.items() if len(v) > 1)
        self.ledger_ok = True
        self.ledger = self._ledger()   # sets ledger_ok False when the file cannot be read
        self.urls = set(e["url"] for e in self.ledger if e.get("url"))
        self.ids = set(str(i).lower() for e in self.ledger for i in (e.get("identifiers") or []))

    def add(self, cid, sev, line, msg, fix):
        self.findings.append(dict(check_id=cid, severity=sev, line=int(line), message=msg, remedy=fix))
    def bad(self, cid, line, msg, fix): self.add(cid, "block", line, msg, fix)
    def note(self, cid, line, msg, fix): self.add(cid, "advisory", line, msg, fix)
    def inspan(self, name, i0): return any(a <= i0 < b for a, b in self.spans.get(name, ()))
    def text(self, name):
        return "\n".join("\n".join(self.lines[a:b]) for a, b in self.spans.get(name, ()))

    def _ledger(self):
        case, rows = self.fm.get("case_id", ""), []
        try:
            with open(os.path.join(self.state, "ledger.jsonl"), encoding="utf-8") as fh: raw = fh.read()
        except OSError:
            self.ledger_ok = False; return rows
        for ln in raw.splitlines():
            try: r = json.loads(ln) if ln.strip() else None
            except ValueError: r = None
            if r and (not case or r.get("case_id") == case): rows.append(r)
        return rows

    def logical(self, name=None):
        """(1-based line, text) pairs, every occurrence of the section, wrapped lines merged."""
        out = []
        for a, b in ([(0, len(self.lines))] if name is None else self.spans.get(name, ())):
            for i in range(a, min(b, len(self.lines))):
                ln = self.lines[i]
                if (out and ln.strip() and out[-1][1].strip() and not ln.startswith("---")
                        and not RE_LEAD.match(ln)): out[-1] = (out[-1][0], out[-1][1] + " " + ln.strip())
                else: out.append((i + 1, ln))
        return [(n, t) for n, t in out if t.strip()]

    def cited(self):
        low = self.raw.lower()
        hit = [e for e in self.ledger if (e.get("url") and e["url"] in self.raw)
               or any(str(i).lower() in low for i in (e.get("identifiers") or []))]
        return hit or self.ledger
    def paragraphs(self):
        out, n = [], 1
        for chunk in re.split(r"\n[ \t]*\n", self.raw):
            out.append((chunk.replace("\n", " "), n))
            n += chunk.count("\n") + 2
        return out
    def bodies(self):
        """Up to 60 readable cached bodies for this case, newest first. Position in the
        ledger never disqualifies a body: only unreadability does."""
        if self._bodies is None:
            self._bodies, seen = [], set()
            for e in reversed(self.ledger):
                d = e.get("sha256")
                if not d or d in seen: continue
                seen.add(d)
                try:
                    with open(os.path.join(self.state, "cache", d + ".txt"), encoding="utf-8") as fh:
                        toks, idx = _toks(fh.read()), {}
                except (OSError, UnicodeDecodeError): continue
                for p, tok in enumerate(toks): idx.setdefault(tok, []).append(p)
                self._bodies.append((toks, idx))
                if len(self._bodies) >= 60: break
        return self._bodies
def c1_structure(x):
    if not x.fm: return x.bad("C1", 1, "no frontmatter block", "run lacuna template memo")
    for k in FM_KEYS:
        if not x.fm.get(k): x.bad("C1", 1, "frontmatter key missing: %s" % k, "add it")
    if x.fm.get("distribution") and not x.fm["distribution"].startswith("internal-only"):
        x.bad("C1", x.fm_line.get("distribution", 1), "distribution must be internal-only",
              "set distribution: internal-only")
    if x.fm.get("generated_by") and not x.fm["generated_by"].startswith("lacuna@"):
        x.bad("C1", x.fm_line.get("generated_by", 1), "generated_by must be lacuna@<git-sha>",
              "run lacuna check for the sha")
    for d in x.dupes:
        x.bad("C1", x.spans[d][1][0], "duplicate section heading ## %s: a repeated heading hides "
              "its body from the section-scoped checks" % d, "merge the two blocks")
    seen = -1
    for name in SECTIONS:
        if name not in x.sec:
            x.bad("C1", 1, "required section missing: ## %s" % name, "run lacuna template memo")
            continue
        if x.sec[name][0] < seen:
            x.bad("C1", x.sec[name][0], "section out of order: ## %s" % name, "restore the order")
        seen = x.sec[name][0]
    if CAVEAT_HEAD not in x.raw or CAVEAT_TAIL not in x.raw:
        x.inserts.append((x.fm_end + 1, [CAVEAT_HEAD + " unknown. " + CAVEAT_TAIL + " supports the "
                          "point it is cited for,", "and whether it is still good law. A lawyer "
                          "must read every cited case.", ""]))
        x.note("C1", x.fm_end + 1, "citation caveat was missing and was inserted", "leave it")
    if FOOTER not in x.raw:
        x.appends.append("\n\n---\n" + FOOTER + "\nrecommendation to buy or sell any security. "
                         "Do not distribute or forward.\n")
        x.note("C1", len(x.lines), "footer legend was missing and was appended", "leave it")
    if not x.cfg.get("courtlistener_token") and "Case-law verification: OFF" not in x.raw:
        x.inserts.append((x.fm_end + 1, ["Case-law verification: OFF (no CourtListener token)"]))
        x.note("C1", x.fm_end + 1, "Case-law verification: OFF banner inserted", "run /lacuna:setup")
def c2_freshness(x):
    rows = [e for e in x.cited() if _ts(e.get("ts"))]
    if not rows and not x.ledger_ok:
        return x.infra.append("the retrieval ledger is unreadable, so freshness went unchecked")
    if not rows: return x.bad("C2", 1, "no ledger entries back this memo", "run the data commands")
    stamps = sorted(_ts(e["ts"]) for e in rows)
    for label, dt in (("As of", stamps[-1]), ("Oldest source used", stamps[0])):
        pat = re.compile(r"^" + re.escape(label) + r":\s*(.*)$")
        idx = next((i for i, ln in enumerate(x.lines) if pat.match(ln)), None)
        if idx is None:
            x.inserts.append((x.fm_end + 1, ["%s: %s" % (label, _iso(dt))]))
            x.bad("C2", x.fm_end + 1, "%s: line missing" % label, "the verifier writes it"); continue
        got = _ts(pat.match(x.lines[idx]).group(1))
        x.lines[idx] = "%s: %s" % (label, _iso(dt))
        if got is None or abs((got - dt).total_seconds()) > 60:
            x.bad("C2", idx + 1, "%s: disagreed with the ledger by over 60 seconds" % label,
                  "the verifier rewrote it from the ledger")
    now = _now()
    for e in rows:
        tool = (e.get("tool") or "").lower()
        budget = next((h for p, h in FRESH_HOURS if tool.startswith(p)), 720)
        age = (now - _ts(e["ts"])).total_seconds() / 3600.0
        if age > budget:
            x.bad("C2", 1, "stale source: %s fetched %.0f hours ago, budget %d hours"
                  % (tool or "source", age, budget), "refetch %s" % (e.get("url") or tool))
def c3_citations(x):
    cpath = os.path.join(x.state, "cite-cache.json")
    cites = sorted(set(m.group(0) for m in RE_CITE.finditer(x.raw)))
    rej = lambda i0: x.inspan("Rejected and unverified claims", i0)
    cache, blind = _load(cpath, {}), False
    if [c for c in cites if c not in cache]:
        res = x.net.cite_lookup(x.raw) if x.net else None
        if res is None:
            # No token is a known-off state the banner announces, and still blocks unbacked case
            # references. A reachability failure is infrastructure and blocks nothing.
            blind = bool(x.cfg.get("courtlistener_token"))
            x.infra.append("citation lookup unavailable, %d citations unchecked" % len(cites))
        else:
            for it in res:
                cache[str(it.get("citation"))] = {"status": it.get("status"),
                                                  "case_name": it.get("case_name")}
            _save(cpath, cache)
    for cite in cites:
        line = next((i + 1 for i, ln in enumerate(x.lines) if cite in ln), 1)
        st = (cache.get(cite) or {}).get("status")
        what = {404: "not found in the case-law database", 400: "a malformed reporter"}.get(st)
        if what and rej(line - 1): x.note("C3", line, "citation %s is %s" % (cite, what), "leave it")
        elif what:
            x.bad("C3", line, "citation %s is %s and sits outside %s" % (cite, what, REJECTED),
                  "move it to " + REJECTED + " or delete it")
        elif st == 300 and "ambiguous" not in x.lines[line - 1].lower():
            x.bad("C3", line, "citation %s is ambiguous and is not labelled so" % cite,
                  "label it ambiguous and name the candidates")
    ok = set(str((cache.get(c) or {}).get("case_name") or "").lower() for c in cites
             if (cache.get(c) or {}).get("status") == 200)
    for line, text in ([] if blind else x.logical()):
        if rej(line - 1) or x.inspan("Provenance", line - 1): continue
        for m in RE_CASE.finditer(text):
            name, ids = m.group(0), [i.lower() for i in RE_ACC.findall(text) + RE_DOCKET.findall(text)]
            if any(i in x.ids for i in ids) or any(u in text for u in x.urls): continue
            if _norm(name) in " ".join(ok): continue
            x.bad("C3", line, "case reference %r outside %s is backed by no retrieval: no ledgered "
                  "docket, accession or URL on its line, and no citation on it resolved"
                  % (name, REJECTED), "move it to " + REJECTED + ", or cite what you retrieved")
    bad = set(c for c in cites if (cache.get(c) or {}).get("status") in (400, 404))
    for para, first in x.paragraphs():
        if rej(first - 1): continue
        if ("[UNVERIFIED]" in para or any(c in para for c in bad)) and RE_PREMISE.search(para):
            x.bad("C3", first, "an unverified citation is used as a premise: %s"
                  % re.sub(r"\s+", " ", para)[:100], "delete it or cite verified authority")
def c4_dockets(x):
    subject, judges, blind = _norm(x.fm.get("subject", "")), set(), False
    for num in sorted(set(RE_DOCKET.findall(x.raw))):
        pos = x.raw.find(num)
        line, window = x.raw[:pos].count("\n") + 1, x.raw[max(0, pos - 200):pos + 200]
        pm = re.search(r"\(([^)]{2,40})\)", window)
        hint = pm.group(1).strip() if pm else None
        rec = x.net.docket_lookup(num, hint) if x.net else None
        if rec is None:
            x.infra.append("docket lookup unavailable for %s" % num); blind = True; continue
        if not rec.get("exists"):
            x.bad("C4", line, "docket %s does not exist in the federal docket database" % num,
                  "remove it, or run court docket for the real number")
            continue
        court, cap = rec.get("court") or "", rec.get("case_name") or ""
        if hint and _norm(hint) != _norm(court):
            x.bad("C4", line, "docket %s resolves to court %s, the memo says (%s)" % (num, court,
                  hint), "correct the parenthetical to %s" % court)
        if cap and _norm(cap) not in _norm(window):
            x.bad("C4", line, "docket %s caption %s is absent near the number" % (num, cap),
                  "state the resolved caption beside the number")
        parties = _norm(" | ".join(rec.get("parties") or []))
        if subject and parties and subject not in parties:
            x.bad("C4", line, "docket %s parties exclude the memo subject %s" % (num,
                  x.fm.get("subject", "")), "confirm the docket concerns the subject")
        if rec.get("assigned_to"): judges.add(_norm(rec["assigned_to"]).split()[-1])
    if blind:
        return x.infra.append("a docket lookup failed, so judge surnames were not checked")
    for m in RE_JUDGE.finditer(x.raw):
        if _norm(m.group(1)) not in judges:
            x.bad("C4", x.raw[:m.start()].count("\n") + 1, "judge %s matches assigned_to on no "
                  "resolved docket" % m.group(1), "remove the name or resolve the docket")
def c5_urls(x):
    stripped = set(s.lstrip("0") for s in x.ids)
    for m in RE_URL.finditer(x.raw):
        url, line = _clean(m.group(0)), x.raw[:m.start()].count("\n") + 1
        row = x.lines[line - 1] if line - 1 < len(x.lines) else ""
        if url in x.urls: continue
        ids = [i.lower() for i in RE_ACC.findall(url) + RE_DOCKET.findall(url)]
        ids += re.findall(r"/data/(\d{4,10})/", url) + re.findall(r"CIK(\d{10})", url)
        if _allowed(url):
            if not any(i.lower() in x.ids or i.lstrip("0") in stripped for i in ids):
                x.bad("C5", line, "allowlisted URL %s carries no ledgered identifier" % url,
                      "fetch it with lacuna so it is ledgered")
            continue
        if x.inspan("Verified facts", line - 1):
            x.bad("C5", line, "untrusted-host URL %s appears in ## Verified facts" % url,
                  "move it out and tag it [web, verify]")
        elif "[web, verify]" not in row:
            x.bad("C5", line, "untrusted-host URL %s is not tagged [web, verify]" % url,
                  "tag the line [web, verify] or remove the URL")
    for m in RE_ACC.finditer(x.raw):
        if m.group(0).lower() not in x.ids:
            x.bad("C5", x.raw[:m.start()].count("\n") + 1, "accession %s was never retrieved by this "
                  "desk" % m.group(0), "run lacuna edgar doc %s" % m.group(0))
def c6_quotes(x):
    bodies = x.bodies()
    prev = _load(os.path.join(x.state, "verified.json"), {}).get(x.path) or {}
    pending, present, matched, failed = set(prev.get("pending_quotes") or []), set(), set(), set()
    for name in x.sec:
        for line, text in x.logical(name):
            for q in _quotes(text):
                h = _qhash(q)
                present.add(h)
                if not RE_TAG.search(text):
                    if name == "Verified facts":
                        x.bad("C6", line, "untagged quoted run in ## Verified facts, so it cannot "
                              "be checked: \"%s\"" % q[:70], "tag the line with its source, or move "
                              "the claim out of ## Verified facts")
                    continue
                if not bodies:
                    x.infra.append("no readable cached body backs ## %s" % name)
                    x.add("C6", "block" if name == "Verified facts" else "advisory", line,
                          "the retrieved body behind this quote is no longer readable, so it was "
                          "not machine-checked: \"%s\"" % q[:70], "refetch the source with lacuna")
                    continue
                score = _overlap(q, bodies)
                if score >= 0.95: matched.add(h); continue
                failed.add(h)
                x.add("C6", "block" if name == "Verified facts" else "advisory", line,
                      "quoted run not found in any retrieved source (%.0f%% token overlap): \"%s\""
                      % (score * 100, q[:70]), "quote the retrieved text exactly")
    for line, text in x.logical("Verified facts"):
        if not (RE_ATTRIB.search(text) and RE_SRC.search(text)): continue
        ids = [i.lower() for i in RE_ACC.findall(text) + RE_DOCKET.findall(text)]
        if not any(i in x.ids for i in ids) and not any(u in text for u in x.urls):
            x.bad("C6", line, "attribution with no ledgered accession, docket or URL on the line: "
                  "%s" % re.sub(r"\s+", " ", text)[:80], "add the accession behind it")
    for _ in sorted(pending - present - matched):
        x.bad("C6", 1, "a quote that failed verification was deleted rather than sourced",
              "restore it with its retrieved source, or state the claim unquoted and cite it")
    x.pending_quotes = sorted((pending | failed) - matched)
def c7_confidence(x):
    for name in x.sec:
        for line, text in x.logical(name):
            if re.match(r"^\s*-?\s*Reference class:", text): continue
            for em in RE_EST.finditer(text):
                gaps = [text[min(em.end(), c.end()):max(em.start(), c.start())]
                        for c in RE_OUT.finditer(text)]
                if not any(len(g.split()) <= 15 for g in gaps): continue
                tail, est = "\n".join(x.lines[line:line + 8]), em.group(0).strip()
                miss = [l for l in CONF_LINES if l not in tail]
                if miss: x.bad("C7", line, "estimate \"%s\" is missing: %s" % (est, ", ".join(miss)),
                               "add the missing lines under the estimate")
                rc = next((l for l in tail.split("\n") if "Reference class:" in l), "")
                if rc and NO_BASE not in rc and not (RE_TAG.search(rc)
                                                     and any(u in rc for u in x.urls)):
                    x.bad("C7", line, "reference class has no ledgered source and is not labelled "
                          "%s" % NO_BASE, "cite a retrieved base rate or label it")
                v = _value(est)
                if v is not None and not 0.15 <= v <= 0.85 and "deterministic" not in tail.lower():
                    x.bad("C7", line, "extreme estimate %s names no deterministic event" % est,
                          "name the event that justifies the extreme")
def c8_provenance(x):
    restricted = [str(t).lower() for t in (x.cfg.get("restricted_tickers") or [])]
    tickers = [t.strip().lower() for t in
               re.sub(r"[\[\]]", " ", x.fm.get("tickers", "")).split(",") if t.strip()]
    hits = [t for t in tickers if t in restricted]
    hits += [str(p).lower() for p in (x.cfg.get("restricted_parties") or [])
             if str(p).lower() and str(p).lower() in _norm(x.fm.get("subject", ""))]
    for h in hits:
        _save(os.path.join(x.state, "restricted-hits.jsonl"),
              {"ts": _iso(_now()), "memo": x.path, "name": h}, "a")
        x.bad("C8", x.fm_line.get("subject", 1), "restricted name, escalate to compliance: %s" % h,
              "stop work on this name")
    tainted = []
    for line, text in x.logical("Provenance"):
        if not text.strip().startswith("-"): continue
        cls = next((k.rstrip(":") for k in ("public:", "nonpublic", "unknown") if k in text), None)
        um = RE_URL.search(text)
        if cls is None:
            x.bad("C8", line, "provenance item is not classified public, nonpublic or unknown",
                  "classify it public:<ledgered url>, nonpublic or unknown")
        elif cls == "public":
            if not um or _clean(um.group(0)) not in x.urls:
                x.bad("C8", line, "provenance item claims public: with an unretrieved URL",
                      "fetch the URL with lacuna, or classify it unknown")
        else:
            tainted.append((line, text))
            if cls == "nonpublic" and x.fm.get("contains_nonpublic", "").lower() != "true":
                x.bad("C8", x.fm_line.get("contains_nonpublic", line), "a nonpublic provenance "
                      "item is present but contains_nonpublic is false", "set it true")
    if (x.fm.get("contains_nonpublic", "").lower() == "true"
            and "do not act" not in x.fm.get("distribution", "")):
        x.bad("C8", x.fm_line.get("distribution", 1), "contains_nonpublic: true requires "
              "distribution: internal-only, do not act", "set distribution: internal-only, do not act")
    guard = {}
    for name in GUARDED:
        for gl, text in x.logical(name): guard[gl] = (name, _grams(_toks(text)))
    for line, text in tainted:
        for q in list(_quotes(text)) or [text]:
            want = _grams(_toks(q))
            for gl in sorted(guard):
                if not (want & guard[gl][1]): continue
                x.bad("C8", gl, "nonpublic or unknown material from ## Provenance (line %d) is "
                      "repeated in ## %s" % (line, guard[gl][0]), "remove it or source it")
                break
def c9_catalysts(x):
    for line, text in x.logical("Catalyst calendar"):
        if not text.strip().startswith("-") or "scheduled" not in text: continue
        miss = [lbl for lbl, ok in (("a time with a time zone", RE_TIME.search(text)),
                                    ("a source link", RE_URL.search(text)),
                                    ("a quoted docket entry", RE_ENTRY.search(text)),
                                    ("a court", RE_COURT.search(text))) if not ok]
        if miss:
            x.bad("C9", line, "scheduled catalyst is missing %s" % ", ".join(miss),
                  "quote the docket entry that sets the date, or relabel it expected")
    if any((e.get("tool") or "").startswith("price") for e in x.ledger): return
    for line, text in x.logical("Price evidence"):
        if RE_RET.search(text):
            x.bad("C9", line, "price figure with no ledgered price retrieval: %s"
                  % re.sub(r"\s+", " ", text)[:80], "write \"price data unavailable\"")
def c10_searched(x):
    if "What was searched" not in x.sec:
        return x.bad("C10", 1, "## What was searched is missing", "run lacuna searched")
    # Both sides are stripped of quotes: `searched` prints shlex-quoted argv, the ledger stores
    # the raw list, and a naive comparison makes every multi-word query an unfixable block.
    line, body = x.sec["What was searched"][0], _unq(x.text("What was searched"))
    if not body: return x.bad("C10", line, "## What was searched is empty", "run lacuna searched")
    for e in x.ledger:
        argv = " ".join(str(a) for a in (e.get("argv") or []))
        if argv and _unq(argv) not in body:
            x.bad("C10", line, "## What was searched omits a ledgered search: %s" % argv,
                  "regenerate the block with lacuna searched")
CHECKS = (c1_structure, c2_freshness, c3_citations, c4_dockets, c5_urls, c6_quotes,
          c7_confidence, c8_provenance, c9_catalysts, c10_searched)
def _write(x, text):
    try:
        with open(x.path, "w", encoding="utf-8") as fh: fh.write(text)
    except OSError as exc:
        x.infra.append("could not rewrite the memo: %s" % exc)
        return x.raw
    return text


def _flush(x):
    lines = list(x.lines)
    for at, block in sorted(x.inserts, key=lambda p: -p[0]): lines[at:at] = block
    text = "\n".join(lines) + "".join(x.appends)
    return _write(x, text) if text != x.raw else text
def _write_failure(x, text, blocks):
    lines, at = text.split("\n"), (x.fm_end + 1 if x.fm_end else 0)
    lines[at:at] = [BANNER, "", "## Verification failures", ""] + [
        "- %s (%s, line %d). Fix: %s" % (f["message"], f["check_id"], f["line"], f["remedy"])
        for f in blocks] + [""]
    return _write(x, "\n".join(lines))
def _clear(sentinel):
    try: os.remove(sentinel)
    except OSError: pass
def run_verify(memo_path, state_dir, config, net, blocking):
    """Run the ten checks over one memo. Content blocks; infrastructure never does."""
    t0, sentinel = time.time(), os.path.join(state_dir, "last-verify.json")
    _save(sentinel, {"path": memo_path, "started": _iso(_now())})
    try:
        with open(memo_path, encoding="utf-8") as fh: raw = fh.read()
    except OSError as exc:
        _clear(sentinel)
        return {"findings": [], "exit_code": 0,
                "infra_failures": ["cannot read %s: %s" % (memo_path, exc)]}
    x = Ctx(memo_path, raw, state_dir, config, net)
    for fn in CHECKS:
        if time.time() - t0 > BUDGET_SECONDS:
            x.infra.append("90 second budget exceeded, later checks were skipped")
            break
        try: fn(x)
        except Exception as exc:
            x.infra.append("%s raised %s: %s" % (fn.__name__, type(exc).__name__, exc))
    blocks, result = ([f for f in x.findings if f["severity"] == "block"],
                      {"findings": x.findings, "infra_failures": x.infra, "exit_code": 0})
    if not blocking:
        _clear(sentinel); return result
    text, vpath = _flush(x), os.path.join(state_dir, "verified.json")
    store = _load(vpath, {})
    if not isinstance(store, dict): store = {}
    prev = store.get(memo_path) or {}

    sig = hashlib.sha256("|".join(sorted(f["check_id"] + ":" + f["message"]
                                         for f in blocks)).encode("utf-8")).hexdigest()[:16]
    attempts = (prev.get("attempts", 0) + 1) if prev.get("sig") == sig else 1
    if blocks and attempts > MAX_BLOCKING_ATTEMPTS:
        if prev.get("attempts", 0) <= MAX_BLOCKING_ATTEMPTS: text = _write_failure(x, text, blocks)
    elif blocks: result["exit_code"] = 2
    store[memo_path] = {"sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                        "checked_at": _iso(_now()), "sig": sig if blocks else None,
                        "attempts": attempts if blocks else 0,
                        "pending_quotes": x.pending_quotes, "last_findings": x.findings}
    _save(vpath, store)
    _clear(sentinel)
    return result
