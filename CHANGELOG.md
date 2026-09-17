# Changelog

All notable changes to the `lacuna` plugin are recorded here. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this
project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The first line under each version heading is a one-sentence summary. Keep it
short and keep it plain.

## [0.7.0] - 2026-09-17

One paste and you are connected: a second plugin, `lacuna-desk`, carries both
of Nic's live services and asks you for your keys as it installs.

### Added

- **A `lacuna-desk` plugin** in the same marketplace. It holds the addresses of
  the news desk and the alerts archive, and declares two options, a news desk
  key and an alerts key, which it asks for on install. The keys never touch
  this repository, so the repository stays public and each person's access
  stays their own.
- **The alerts archive**, reachable for the first time from the plugin. It
  holds every alert the monitors have sent: market odds, docket entries,
  opinion days, and the health of the monitors themselves.

- **An `alerts` skill.** It reads the alerts archive in plain words: what
  happened overnight, what is going on with a situation, how noisy something
  has been, what one alert meant, and whether the monitors are still running.
  It is read only, and it says so when asked to change anything.

### Notes

- Installing from a terminal takes one line, which Nic sends: it adds the
  marketplace, installs both plugins, and passes the keys in one go. In Cowork
  the same thing is done by hand from Customize then Plugins, pasting each key
  into the box the plugin asks for.
- The older `lacuna-news:v1:` code still works and still needs no terminal.

## [0.6.0] - 2026-09-15

A first-time setup that does the work for you: say "set up the desk" after
installing and it checks the desk is loaded, connects the news desk with the
code Nic sent you, and tells you what to ask for next. The only thing you type
is the code.

### Added

- **A `setup` skill.** It is the first thing to run after installing. It
  confirms the desk is really loaded, hands over to the news connection with
  your code, covers the restart, and closes with four things you could say
  next, written out as sentences you could type. Everything it says is plain
  English, and every reply ends with what was done and what is recommended.

### Changed

- **`/lacuna:news` now answers the "I have no code" case directly**, in one
  sentence, instead of leaving a new person to work out that a code has to come
  from somewhere.
- **`/lacuna:start` points a brand new person at the setup skill** rather than
  making them read the whole tour first, and tells anyone who asks about share
  prices that market data is a separate thing with its own code from Nic.

## [0.5.0] - 2026-09-14

The news desk for people who are not technical: one command, `/lacuna:news`,
connects you or tells you how the desk is doing, and every news skill now talks
in plain words, ends each answer with what was done and what to do next, and
knows how to send a company's news to your email or phone.

### Added

- **`/lacuna:news`**, the one door to the news desk. If you are not connected
  it connects you, using the code Nic sends you. If you are, it says in three
  lines how many companies the desk is following, whether everything is
  running, and whether you can add companies, then lists the four things you
  can say next.
- **Send a company's news to yourself.** When you start watching a company the
  desk asks once where the news should go: an email address, a phone number for
  WhatsApp, both, or just the desk. You can change that later ("send it to my
  phone") or stop it ("stop sending that to me"). Your email gets everything;
  your phone gets only stories that matter and are less than two days old,
  plus the company's own filings, so an old story never buzzes you.
- **Check a feed more or less often.** "Check that company's feeds every 20
  minutes" works, between once a minute and once a day. The desk will not go
  faster than once a minute so the news sites do not block it.

### Changed

- Every news-facing skill and command is written for someone who has never
  opened a terminal. Nothing technical reaches you: no internal names, no
  commands, no raw output. If something goes wrong you get one or two plain
  sentences and are told to ask Nic. Every answer ends with two lines, what
  was done and what is recommended.
- `news-connect` says plainly what to do with a cut-off code, a refused code,
  an existing connection (it asks before replacing), and the restart, and that
  your companies and settings are safe through all of them. Connecting now
  also leaves a short note in your Claude Code memory file so that every later
  session handles news questions the plain way; disconnecting removes it.
- `news-watch` is complete against the desk: watching a company, asking what
  the news is, sending news to your email or phone, pausing, resuming,
  removing, quietening a noisy outlet, ignoring stories about something else
  with the same name, and changing how often a feed is checked. Every example
  uses invented companies.
- `/lacuna:start` mentions the news desk in one short paragraph pointing at
  `/lacuna:news`. In Cowork it says the news desk needs Claude Code for now.
- `README.md` has a short section for people who just want to use the news
  desk, and a separate factual section for the technical reader.

## [0.4.0] - 2026-09-14

The news desk: a person with a connection code from Nic can connect to the Lacuna
news desk from Claude Code, read the news, and, with write access, add and manage
the companies it watches.

### Added

- **`news-connect`.** Takes the one-line connection code Nic sends privately,
  proves the key works, registers the news server for that person at user scope
  without ever printing the key, and reports in plain words what they can do. It
  handles a damaged code, a refused key, an unreachable server and an existing
  connection each with one plain sentence. Claude Code only: Cowork cannot give
  each person their own key for a custom connector yet, and the skill says so.
- **`news-watch`.** Ask what the news is, add a company, pause, resume, change or
  remove a watch, mute an outlet, and change how often a feed is checked. The
  agent drafts the names, tickers, searches, SEC number and the paragraph on
  what matters, reads them back as one sentence, and saves only on a yes. Every
  change ends with what was done and what is recommended. A read-only
  connection gets a plain explanation that writing needs access from Nic.
- **`add-monitor`.** Sends news requests to `news-watch`. For a docket, a
  prediction market, a web page or a state court case it gathers the minimum and
  drafts a ready-to-send request to Nic, who sets those up.

### Changed

- `/lacuna:start` mentions the news desk when it is connected, and otherwise
  says in one line how to connect it.
- The plugin keeps no server address and no key. Both arrive in the person's
  connection code and live only in their own Claude Code settings.

## [0.3.0] - 2026-07-30

The dual-target port: the same desk now runs in Claude Cowork and in Claude Code,
with every instruction that assumed a terminal, a `CLAUDE.md`, or a subagent
branching explicitly instead.

### Changed

- **The target.** 0.2 was a Claude Code plugin. 0.3 is the same bundle running in
  both Claude Cowork and Claude Code, which costs nothing structurally because
  Cowork plugins use the identical layout (`.claude-plugin/plugin.json`,
  `.mcp.json`, `commands/`, `skills/`) and this bundle has been markdown and JSON
  with no binaries since 0.2.
- **Portability is now a rule rather than an accident.** No instruction has a
  terminal command as its only path. Where an action is available by more than one
  route the skill describes the action first ("fetch this address") and then gives
  the concrete per-environment form, labelled in plain language as "In Cowork" and
  "In Claude Code".
- `README.md` leads with the fact that it runs in both, gives the two install
  paths side by side (Cowork's **Customize > Plugins**, syncing the marketplace
  from the repository's git URL or installing from the plugin directory; Claude
  Code's `/plugin marketplace add` and `/plugin install`), and adds a
  "What differs between Cowork and Claude Code" section covering the three real
  differences: SEC fetches, where the desk profile lives, and the docket sweep.
  It also records that Cowork plugins currently save locally to the machine they
  are installed on, with org-wide sharing coming later.
- The desk profile is now described by what it is rather than by the file that
  held it. Claude Code keeps it in a fenced section of `~/.claude/CLAUDE.md`.
  Cowork has no `CLAUDE.md` and no `~/.claude`, so the profile lives in a
  `desk-profile.md` in the workspace alongside Claude's own Memory profile, which
  the analyst can read and edit at profile icon > Settings > Capabilities > Memory.
- `plan-execute-verify` rung 3 states both forms of the independent
  re-derivation and no longer treats them as equivalent. Where a subagent is
  available, a fresh one derives the load-bearing claims and the model completes
  the check itself. Where none is available, the model cannot open a fresh
  conversation and must not claim it did: it writes a self-contained re-derivation
  brief (claims restated as open questions, the sources, none of its reasoning),
  marks the independent check OUTSTANDING, and asks the analyst to run it and
  report back. The precedence rule shared with `verification-habits` is unchanged
  and still stated identically in both files.
- The desk profile is now actually read. Every skill that writes analyst-facing
  output (`plan-execute-verify`, `verification-habits`, `chronology`,
  `matter-briefing`, `earnings-analysis`, `equity-research`, `docket-sweep`) opens
  `desk-profile.md` from the working folder when it is there and follows it. Cowork
  auto-loads no file, so this is what makes the Cowork half of the interview apply
  at all, and the copy in `README.md`, `commands/start.md`, and
  `commands/interview.md` now says that rather than implying the file is picked up
  for you.
- Environment detection in both commands makes a shell or Bash tool decisive for
  Claude Code on its own, with `~/.claude` as confirmation rather than a second
  required condition. A read of `~/.claude/CLAUDE.md` that was refused or left
  unapproved is distinguished from a path that is absent, so a denied permission
  prompt no longer routes a Claude Code user down the Cowork branch.
- `skills/edgar-research` carries a measured table of how the SEC hosts treat the
  `User-Agent` header, replacing a model of it that was inverted. All hosts refuse
  a request with no header; `data.sec.gov` and `efts.sec.gov` accept any non-empty
  one; `www.sec.gov`, which serves the filing documents, the ticker mapping, and
  `cgi-bin/browse-edgar`, refuses a browser-style header and answers only when the
  header carries an address. The Cowork consequence is stated plainly instead of
  implying a working path: where a fetch tool cannot set the header, filing
  documents are unavailable and the honest output is to hand over the URL and ask
  the analyst to paste the text. The SEC contact address is kept as the published
  condition of use rather than presented as server behaviour.
- `commands/start.md` section 3A describes EDGAR fetches as arriving by `WebFetch`
  by default and by `curl` where a shell is the better route, so the permission
  rule set it prints covers both, and it no longer teaches that every fetch is a
  shell command.
- `commands/start.md` describes connector enablement by the outcome to look for
  (the CourtListener tools present in the tool list, one browser sign-in on first
  use) with the panel path given as a likely location, and adds the recovery line
  that `docket-research` already carries: say so plainly and fall back to the open
  web with `[web, verify]` tags.
- `commands/interview.md` tells the analyst that notes kept across re-runs belong
  outside the markers, and shows the current block content and asks before
  replacing it on a re-run. The SEC contact address is still collected in both
  branches, with the honest reason attached: the header can be set exactly in
  Claude Code and a Cowork fetch tool usually cannot apply it.
- `README.md` leads the Cowork install with syncing the marketplace from the
  repository's git URL as the only route, and says in one line that the plugin is
  not in the public directory, matching `docs/useful-things.md`.
- `README.md` no longer claims this repository's `.gitignore` protects the
  analyst's `cases/` folder, because it governs this repository only. The skills
  that create `cases/` (`chronology`, `matter-briefing`, `docket-sweep`, and the
  `templates/memo.md` header) now check whether the workspace is a git repository
  on first creation and offer to add `cases/` to its `.gitignore`, reporting what
  they did.
- `token-efficiency` no longer assumes subagents, background execution, or a
  choosable model. Noisy retrieval goes into a subagent where one exists and into
  a file on disk where one does not, with the same underlying rule in both cases:
  raw retrieval belongs in a file and the conversation holds conclusions with
  their sources. Slow fetches overlap with thinking whether or not there is a
  background runner. The model-routing table now reads as guidance on how much
  deliberation a task deserves wherever the model is not the analyst's to pick.
- The docket sweep method moved out of `agents/docket-watcher.md` and into a
  skill. Skills are documented as bundleable in Cowork and `agents/` is not, so a
  method that lived only in an agent file was unreachable there while three places
  claimed otherwise. `agents/docket-watcher.md` is now a thin subagent wrapper that
  loads the skill and returns its report, and it buys exactly one thing: a separate
  context window in Claude Code. The Apache-2.0 provenance header travels with the
  method and is present in both files.
- `chronology`, `matter-briefing`, and `docket-sweep` say "workspace" where they
  used to say "project", and each names creating `cases/` when it is missing
  rather than assuming a local checkout.
- `templates/memo.md` says where the finished memo belongs and drops the
  assumption that it gets there by copying a file out of the plugin directory.
- Both manifests describe the plugin as running in Cowork and Claude Code.

### Added

- `skills/docket-sweep`, the portfolio docket sweep as a skill: the sweep list,
  the skip-closed-cases rule, the reading discipline for orders, the
  `[computed, verify]` marking of derived dates, the NEEDS A LOOK / DATED AHEAD /
  POSTURE CHANGES / QUIET / OUTSIDE COVERAGE report template, and the report path
  under `cases/reports/`. It carries the Apache-2.0 provenance note from
  `anthropics/claude-for-legal`, since that is where the method came from, and it
  loads in Cowork and in Claude Code alike. Ten skills now, up from nine.
- `docs/useful-things.md` gains two pointers: the Cowork plugin directory at
  <https://claude.com/plugins>, and `anthropics/knowledge-work-plugins`, the
  Anthropic collection built for Cowork and compatible with Claude Code, which is
  the reference for what a Cowork plugin is allowed to contain. Everything already
  there is kept, with the documentation section noting which pages describe a
  Claude Code path and what the Cowork equivalent is.
- `docs/releasing.md` gains a portability sweep to run before tagging, checking
  that no shipped instruction leaves a terminal command as the only path and that
  every `CLAUDE.md` reference is branched. The version-agreement check is
  unchanged, because 0.3 adds no new versioned file: `.claude-plugin/plugin.json`,
  `.claude-plugin/marketplace.json`, and the top `CHANGELOG.md` heading are still
  the complete set, and the check now says so.

## [0.2.0] - 2026-07-30

The expressive edition: the enforcement machinery is gone and the same discipline
now lives in skills the model reads and the analyst directs.

### Changed

- **The whole philosophy.** 0.1 held the line with machinery: hooks on every tool
  call, deny rules over the shell, site restrictions, and a Python verifier that
  blocked a memo until ten deterministic checks passed. 0.2 asks for the same
  standards in prose and trusts the model to follow them, because a desk that
  fights its analyst teaches nothing and nobody can direct what they cannot see.
  Verification is now a dial sized to the stakes rather than a wall in front of
  every memo.
- Legal and finance practices are adapted from Anthropic's open
  `claude-for-legal` and `financial-services` repositories, each vendored file
  carrying a provenance note and the upstream Apache-2.0 text copied into
  `licenses/`.
- Court data now arrives through the hosted CourtListener MCP server rather than
  a bundled Python client and a pasted API token. First use opens a browser
  sign-in, it costs nothing, and there is no key to store.
- SEC access is documented as keyless recipes over EDGAR full-text search and the
  `data.sec.gov` company APIs.
- `templates/memo.md` is a short optional shape with a header saying so, in place
  of the fourteen-section form the verifier used to police.
- `README.md` is rewritten for the new shape, with a credits and licences section
  naming every upstream source.
- `.gitignore` keeps `cases/` and drops the entries for machinery that no longer
  exists.

### Added

- `/lacuna:start`, a five-minute orientation: what the skills do, how to ask for
  things without learning any syntax, permission modes including how to turn the
  approval prompts down once the flow is trusted, when plan mode is worth it,
  that the memory files are plain text the analyst owns, where case files live,
  and how to connect the court data.
- `/lacuna:interview`, a conversational ten-minute interview on working style,
  covering what counts as verified, trusted and distrusted sources, depth
  calibration, memo length and hedging taste, standing interests, pet peeves, and
  how to express probabilities. It writes the result into a fenced section of the
  global `~/.claude/CLAUDE.md`, replacing only its own section on a re-run and
  never touching anything outside the markers, and offers a project-level copy.
- `skills/plan-execute-verify`, the severity ladder as practice: quick lookup,
  standard research, and high-stakes work each get a stated rung with matching
  planning and verification, including when to escalate mid-flight.
- `skills/verification-habits`, adapted with attribution from the
  `verification-before-completion` skill in obra/superpowers (MIT), tuned to
  legal and financial research: evidence before claims, fact against inference
  against speculation, timestamps on retrievals, unlooked-up citations labelled
  unverified, quotes limited to what the document says, and coverage limits
  stated out loud.
- `skills/token-efficiency`, on model routing, subagents for noisy searches,
  backgrounding long fetches, not re-reading what is established, and keeping the
  memo as the durable artifact.
- `docs/useful-things.md`, a pointer page covering CourtListener and the
  commercial state-court option, both Anthropic source repositories, the
  superpowers plugin, the SEC endpoints, the RECAP archive, eyecite, and the
  Claude Code documentation worth reading.
- `agents/docket-watcher`, adapted with attribution from the same agent in
  `claude-for-legal`: a subagent that sweeps every tracked case for entries filed
  since the last check, flags posture changes and dated events as leads, and
  writes a report under `cases/reports/`. Documented in `README.md` and named in
  the `/lacuna:start` tour, so it is discoverable without reading the tree.
- The `cases/` workspace is now introduced properly, in `README.md` and in the
  `/lacuna:start` tour: what `cases/<case-id>/` holds, that Claude creates it on
  first use rather than the analyst scaffolding it, and why `.gitignore` keeps it
  out of git. The three files that read it also create it when it is missing.
- A precedence rule shared between `plan-execute-verify` and
  `verification-habits`, stated identically in both, so the rung named by the
  first decides how much of the second applies instead of the two skills
  contradicting each other when both load in one turn.
- `licenses/`, holding the upstream licence text for every vendored source. Both
  Apache-2.0 upstreams ship identical licence text and neither ships a NOTICE
  file, so `licenses/APACHE-2.0.txt` is one copy covering both.
- `docs/releasing.md`, describing both `claude plugin validate` targets and what
  each one does and does not check, plus the frontmatter, version-agreement,
  style, and headless-load checks to run before tagging.

### Removed

- All hooks, including the SessionStart banner and the tool-call gates.
- All permission deny rules and site restrictions.
- The `bin/lacuna` client and `bin/lacuna_verify.py` verifier, the ten
  deterministic memo checks, the retrieval ledger, and the local `.lacuna/`
  state directory that fed them.
- `/lacuna:setup`, `/lacuna:research`, and `/lacuna:verify`, along with the
  `case-researcher` agent and the eval harness that scored them.
- Nothing is lost: all of it remains in git history at commit `e66db93`, if the
  argument for enforcement ever wins. That commit rather than the `v0.1.0` tag,
  because the tag was cut before the review round and the three commits after it
  carry the fixes listed below.

## [Superseded, unreleased against 0.1]

The entries below fixed the 0.1 enforcement machinery and never shipped in a
release. 0.2.0 removes that machinery, so they are kept as a record of what was
learned rather than as a description of current behaviour.

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
