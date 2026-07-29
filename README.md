# lacuna

A Claude Code plugin that turns a fresh session into a research desk for
litigation-driven trading. It is built for someone who is sharp about markets
and courts and new to working with AI.

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
the SEC asks for.

**Verification as scaled practice.** Claude is asked to size every substantive
task before starting it and to say which rung it put the task on. A quick lookup
gets a sanity check. Standard research is asked for a checking pass: resolve the
links, look up the citations, confirm the dates against sources. Anything with
money on it is asked for a fresh independent agent that re-derives the
load-bearing claims. The skills also ask for facts kept visibly separate from
inference and guesswork, a timestamp on everything fetched, and an unverified
label on any citation nobody looked up. These are instructions Claude reads and
follows rather than checks something enforces, so see the honest limits below.

**An interview that teaches Claude how you work.** Ten minutes of questions
about how you decide something is solid, which sources you trust, how long you
want a memo, and how you want probabilities put. The answers get written into
your global `CLAUDE.md`, so every session afterwards already knows them.

It never places a trade.

## Install

```
/plugin marketplace add ./lacuna-plugin
/plugin install lacuna@lacuna-tools
```

The first line takes the directory containing `.claude-plugin/marketplace.json`,
so a local checkout works as shown; if you are pulling from GitHub, use
`niclom12/lacuna-plugin` in place of the path. If `/lacuna` shows no commands
afterwards, restart Claude Code.

## The two commands

**`/lacuna:start`** is a five-minute orientation. What the skills do, how to
talk to Claude without learning any syntax, how permission modes work and how to
turn the approval prompts down once you trust the flow, when plan mode earns its
keep, the fact that your memory files are plain text you can edit, and how to
connect the court data. Run this first.

**`/lacuna:interview`** is the working-style interview described above. Run it
second, or whenever your standards change. Re-running it replaces only its own
fenced section in `~/.claude/CLAUDE.md` and leaves the rest of that file
untouched.

After those two, there are no more commands to learn. Ask for what you want in
plain language and the skills load themselves when they are relevant, and the
`docket-watcher` subagent starts itself when you ask for a docket sweep.

## What is on the desk

Nine skills. Claude loads one when the work calls for it; you never invoke them
by name.

Three cover the practice, and apply to everything:

- **`plan-execute-verify`** sizes the stakes out loud before starting, and sets
  how hard the result gets checked.
- **`verification-habits`** keeps evidence in front of claims, labels fact
  against inference against speculation, and states what was not covered.
- **`token-efficiency`** routes planning to the strong model and execution to
  the mid model, pushes noisy searches into subagents, and keeps the durable
  findings in a file instead of in chat scrollback.

Three cover the legal side:

- **`docket-research`** finds and reads federal dockets, opinions, and judges,
  and verifies that a citation points at a case that exists.
- **`chronology`** builds the dated event spine of a matter from dockets,
  opinions, filings, and news, de-duped and tagged with where each event came
  from.
- **`matter-briefing`** says where a tracked case stands, what moved since the
  last look, the next dated event, and how stale the file is.

Three cover the company side:

- **`edgar-research`** works SEC EDGAR directly with no key: resolving a name to
  a CIK, full-text search, and pulling the body of a 10-K, 10-Q, 8-K, or 13D.
- **`earnings-analysis`** reads a quarter as a tradeable event, including how the
  contingencies note and Item 3 moved since last quarter.
- **`equity-research`** writes the company note: what the business earns, what a
  matter could cost it, and what that is worth, with every claim linked to the
  filing it came from.

One subagent, `docket-watcher`. It sweeps the docket of every case the desk
tracks, pulls the entries filed since the last check, flags posture changes and
dated events as leads, and writes a report to `cases/reports/`. Ask for "any new
filings", "watch the dockets", or "sweep the dockets before the open" and it
runs in its own context window; you never name it directly. Every lead it
returns still needs a person to read the filing and decide what it means.

`/lacuna:start` lists whatever is actually installed, which is a better source
than this README.

`templates/memo.md` is an optional starting shape for a writeup. It is a default
to bend rather than a form to fill in.

## The case workspace

Work on a tracked case accumulates under `cases/` in whatever project you are
working in: `cases/<case-id>/memo.md` holds the thesis and the verified facts,
`cases/<case-id>/chronology.md` holds the dated event spine, and docket sweeps
land in `cases/reports/`. You do not create any of it yourself, because Claude
creates the folder the first time a memo or a chronology needs somewhere to go,
and the case-id is just a short slug you agree on, such as `acme-appraisal`.
`.gitignore` keeps `cases/` out of git on purpose, since memos are work product
and may be privileged, so tracking them is a deliberate opt-in.

## What changed from 0.1

Version 0.1 enforced good practice with machinery: hooks that fired on every
tool call, deny rules over the shell, a Python verifier that blocked a memo
until ten mechanical checks passed. It worked, and it was the wrong shape,
because a desk that fights its analyst teaches nothing and nobody can direct
what they cannot see. Version 0.2 removes all of it and puts the same discipline
into skills the model reads and follows, with the analyst able to see which rung
a task is on and overrule it. The enforcement engines are not deleted from
history: they live in git at commit `e66db93`, if the argument for them ever
wins. Use the commit rather than the `v0.1.0` tag, because the tag was cut before
the review round and three later commits fixed the disarm paths, the config path,
and a check that let an unresolved case name through.

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
- Not legal advice. Not investment advice.

## Credits and licences

This plugin is MIT licensed. See `LICENSE`.

It stands on three pieces of other people's work, each vendored with a
provenance note at the top of the adapted file and the upstream licence text
copied into `licenses/`:

- **[anthropics/claude-for-legal](https://github.com/anthropics/claude-for-legal)**,
  Apache-2.0. Source of the `chronology` and `matter-briefing` skills, the
  `docket-watcher` subagent, and the CourtListener server entry in `.mcp.json`.
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
the eyecite citation library, and the Claude Code documentation worth reading.
Once the plugin is installed it lives in the plugin's own directory, which
`/lacuna:start` resolves for you. `docs/releasing.md` is for whoever ships the
next version: the two `claude plugin validate` targets that both have to pass,
the frontmatter sweep that catches a skill silently loading with no description,
and the version and style checks to run before tagging.
