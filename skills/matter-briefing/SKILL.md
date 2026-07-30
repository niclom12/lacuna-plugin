---
name: matter-briefing
description: Use when the user says "brief me on <case>", "where are we on <case>", "catch me up", or "what changed", or wants a read on a tracked case before a call. Reports where the case stands, what has moved since the last look, the next dated event, what would break the thesis, and what is still unknown, then flags how old the underlying file is.
---

<!-- Provenance: adapted from anthropics/claude-for-legal,
     litigation-legal/skills/matter-briefing/SKILL.md, Apache-2.0 (licence
     text: licenses/APACHE-2.0.txt).
     Adapted for lacuna: rebuilt for a litigation-driven trading
     desk. The attorney framing (conflicts gate, work-product header, reserve and
     materiality fields, GC and outside-counsel audience) is removed. The
     briefing shape, the staleness flag, the re-assessment prompt, the "say what
     is known and flag what is not" tone, and the read-only stance are kept. -->

# Matter briefing

A briefing is a read on one case, delivered fast, honest about its own age. It
answers four questions: where does this stand, what moved, what is next, and what
would change our mind.

It reads and reports. It does not update the case file, and it does not decide
anything.

## Load

**The desk profile first.** If `desk-profile.md` is in the working folder, open it
and follow it: it carries what counts as verified for this analyst, distrusted
sources, briefing length and hedging taste, how probabilities get expressed, and
pet peeves. In Claude Code the same profile sits in a fenced `lacuna desk profile`
block in `~/.claude/CLAUDE.md` and loads by itself. In Cowork nothing loads it for
you, so opening the file is what makes it apply. `/lacuna:interview` is what
writes it.

Then the case:

- `cases/<case-id>/memo.md`: the thesis, the verified facts, the catalyst
  calendar, what was already rejected as unverified
- `cases/<case-id>/chronology.md`: the event spine, if one has been built
- Any other notes in `cases/<case-id>/`
- The docket itself, via the CourtListener MCP tools, when the file is older than
  the case is moving (see Staleness)

`cases/` sits in whatever workspace the session is running in, and if it does not
exist yet, create it. A first briefing on a desk with no case folder is a normal
situation rather than an error.

**When you create `cases/` for the first time**, deal with the privilege question
in the same breath. Case material is work product and may be privileged, and
nothing in this plugin ignores `cases/` in the analyst's workspace, so a routine
commit would push it. Check whether the workspace is a git repository. **In Claude
Code:** `git rev-parse --is-inside-work-tree` answers that, and
`git check-ignore -q cases` says whether it is already ignored. **In Cowork:** look
for a `.git` directory or a `.gitignore` in the working folder. If it is a git
repository and `cases/` is not already ignored, offer to append `cases/` to its
`.gitignore`, with the one-line reason. Report what you did either way, and never
imply the folder is protected when it is not.

If the case-id is missing or ambiguous, list what is in `cases/` and ask which
one. Do not guess between two similar names; corporate captions repeat.

If there is no case file at all, say so and offer the alternative: "Nothing in
`cases/` for that name. I can research it from scratch, which takes longer, or
you can point me at the file." A briefing invented from memory is the worst
output this skill could produce.

## The briefing

```markdown
# [Case name]: briefing as of [YYYY-MM-DD]

**Stage:** [where the case is procedurally]
**Court:** [court, judge, docket number]
**Case file last updated:** [date] [flag STALE if the docket has moved since]
**Thesis in one line:** [from the memo]

## Where this stands

[One paragraph of current posture in plain English. What is pending, before whom,
and what the case is waiting on. No jargon that would need a lookup.]

## What has changed

[The last three to five events, most recent first, each with a source tag. If
nothing has changed since the last look, say that in one line and give the date
of the last event rather than padding.]

## What is next

- **Next dated event:** [date with time zone, what it is, and the quoted docket
  entry or order that sets it. Mark `[computed, verify]` if you worked it out
  from a rule rather than read it from a document.]
- **Then:** [the following one or two, same standard]
- **Waiting on:** [anything pending with no date attached, which is most of it]

## What the thesis rests on

[The two or three load-bearing facts or assumptions. For each: is it still true,
and how do we know as of today?]

## What would change our mind

[The specific, observable things that would break the thesis. An adverse ruling
on a named motion, a settlement, a stay, a disclosure. Concrete enough that the
reader would recognise it in a headline.]

## Open questions

[What is genuinely unknown, including anything the memo already parked in its
rejected-and-unverified section. Sealed entries live here: date and filer known,
contents unknown, no inference drawn.]

## Confidence and its age

[One or two lines. How much of this briefing came from a live retrieval today
versus from a file written weeks ago. Count the entries still carrying
`[model knowledge, UNVERIFIED]`.]
```

## Staleness

Litigation moves in bursts, so age matters more than any fixed interval. Check
the case file's last-updated date against how fast the case has been moving.

- **File older than 14 days, or a dated event has passed since it was written:**
  flag it at the top and refresh the docket before briefing. A briefing that
  quietly reports last month's posture is worse than no briefing.
- **File current:** say so, with the date.
- **Either way, name the date behind every "currently".**

RECAP is a mirror of PACER filled in by its users, so a clean refresh may mean
nothing was filed or may mean nobody has pulled the docket lately. Report which
of those you know.

## Tone

Say what is known. Flag what is not. A case opened last week with two docket
entries produces a short briefing, and short is the correct length for it. Do not
pad to look thorough. If the honest answer to "what changed" is "nothing since
the 12th", that sentence is the section.

## Re-assessment prompts

End with questions rather than answers. The reader holds the position, and the
reader decides.

- Does the thesis still say what you would say today?
- Has the timing assumption held, or has the case slowed?
- Is anything in the memo's verified-facts section now stale enough to recheck?
- Is there an angle nobody has looked at since the case opened?

Then offer the next steps that fit what you just found: refresh the docket,
research a specific angle, rebuild the chronology, verify a particular citation,
or stop here. The reader picks.

## What this skill does NOT do

- **Does NOT predict outcomes.** It reports posture and surfaces the questions a
  forecast would have to answer.
- **Does NOT size or recommend a position**, and it never places a trade.
- **Does NOT write to the case file.** It reads. Changes to the thesis or the
  facts belong in the memo, made deliberately.
- **Does NOT calendar deadlines.** Dates in "What is next" are leads for a human
  to verify against the court's own orders.
- **Does NOT fill gaps from memory.** A thin case file produces a thin briefing
  with the gaps named.
