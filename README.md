# lacuna

A research desk for litigation-driven trading, delivered as a plugin. It runs in
**Claude Cowork** and in **Claude Code**, from this one repository, with the same
skills and the same two commands in both. It is built for someone who is sharp
about markets and courts and new to working with AI.

Everything in it is markdown and JSON. There is no binary to install, no build
step, and nothing to compile, which is why the same bundle works in both places.

## What this is

Five things in one small bundle.

**Curated legal and finance skills.** Written practices, adapted from
Anthropic's own open legal and financial-services skill repos, that teach Claude
how to read a federal docket, how to work through an SEC filing, and how to cite
either one properly.

**Free court data.** Federal dockets, opinions, and a citation lookup, through
the CourtListener hosted MCP server run by the non-profit Free Law Project.
There is no key to buy and no trial to start. You approve a browser sign-in once
and it stays connected.

**Keyless EDGAR recipes.** SEC full-text search and the structured company APIs
need no account at all. The finance skills carry the endpoints and the etiquette
the SEC asks for, described so they work whether the fetch happens over the web
or from a terminal.

**Verification as scaled practice.** Claude is asked to size every substantive
task before starting it and to say which rung it put the task on. A quick lookup
gets a sanity check. Standard research is asked for a checking pass: resolve the
links, look up the citations, confirm the dates against sources. Anything with
money on it is asked for an independent re-derivation of the load-bearing claims
by something that has not read the working. Where a subagent is available, a
fresh one does that re-derivation and the two answers get compared. Where none is
available, the desk writes you a self-contained re-derivation brief, marks the
independent check as outstanding, and asks you to run it in a new conversation,
because a second pass inside the same context has already read the working it is
supposed to test. The skills also ask for facts kept visibly
separate from inference and guesswork, a timestamp on everything fetched, and an
unverified label on any citation nobody looked up. These are instructions Claude
reads and follows rather than checks something enforces, so see the honest limits
below.

**An interview that teaches Claude how you work.** Ten minutes of questions
about how you decide something is solid, which sources you trust, how long you
want a memo, and how you want probabilities put. The answers get written into a
durable profile. In Claude Code that profile is a fenced section of
`~/.claude/CLAUDE.md`, which every session loads by itself. In Cowork it is a
`desk-profile.md` in the folder you work in, and the skills open it at the top of
a piece of work when it is there, so keeping the file in that folder is what
makes it apply. The next section has the detail.

It never places a trade.

## Install

Same repository, two front doors.

### Claude Cowork

This plugin is not in the public plugin directory, so searching **Browse plugins**
for `lacuna` will not find it. The route in is to sync this repository as a
marketplace.

Open **Customize > Plugins**, choose the option to add a marketplace from a
GitHub repository or a git URL, and give it this address:

```
https://github.com/niclom12/lacuna-plugin
```

Cowork reads `.claude-plugin/marketplace.json` from the repository and offers
`lacuna` for install. Plugins currently save locally to the machine you install
them on, with org-wide sharing coming later, so a colleague syncs the same
marketplace rather than inheriting your copy.

### Claude Code

```
/plugin marketplace add niclom12/lacuna-plugin
/plugin install lacuna@lacuna-tools
```

The first line takes a GitHub `owner/repo` as shown, or the path to a local
checkout containing `.claude-plugin/marketplace.json`. If `/lacuna` shows no
commands afterwards, restart Claude Code.

### What differs between Cowork and Claude Code

Most of the desk is identical: the skills load the same way, the CourtListener
connector is the same server, the memo and chronology files land in the same
place, and the two commands read the same. Three things genuinely differ, and
every skill that touches them says so in plain language.

**Fetching SEC filings.** In Claude Code there is a terminal, so an EDGAR
endpoint can be pulled with a shell command and the response saved and processed
locally. Cowork's tool surface does not advertise a terminal, so the same
endpoints are read over the web instead. The finance skills describe the request
itself (the URL, the required `User-Agent`, the rate etiquette) and then give the
concrete per-environment form, so neither path is the only path.

**Where your desk profile lives.** Claude Code reads `~/.claude/CLAUDE.md` at the
start of every session, so `/lacuna:interview` writes its answers into a fenced
section of that file. Cowork has no `CLAUDE.md` and no `~/.claude` directory. It
keeps a Memory profile that Claude distils from your conversations, which you can
read and edit at **profile icon > Settings > Capabilities > Memory**, so in Cowork
the interview writes a `desk-profile.md` into the workspace you are working in and
tells you which answers are worth pasting into Memory as well. Nothing in Cowork
loads a file for you, so every skill that writes analyst-facing output opens
`desk-profile.md` from the working folder itself when it is there. Both the file
and the Memory page are plain text you own and can edit by hand.

**The docket sweep.** The sweep method lives in the `docket-sweep` skill, which
loads in both environments, so asking for "any new filings" or "sweep the
dockets" in plain language gets the same procedure and the same report either
way. Claude Code adds one thing on top: `docket-watcher`, a thin subagent
wrapper around that skill, so the sweep runs in its own context window and your
main thread receives the report rather than several hundred docket entries.
Cowork's plugin documentation lists sub-agents among the things a plugin can
bundle without documenting the `agents/` folder convention, so treat the wrapper
as best-effort there and the skill as the reliable path.

## The two commands

**`/lacuna:start`** is a five-minute orientation. What the skills do, how to
talk to Claude without learning any syntax, how permission and approval prompts
work and how to turn them down once you trust the flow, when planning first earns
its keep, the fact that your memory files are plain text you can edit, and how to
connect the court data. Run this first.

**`/lacuna:interview`** is the working-style interview described above. Run it
second, or whenever your standards change. Re-running it replaces only its own
fenced section of the profile and leaves everything around it untouched.

After those two, there are no more commands to learn. Ask for what you want in
plain language and the skills load themselves when they are relevant.

## What is on the desk

Ten skills. Claude loads one when the work calls for it; you never invoke them
by name.

Three cover the practice, and apply to everything:

- **`plan-execute-verify`** sizes the stakes out loud before starting, and sets
  how hard the result gets checked.
- **`verification-habits`** keeps evidence in front of claims, labels fact
  against inference against speculation, and states what was not covered.
- **`token-efficiency`** matches deliberation to the task, keeps noisy searches
  out of the main thread, and keeps the durable findings in a file instead of in
  chat scrollback.

Four cover the legal side:

- **`docket-research`** finds and reads federal dockets, opinions, and judges,
  and verifies that a citation points at a case that exists.
- **`chronology`** builds the dated event spine of a matter from dockets,
  opinions, filings, and news, de-duped and tagged with where each event came
  from.
- **`matter-briefing`** says where a tracked case stands, what moved since the
  last look, the next dated event, and how stale the file is.
- **`docket-sweep`** carries the portfolio sweep: every tracked case, everything
  filed since the last check, posture changes and dated events flagged as leads,
  written up as a dated report.

Three cover the company side:

- **`edgar-research`** works SEC EDGAR directly with no key: resolving a name to
  a CIK, full-text search, and pulling the body of a 10-K, 10-Q, 8-K, or 13D.
- **`earnings-analysis`** reads a quarter as a tradeable event, including how the
  contingencies note and Item 3 moved since last quarter.
- **`equity-research`** writes the company note: what the business earns, what a
  matter could cost it, and what that is worth, with every claim linked to the
  filing it came from.

`/lacuna:start` lists whatever is actually installed, which is a better source
than this README.

`templates/memo.md` is an optional starting shape for a writeup. It is a default
to bend rather than a form to fill in.

## The docket sweep

The sweep reads the docket of every case the desk tracks, pulls the entries filed
since the last check, flags posture changes and dated events as leads, and writes
a report to `cases/reports/`. Ask for "any new filings", "watch the dockets", or
"sweep the dockets before the open" and it runs; you never name anything directly.

The method is the `docket-sweep` skill, which loads in Cowork and in Claude Code
alike, so the procedure and the report are identical in both. In Claude Code
there is also `docket-watcher`, a subagent that does nothing but load that skill
and run it, which buys you a separate context window: the sweep reads several
hundred docket entries over there and your main thread receives the report.
Either way, every lead it returns still needs a person to read the filing and
decide what it means.

## The case workspace

Work on a tracked case accumulates under `cases/` in whatever workspace you are
working in: `cases/<case-id>/memo.md` holds the thesis and the verified facts,
`cases/<case-id>/chronology.md` holds the dated event spine, and docket sweeps
land in `cases/reports/`. You do not create any of it yourself, because Claude
creates the folder the first time a memo or a chronology needs somewhere to go,
and the case-id is just a short slug you agree on, such as `acme-appraisal`.

**Nothing in this plugin ignores `cases/` in your workspace.** The `.gitignore`
in this repository governs this repository only. So if the folder you work in is
a git repository, a memo written under `cases/` is a tracked file like any other
and a routine commit will push your work product to whatever remote that
repository has. Memos are work product and may be privileged, so the skills that
create `cases/` for the first time check whether the workspace is a git
repository and offer to add `cases/` to its `.gitignore`, saying what they did.
Accepting that offer is what makes tracking a memo a deliberate choice. If you
declined, or if the folder existed before this plugin did, the check is worth
running by hand.

## The philosophy

Version 0.1 enforced good practice with machinery: hooks that fired on every
tool call, deny rules over the shell, a Python verifier that blocked a memo
until ten mechanical checks passed. It worked, and it was the wrong shape,
because a desk that fights its analyst teaches nothing and nobody can direct
what they cannot see. Version 0.2 removed all of it and put the same discipline
into skills the model reads and follows, with the analyst able to see which rung
a task is on and overrule it.

Version 0.3 is the same idea carried one step further. A desk with no binaries,
no hooks, and no gates is a desk made of prose, and prose travels: it runs
wherever Claude reads skills, which is now Cowork as well as Claude Code. Where
the two environments really differ the instruction branches and says which branch
it is on, so nothing here has a terminal command as its only path.

The enforcement engines are not deleted from history: they live in git at commit
`e66db93`, if the argument for them ever wins. Use the commit rather than the
`v0.1.0` tag, because the tag was cut before the review round and three later
commits fixed the disarm paths, the config path, and a check that let an
unresolved case name through.

## Honest limits

- No good-law or citator check. Nothing here tells you a case was overruled,
  distinguished, or vacated. A lawyer reads every cited case before you rely on
  it.
- Federal courts only. State trial court matters are largely invisible unless a
  commercial source such as Trellis is added, which this plugin does not do.
- The RECAP document archive is contributed by users, so a filing missing from it
  may simply never have been purchased.
- EDGAR full-text search reaches back to 2001.
- No price or return figures unless a price source was actually queried in the
  session.
- Nothing in this plugin blocks Claude or checks up on it. The practices work
  because they are read and followed. If the output is wrong, telling it so is
  the fix.
- Cowork's tool surface is not publicly enumerated, so the Cowork branches assume
  only file creation and web access. If your Cowork session turns out to have
  more than that, the extra is a bonus rather than something a skill here depends
  on.
- Not legal advice. Not investment advice.

## Credits and licences

This plugin is MIT licensed. See `LICENSE`.

It stands on three pieces of other people's work, each vendored with a
provenance note at the top of the adapted file and the upstream licence text
copied into `licenses/`:

- **[anthropics/claude-for-legal](https://github.com/anthropics/claude-for-legal)**,
  Apache-2.0. Source of the `chronology`, `matter-briefing`, and `docket-sweep`
  skills, the `docket-watcher` subagent that wraps the last of those, and the
  CourtListener server entry in `.mcp.json`.
- **[anthropics/financial-services](https://github.com/anthropics/financial-services)**,
  Apache-2.0. Source of `earnings-analysis` and `equity-research`.

Both Apache-2.0 upstreams ship the same licence text and neither ships a NOTICE
file, so one copy at `licenses/APACHE-2.0.txt` covers both and there is nothing
further to carry forward under section 4(d).
- **[obra/superpowers](https://github.com/obra/superpowers)** by Jesse Vincent,
  MIT. `verification-habits` is adapted from its `verification-before-completion`
  skill. Worth installing alongside this plugin.

Court data comes from [CourtListener](https://www.courtlistener.com/) and the
[RECAP archive](https://www.courtlistener.com/recap/), both run by the
[Free Law Project](https://free.law/), a non-profit. Supporting them is a
reasonable thing to do with some of the money this desk saves you.

`docs/useful-things.md` has a paragraph on each of those, plus the SEC endpoints,
the eyecite citation library, the Cowork plugin directory, Anthropic's own Cowork
plugin collection, and the documentation worth reading in either environment.
Once the plugin is installed it lives in the plugin's own directory, which
`/lacuna:start` resolves for you. `docs/releasing.md` is for whoever ships the
next version: the two `claude plugin validate` targets that both have to pass,
the frontmatter sweep that catches a skill silently loading with no description,
and the version, portability, and style checks to run before tagging.
