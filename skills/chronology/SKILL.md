---
name: chronology
description: Use when the user asks for a chronology or timeline of a case, says "chron this case", "what happened when", "put the sequence together", or needs the event spine behind a position before a memo gets written. Builds or updates a dated chronology from docket entries, court opinions, SEC filings, and news, de-duped, provenance-tagged, and marked by how much each event moves the outcome.
---

<!-- Provenance: adapted from anthropics/claude-for-legal,
     litigation-legal/skills/chronology/SKILL.md, Apache-2.0 (licence text: licenses/APACHE-2.0.txt).
     Adapted for lacuna: rebuilt for a litigation-driven trading desk. The
     attorney workflow (privilege gate, disclosed-document use restrictions,
     work-product headers, plaintiff/defense advocacy framing) is removed. The
     extraction method, de-duplication rule, gap reporting, provenance tagging,
     and the refusal to resolve contradictions are kept. -->

# Chronology

Facts happen in order, and the order is usually where the mispricing hides. A
chronology is the spine every later document hangs on: the situation section of a
memo, the catalyst calendar, the argument you make to yourself about why the
market has this wrong.

Structured extraction is something a model is good at. The failure mode is
equally reliable: an event that never happened, sitting in a clean table between
two real ones, looking exactly as credible. Everything below exists to keep that
event out, or failing that, to keep it labelled.

**Read the desk profile first.** If `desk-profile.md` is in the working folder,
open it and follow it: it carries what counts as verified for this analyst,
distrusted sources, standing interests, and pet peeves, all of which change what
gets tagged `key` and how the output reads. In Claude Code the same profile sits
in a fenced `lacuna desk profile` block in `~/.claude/CLAUDE.md` and loads by
itself. In Cowork nothing loads it for you, so opening the file is what makes it
apply. `/lacuna:interview` is what writes it.

## Sources, in the order to try them

1. **What the analyst hands you this session.** Paths, pasted docket text, PDFs,
   filing excerpts, links. Highest confidence, because a human chose it.
2. **The case workspace.** `cases/<case-id>/` in the workspace this session is
   running in, for an existing memo, a prior chronology, and any notes already
   gathered. If `cases/` does not exist yet, create it.
3. **The CourtListener MCP tools.** Docket entries with filed dates, opinions
   with decision dates, and the docket sheet header for the procedural spine.
   This is the strong default for court events, and it is the same connector in
   every environment.
4. **SEC filings.** 8-K items, the 10-K legal proceedings item, and the
   contingencies note carry dated litigation events with the company's own
   characterisation attached. Read them by whatever route this session has: a
   direct fetch of the EDGAR address is enough, and `edgar-research` carries the
   per-environment detail.
5. **The open web.** News, regulator press rooms, court sites, company IR pages.
   Fine to use, and every event taken from it carries a `[web, verify]` tag.

If a source you expected to reach is unreachable, name it in the Gaps section.
Silence about a source the reader assumed you used is the same as a wrong entry.

## Workflow

### 1. Fix the frame

Read the case theory if one exists (`cases/<case-id>/memo.md`, or ask). You need
one sentence: what has to happen for the position to work. That sentence is what
"significant" means for the rest of the run. Write it at the top of the output so
the reader can see what your tagging was measured against.

Say plainly which way the desk is leaning if it is leaning, and then watch
yourself for the obvious hazard: events that support the existing view feel more
significant than they are. When an entry is a close call, tag it lower and mark
it `[borderline]` for the reader to overrule.

### 2. Extract dated events

One event per document is the norm. Sometimes zero (undated, or nothing actually
happened). Sometimes several (an opinion resolving four motions).

Shapes that recur:

- **Filing:** `[date] [party] filed [document]` (entry number, court)
- **Order:** `[date] court [granted/denied/scheduled] [what]`
- **Corporate:** `[date] [company] disclosed [what]` (form type, accession)
- **Agency:** `[date] [agency] [opened/charged/settled] [what]`
- **Market-visible external event:** `[date] [thing happened]`
- **Scheduled future event:** `[date] [event] is set` (see the rule below)

**Forward-looking entries are leads.** A future date belongs in the chronology
only when a source states it. Quote the docket entry or the order text that sets
it, and mark anything you worked out from a rule rather than read from a document
as `[computed, verify]`. Deadline rules vary by court, judge, local rule, and
standing order, and a stay resets them. A computed date is a research lead for a
human to check before anyone relies on it as a date.

### 3. De-dupe

The same event surfaces three times: the docket entry, the company's 8-K, and a
wire story. That is one event with three sources. Merge it, and list all three.
Three rows for one event overstates how much happened.

### 4. Tag significance against the frame from step 1

- **key**: changes the probability of the outcome the position depends on
- **context**: supports a secondary point, or establishes a pattern
- **background**: true, useful for orientation, going nowhere near the thesis

Discipline: a chronology of 200 entries where 200 are tagged `key` has no tags.
Reserve `key` for events that would move the number. When in doubt, `context`.

### 5. Tag provenance on every row

Every entry carries where it came from:

- `[CourtListener]` only when it appeared in a CourtListener tool result this
  session
- `[SEC EDGAR]` with the accession number
- `[web, verify]` for anything from a web fetch or search
- `[model knowledge, UNVERIFIED]` for anything recalled rather than retrieved
- `[user provided]` for what the analyst stated

The tags are the reader's fastest signal about where to spend verification time,
so never strip or collapse them. An untagged date defaults to
`[model knowledge, UNVERIFIED]`, which is the honest reading of an entry nobody
can trace.

This rule reaches past the timeline table. The Gaps section, the key-events
section, any line characterising why an event matters, and any statement about a
limitations period, a tolling event, or a filing deadline are all analysis you
wrote. They carry the same tags the rows do.

### 6. Report gaps instead of filling them

If coverage for a stretch of the case is thin, say so and stop. Do not reach for
memory to smooth the timeline. Say: "Sources returned N events for [period].
Coverage looks thin. Options: point me at more sources, let me search the open
web with results tagged `[web, verify]`, or leave the gap noted. Which?" The
analyst decides whether to accept weaker sources.

## Output

Write to `cases/<case-id>/chronology.md` in the current workspace, creating the
folder if it is not there.

**When you create `cases/` for the first time**, deal with the privilege question
in the same breath. A chronology is work product and may be privileged, and
nothing in this plugin ignores `cases/` in the analyst's workspace, so a routine
commit would push it. Check whether the workspace is a git repository. **In Claude
Code:** `git rev-parse --is-inside-work-tree` answers that, and
`git check-ignore -q cases` says whether it is already ignored. **In Cowork:** look
for a `.git` directory or a `.gitignore` in the working folder. If it is a git
repository and `cases/` is not already ignored, offer to append `cases/` to its
`.gitignore`, with the one-line reason. Report what you did either way, and never
imply the folder is protected when it is not.

```markdown
# Chronology: [case name]

**Case:** [case-id]
**Built:** [YYYY-MM-DD]
**Version:** v[N]
**Sources:** [N] documents across [source types]
**Entries:** [N] ([N] key / [N] context / [N] background)
**Significance measured against:** [the one sentence from step 1]

## Timeline

| Date | Event | Tag | Source |
|---|---|---|---|
| [YYYY-MM-DD] | [what happened, one sentence] | key/context/background | [tag + link, entry no., or accession] |

## Key events

### [date]: [event title]
- **What:** [one line]
- **Why it moves the number:** [one line]
- **Source:** [tag + citation]

## Scheduled ahead

| Date (with time zone) | Event | Court | Basis |
|---|---|---|---|
| [YYYY-MM-DD HH:MM tz] | [event] | [court] | quoted entry text, or `[computed, verify]` |

## Gaps

**Date ranges with no events:** [ranges, and what you would expect to be there]
**Expected but not found:** [events the shape of the case implies should exist]
**Unreachable sources:** [named, with why]

## Markers used

- `[computed, verify]`: worked out from a rule rather than read from a document
- `[borderline]`: significance call the reader should overrule if they disagree
- `[conflict]`: sources disagree, both entries kept
- `[cite needed]`: event believed real, source not yet pinned

## Version history

- v[N] built [date] from [source summary]
- v[N-1] built [date]
```

## Incremental builds

If `chronology.md` already exists: read it, build the new one, then show the
diff. New events since the last build, existing events that gained a source,
entries removed with the reason. Increment the version and keep the version
history lines. A chronology whose changes are invisible is a chronology nobody
trusts on the second read.

## Verification scaled to stakes

- An entry the thesis rests on: open the source and read it. Quote the docket
  entry text in the Source column.
- A date someone will trade against: same, plus the time zone.
- Background and orientation entries: a source tag and a link are enough.
- Anything still carrying `[model knowledge, UNVERIFIED]` when you finish: say so
  in the handoff line, with the count.

Close by pointing the reader at the calls most likely to be wrong: "Here is what
I built. The `key` rows and anything marked `[borderline]` or `[computed, verify]`
are where I would look first."

## What this skill does NOT do

- **Does NOT resolve contradictions.** When two sources disagree about when
  something happened, both entries go in with `[conflict]`. Picking one is a
  judgment call for the reader, and it often needs a source neither of you has.
- **Does NOT invent events to fill a gap.** If it is not in a source, it is not a
  row. The Gaps section is where a suspected missing event goes.
- **Does NOT guarantee completeness.** A chronology is worth exactly what its
  sources are worth. When RECAP is missing three weeks of entries, the chronology
  is missing three weeks of entries, and it says so.
- **Does NOT calendar anything.** Dates in "Scheduled ahead" are leads for a
  human to verify against the court's own orders.
- **Does NOT forecast.** It puts events in order. What that order implies about
  probability is the memo's job, and the trade is the analyst's.
