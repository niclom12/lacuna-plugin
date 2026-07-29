---
name: token-efficiency
description: Use when a research session is long, search-heavy, or running slowly, and when choosing how to spend model capacity on a task. Covers routing planning to the strong model and routine execution to the mid model, pushing noisy searches into subagents so the main thread stays readable, backgrounding long fetches, avoiding re-reads of material already established, and treating the written memo as the durable artifact instead of chat scrollback.
---

# Token efficiency

A research session has a budget: the analyst's attention, the context window,
and money. Spending it well is part of doing the work well. A session that
burns its context on raw search output has no room left to think, and the
thinking is what the analyst is paying for.

## Route the model to the task

Different parts of the same job deserve different horsepower.

| Work | Model | Why |
|---|---|---|
| Framing the question, planning the research, reading a plan back critically, the final judgement call | the strong model | This is where being smarter changes the answer |
| Running the plan: fetching dockets, pulling filings, extracting entries, assembling the memo | the mid model | Competent execution of a defined task |
| One fact, one date, one lookup, one conversion | the cheap model | Nothing here rewards deliberation |

Say the routing out loud once, then get on with it. If the analyst wants
everything on the strong model, that is the analyst's call to make and it is a
reasonable one for high-stakes work.

Reserve extended thinking for genuine ambiguity: conflicting sources, a
holding that cuts both ways, a plan with real trade-offs. Do not spend it on
retrieval.

## Push noisy work into subagents

Some tasks produce far more output than signal. Full-text searches with
hundreds of hits, docket sweeps across many cases, scanning a long filing for
one clause. Run those in a subagent and ask for the distilled result back.

The subagent reads the noise; the main thread receives the finding. Give it a
tight brief: what to look for, what to return, what to ignore, and how long
the answer should be. Ask for sources and timestamps in the return, since you
cannot see what it saw.

This is also how parallelism gets cheap. Four dockets, four subagents, one
consolidated answer, and your main context holds four paragraphs rather than
four hundred entries.

## Background the long fetches

A large filing, a slow archive, a broad sweep: start it in the background and
keep working on something that does not depend on it. Come back for the
result. Waiting in the foreground for a two-minute download costs the analyst
two minutes of nothing happening.

## Do not re-read what is established

Once a fact is in the session with its source and timestamp attached, it is
established. Do not re-fetch the docket to check a date you already wrote
down. Do not re-read a file you just edited to confirm the edit landed.

Two exceptions worth honouring: re-fetch when the source could have moved and
freshness matters to the decision, and re-fetch when you are about to make a
high-stakes claim on a single item. Both are deliberate, and both get said out
loud.

## The memo is the artifact, the chat is not

Chat scrollback is a bad place to keep findings. It gets compacted, it gets
lost when the session ends, and nobody scrolls back through it a week later.

So write the durable thing down as you go. A memo file, a running case note,
a dated file under the case folder. When something is worth keeping, put it in
the file rather than in a longer message. Then later sessions read a short
file instead of reconstructing a long conversation, and the analyst has
something to send to a lawyer.

Same principle for standing preferences: they belong in `CLAUDE.md` where every
session sees them, rather than being re-explained each morning. `/lacuna:interview`
exists to put them there.

## Signs the budget is being wasted

- Raw search results pasted into the main thread.
- The same document fetched three times in one session.
- Long recaps of what was just done, addressed to nobody.
- Findings that exist only in chat messages an hour old.
- The strong model extracting dates from a docket.
- The cheap model deciding whether a thesis holds.
