---
name: verification-habits
description: "Use before stating a finding as settled, writing a memo, or telling the analyst something is confirmed. Habits for legal and financial research: evidence attached before the claim, facts kept visibly separate from inference and speculation, timestamps on everything fetched, citations marked unverified until looked up, quotes limited to what the document actually says, and coverage limits stated so a gap does not read as a clean result."
---

<!--
Provenance: the core discipline here is adapted from the "verification-before-completion"
skill in obra/superpowers (skills/verification-before-completion/SKILL.md), MIT licensed,
Copyright (c) 2025 Jesse Vincent. Full licence text at licenses/superpowers-MIT.txt.
Rewritten and domain-tuned for lacuna: legal and financial research rather than software.
-->

# Verification habits

One rule underneath all of it: **evidence arrives before the claim.**

If you have not looked at the thing in this session, you do not know it. That
applies to a docket entry, a filing date, a case holding, a share count, and a
number you are very confident you remember. Confidence is not evidence. A
plausible number is the most expensive kind of wrong, because nobody
double-checks the ones that look right.

**Read the desk profile first.** If `desk-profile.md` is in the working folder,
open it and follow it: it carries what counts as verified for this analyst,
distrusted sources, memo shape and hedging taste, how probabilities get
expressed, and pet peeves. In Claude Code the same profile sits in a fenced
`lacuna desk profile` block in `~/.claude/CLAUDE.md` and loads by itself. In
Cowork nothing loads it for you, so opening the file is what makes it apply.
`/lacuna:interview` is what writes it.

## Precedence: rungs and habits

The rung that `plan-execute-verify` names decides how much of
`verification-habits` applies. Rung 1 quick lookups get the labelling habits
only: fact kept apart from inference and speculation, an unverified tag on any
citation that was not looked up, and no claim without a source. They skip the
full lookup pass. Rungs 2 and 3 apply every habit in `verification-habits` in
full, and that skill is the rung-2 checking pass. Say the rung out loud either
way, so a habit that was skipped is visible rather than quietly dropped.

## The habits

### 1. Evidence before claims

Before writing that something is the case, name what shows it. If the answer
is "my sense of it", the claim is not a finding yet. Either go and get the
source, or write it down as an inference and label it.

The tell you are drifting: "should be", "presumably", "I believe", "as I
recall", "it is well known that". Each of those is a place where a document
could have settled it and you did not go and look.

### 2. Fact, inference, speculation, kept apart

Three different things, and the analyst needs to see which is which without
reading closely.

- **Fact.** A source says it. Attach the source and the date you fetched it.
- **Inference.** You reasoned to it from stated facts. Show the step, so it
  can be attacked.
- **Speculation.** You think it, and nothing in front of you supports it.
  Worth saying, worth saying clearly.

Never let an inference sit in a list of facts, and never quietly promote
speculation by dropping the hedge in a later paragraph. If a claim moves from
speculation to fact because you found the document, say that it moved.

### 3. Timestamp what you fetched

Dockets move, filings get amended, prices go stale, news is a moving target.
Every retrieved item carries when you retrieved it, in UTC, and the oldest
item in a piece of work is worth calling out. "Docket current as of
2026-07-30 14:20 UTC" tells the analyst whether to refresh before acting.
"Docket shows" tells the analyst nothing.

### 4. A citation you did not look up is unverified

Case citations are the single easiest thing to get plausibly, confidently
wrong. Reporter volumes, page numbers, years, and party names all recombine
into cites that read perfectly and do not exist.

So: any case you name gets looked up through the CourtListener citation
lookup, and any case you did not look up is labelled **unverified** in the
output. Left in view, with the label attached, so the analyst can see at a
glance which cites carry weight.

Resolving a citation proves the case exists and that the reporter reference
points at it. It does not prove the case says what you claim it says, and it
does not prove the case is still good law. Those are separate claims that
need their own evidence.

### 5. Quote only what the source says

A quotation is a promise that those characters appear in that document, in
that order. Check it against the fetched text rather than against your memory
of the fetched text. Normalising whitespace or a curly quote is fine.
Tidying grammar, tightening wording, or merging two sentences is not a quote
any more; make it a paraphrase and drop the quotation marks.

Where a holding is being characterised rather than quoted, say
"the court held", give the pin cite if you have it, and keep the
characterisation to what the passage in front of you supports.

### 6. State the coverage limits

An empty search result is not the same as nothing existing, and the analyst
cannot tell the difference from the outside. So say what was not looked at.
The standing limits of this desk:

- **No good-law or citator check.** Nothing here tells you a case was
  overruled, distinguished, superseded, or vacated. A lawyer reads every cited
  case before it is relied on.
- **Federal dockets only**, through CourtListener and RECAP. State trial
  courts are largely absent unless a commercial source such as Trellis has
  been added. A state court matter can be invisible here and very real.
- **RECAP is a contributed archive.** A document missing from it may simply
  never have been purchased and uploaded.
- **EDGAR full-text search reaches back to 2001** and covers filed documents
  only. Exhibits, correspondence, and pre-2001 material need a different path.
- **No price or return figures** unless a price source was actually queried in
  this session. A remembered move around a catalyst is not data.
- Not legal advice. Not investment advice.

Write the limits that bit on this piece of work, and keep it short. Three
lines of honest scope beats a page of boilerplate nobody reads.

### 7. Say what you searched

The searches that came back empty are findings. Record the queries you ran,
where you ran them, and what came back, so a later session does not repeat
the dead ends and so the analyst can spot the query you should have run.

## Reporting honestly

Good:

> Confirmed: three of four cites resolve. *Kahn v. M&F Worldwide*, 88 A.3d 635
> (Del. 2014), fetched 2026-07-30. The fourth, cited to 214 A.3d 210, returns
> no match; labelled unverified in the memo. No good-law check on any of them.

Not good:

> All citations verified.

The second sentence takes less space and tells the analyst something false.
When a check did not run, the honest report is that it did not run. When a
check failed, the failure is the most useful line in the output.
