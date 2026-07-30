<!--
A default shape for a memo, offered rather than imposed. Bend it. Drop sections
that do not apply, add ones that do, reorder it so the thing you care about sits
at the top. The only parts worth keeping in every memo are the three that stop a
reader mistaking a guess for a fact: what was verified, what was inferred, and
what was searched without result.

The finished memo belongs at `cases/<case-id>/memo.md` in the workspace you are
working in, whatever created it.

A memo is work product and may be privileged, and nothing in this plugin ignores
`cases/` in that workspace. So when `cases/` is created for the first time, check
whether the workspace is a git repository (in Claude Code, `git rev-parse
--is-inside-work-tree` and `git check-ignore -q cases`; in Cowork, look for a
`.git` directory or a `.gitignore` beside it) and offer to add `cases/` to its
`.gitignore`. Report what happened rather than assuming the folder is protected.

Delete this comment when you start a memo from this shape.
-->

---
case: <short slug or case name>
tickers: []
date: <YYYY-MM-DD>
status: candidate | tracked | closed
---

# <Title: the question this memo answers>

## Situation

Four to six plain sentences. What is happening, to whom, in which court or
filing, and why it is on the desk at all. No jargon a non-lawyer would have to
look up.

## What I verified

Facts with a source and a retrieval time attached. One line each.

- <fact> - <source name>, <url> - retrieved <YYYY-MM-DD HH:MM UTC>

## What I infer

Reasoning from the facts above, written as reasoning so it can be argued with.
Name the fact each step rests on.

## What I am speculating

Things I think are true and cannot support from anything above. Kept here on
purpose. Nothing in this section is a premise for anything in the two sections
above it.

## Catalysts

Dated events that could move the situation, each with a source for the date and
a label saying how firm it is.

- **<YYYY-MM-DD>** - <court or filer> - <event> - <url> - scheduled | expected | speculated

## Counter-evidence

The strongest case against the thesis, and what would falsify it. If this
section is empty the memo is not finished.

## What was searched

Queries run, where they were run, and what came back, including the ones that
found nothing. An empty result is a finding and the next reader needs to know it
was already tried.

---

**Honesty footer.** No good-law or citator check was performed: nothing here
tells you whether a cited case has been overruled, distinguished, or vacated. A
lawyer reads every cited case before this memo is relied on. Coverage is federal
courts and EDGAR full-text from 2001, so a state trial court matter may be
absent entirely. Not legal advice. Not investment advice.
