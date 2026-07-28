# Changelog

All notable changes to the `lacuna` plugin are recorded here. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this
project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The first line under each version heading is a one-sentence summary. The
SessionStart hook reads that line and shows it once when the installed version
changes, so keep it short and keep it plain.

## [Unreleased]

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
