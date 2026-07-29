# Changelog

All notable changes to the `lacuna` plugin are recorded here. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this
project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The first line under each version heading is a one-sentence summary. The
SessionStart hook reads that line and shows it once when the installed version
changes, so keep it short and keep it plain.

## [Unreleased]

### Fixed

- The session banner's case-law line, docket court parsing, search outcomes in verified facts, and the promised wall clock, from the first live-eval pass.
- The SessionStart banner read settings from `$CLAUDE_PLUGIN_DATA`, which Claude Code exports to hooks but not to Bash tool calls, so it announced `Case-law verification: OFF` while `lacuna check` in the same session read the real token and said ON. Settings now resolve to one path per machine, `~/.config/lacuna/config.json`, whatever launched the process.
- `court docket <id>` printed `court: ?format=json`. The court field is a hyperlink and the API propagates the format suffix onto it, so the id is now read from the URL path rather than by splitting on the last slash.
- Check C3 blocks an unresolved case name anywhere in `## Thesis`, `## Verified facts` or `## Inference`, in any phrasing. A negative-retrieval sentence such as "a search for X returned 0 results" used to pass, and it reads to a skimming reader as a case this desk confirmed.
- Check C5 reads a docket id out of the public permalink path, so a memo can cite the reader-facing `courtlistener.com/docket/<id>/<slug>/` form and still provenance.
- Version reporting, memo attribution, path keying, the confidence check and the eval scorer, from the first review pass.
- `bin/lacuna` reported `1.0.0` while every manifest said `0.1.0`. Both now read `0.1.0`, in the session banner and in the SEC User-Agent.
- An install with no git checkout stamped `generated_by: lacuna@unknown`. It now stamps `lacuna@v<release>`, and check C1 refuses `lacuna@unknown` outright while accepting a git sha or a versioned stamp.
- `verified.json` and the pending-quote state are keyed on the memo's real path, so reaching a project through a symlink no longer hands a failing memo a fresh attempts count.
- Check C7 reads estimates over whole paragraph blocks. An estimate and its outcome verb split across two list items used to walk past it.
- `eval/score.sh` derives the ledger path from the memo path, accepts a `LEDGER` override, and marks M7 `UNSCORABLE` with an explicit error when no ledger can be read, instead of reporting a quiet `INCONCLUSIVE`.
- Setup step 8 pipes the probe citation into `court cite -`. Run with empty stdin the old form printed "no reporter-style citations were found" and exited 0, so a check that verified nothing read as a success.

### Changed

- README and `coverage-limits.md` state what the checks do not catch: the confidence check is a lint over common phrasings, the nonpublic-leak check is defeated by paraphrase, and URL provenance proves the host and the identifier rather than the document path.
- `eval/RUBRIC.md` and `eval/TASK.md` tell a third-party scorer two concrete ways to locate `score.sh` on a fresh install.
- `memo-house-style` records that the `[web, verify]` tag applies only to material the main session supplies, since the case-researcher agent has no web tools.
- The promised wall clock for `/lacuna:research` is now "typically 10 to 25 minutes, with progress lines" everywhere it appears, and the eval's S7 bar moved from 10 minutes to 25. Two live runs of the full task both landed at about 22 minutes on 2026-07-29, so the old 3 to 8 minute figure set the user up to think the run had hung.
- `memo-house-style` and `docket-research` require the public `courtlistener.com/docket/<id>/<slug>/` permalink in memo citations. The v4 API address returns 401 to any reader without a token.

## [0.1.0] - 2026-07-29

First release: federal docket and SEC filing research with ten deterministic verification checks.

### Added

- Three commands: `/lacuna:setup`, `/lacuna:research`, `/lacuna:verify`.
- `bin/lacuna`, a Python 3 stdlib data engine covering SEC EDGAR submissions,
  full-text filing search, archive documents, CourtListener search, dockets and
  citation lookup, and GDELT news. No third-party packages and no
  `pip install`. **No price leg**: see Not included, below.
- `bin/lacuna_verify.py`, the verification engine: ten deterministic checks
  covering structure and compliance, timestamp freshness, citation existence,
  docket identity, URL and accession provenance, quote fidelity and attribution,
  confidence discipline, provenance and restricted names, catalyst discipline,
  and search transparency.
- Four hook registrations dispatching to one script: a SessionStart banner that
  survives compaction, a PreToolUse egress and order-placement deny wall, and a
  verification gate registered on both Stop and SubagentStop that triggers on a
  content-hash scan of `cases/**/*.md`.
- Four skills: `memo-house-style`, `docket-research`, `filing-analysis`,
  `source-discipline`.
- One subagent, `case-researcher`, with an explicit tool allowlist and no
  permission bypass.
- Templates for the memo skeleton and the desk profile.
- A retrieval ledger and a raw response cache pruned automatically at 200 MB
  or 30 days on every write.
- `lacuna template memo` and `lacuna template profile`, which print the
  skeletons to stdout so no caller has to resolve the plugin root by hand.
- A network-free test suite covering the memo fixtures, the disarm paths found
  in review, the PreToolUse wall, the Stop gate and the profile gate, plus a
  black-box eval scored from the artifact and `curl`.

### Not included in this build

- **No price or return data.** There is no `price` subcommand and no Yahoo
  probe. A partial price leg without split and halt handling reports moves that
  did not happen, so nothing is reported at all. `## Price evidence` is a
  documented gap and the verifier blocks any return figure there that no
  ledgered price retrieval backs.
- **No `purge` subcommand and no `cache gc` subcommand.** README section 10
  gives the manual steps for privileged material.

### Notes

- Blocking is capped at two attempts per finding set. On the third fire the
  verifier writes a visible `## Verification failures` block and a
  `VERIFICATION FAILED` banner into the memo and stops blocking. A loud
  permanent failure is preferable to a rewrite loop nobody can escape.
- Infrastructure failures never block. Timeouts, DNS errors, 5xx, 401, 403, 429
  and TLS failures print a warning and exit 0. Only content findings block.
- The CourtListener token is free and needs no card. Without it, citation
  verification is off and every case citation is confined to the rejected
  section under a visible banner.

[Unreleased]: https://github.com/niclom12/lacuna-plugin/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/niclom12/lacuna-plugin/releases/tag/v0.1.0
