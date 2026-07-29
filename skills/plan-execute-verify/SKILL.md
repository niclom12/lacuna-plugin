---
name: plan-execute-verify
description: Use when starting research work of any size, to size the stakes before doing the work. Sorts the request onto one of three rungs (quick lookup, standard research, high-stakes where money moves on the answer) and sets the matching amount of planning and verification for that rung. Also covers escalating a task up a rung part-way through, when a lookup turns out to be load-bearing.
---

# Plan, execute, verify

Verification is a dial the analyst sets. Turning it to maximum for every
question wastes the analyst's time and yours; leaving it at minimum for a
question with money on it is how a bad number reaches a decision. So the first
move on any substantive task is to say out loud which rung it sits on, and why.

State it in one line before starting. The analyst can move it.

> Reading this as a quick lookup: one figure, low stakes, I will answer
> directly and sanity-check it. Say the word if it deserves more.

## The three rungs

### Rung 1: quick lookup

A single fact, a date, a case name, a ticker, one docket entry. Nobody trades
off it on its own.

- **Plan:** none. Answer directly.
- **Thinking:** cheapest that will do the job. Do not think hard about
  whether the Southern District of New York is in New York.
- **Verify:** self-check before sending. Did the source actually say this?
  Is the date the one on the document rather than the one you expected? Give
  the answer with its source attached so the analyst can see where it came
  from in one glance.

### Rung 2: standard research

The default rung. A docket read, a filing walk-through, a short memo, a
"what is going on with X" question that takes several searches.

- **Plan:** a short one first, three to six lines. What you will search, in
  what order, and what would make you stop. Show it, then go, without waiting
  for approval unless the analyst likes to see plans.
- **Execute:** the plan, adjusting as sources surprise you. Say when you
  depart from it.
- **Verify:** a checking pass at the end. Resolve the links, look up the
  citations, confirm the dates against sources. Mechanical and boring on
  purpose, and every item is a yes or a no rather than a judgement:
  - Does every link in the output resolve? Fetch them, do not eyeball them.
  - Does every case cited exist? Look each one up through the CourtListener
    citation lookup. A citation you did not look up is unverified and gets
    labelled that way.
  - Is every date taken from a source, rather than from memory or inference?
  - Is every quoted string present verbatim in the document you fetched?
  - Are the coverage limits stated, so absence of evidence does not read as
    evidence of absence?

  Report the pass in two or three lines. "Six links, six resolve. Three
  citations, three confirmed. One date I could not source, flagged in the
  memo." That report is the product as much as the memo is.

### Rung 3: high stakes, money moves on it

A position, a sizing decision, anything going to a third party, anything where
being confidently wrong is expensive.

- **Plan:** written, and reviewed with the analyst *before* execution. The
  analyst knows things about the trade that are not in any document. Ask what
  they already believe and what would change their mind, then plan against that.
- **Execute:** the agreed plan. Flag material departures as they happen.
- **Verify, twice over:**
  1. The full checking pass from rung 2.
  2. An **independent re-derivation**. Dispatch a fresh subagent with no view
     of your reasoning. Give it the question and the sources, ask it to derive
     the two or three load-bearing claims itself, and compare. Where it
     disagrees, or where it cannot get there from the sources you had, that is
     the finding. Report the disagreement even when you still think you were
     right.

  A fresh context is the point. An agent that has read your working will
  agree with your working.

## Precedence: rungs and habits

The rung that `plan-execute-verify` names decides how much of
`verification-habits` applies. Rung 1 quick lookups get the labelling habits
only: fact kept apart from inference and speculation, an unverified tag on any
citation that was not looked up, and no claim without a source. They skip the
full lookup pass. Rungs 2 and 3 apply every habit in `verification-habits` in
full, and that skill is the rung-2 checking pass. Say the rung out loud either
way, so a habit that was skipped is visible rather than quietly dropped.

## Escalating mid-flight

Rungs are a starting guess, and the work tells you when the guess was wrong.
Move up, say so, and say why:

> This started as a quick lookup, but the answer turns on which subsidiary
> filed, and you mentioned you are sizing on it. Treating it as high stakes:
> here is the plan before I go further.

Escalate when any of these show up:

- The analyst mentions a position, a size, or a deadline.
- The answer rests on one source and that source is thin, stale, or secondary.
- Two sources disagree and the disagreement changes the conclusion.
- You catch yourself writing "presumably", "likely", or "should be" in a place
  where a document could settle it.
- The output is leaving the desk, going to a client, a counterparty, or a
  lawyer.

De-escalating is allowed too, and cheaper than pretending. If a high-stakes
question collapses into one already-verified fact, say so and hand it back
rather than performing a research project around it.

## What this is not

This is not a gate and nothing here blocks. Nothing checks up on you. The
practice is worth something only because the analyst can see which rung you
picked and can overrule it, so always say the rung out loud, and never claim a
verification pass you did not run.
