---
description: A conversational interview about how you work, roughly ten minutes, then writes what it learned into your global CLAUDE.md so every future session already knows your standards.
model: sonnet
---

# Interview the analyst

Your job in this conversation is to learn how this person works, then write it
down somewhere durable so no future session has to ask again.

Two rules for the conversation itself:

1. **Keep it conversational.** Ask one thing at a time. React to what you hear.
   Follow the interesting answer sideways before moving on. If you get a story
   instead of an answer, the story is the answer, so mine it. Never present a
   numbered list of questions and wait for it to be filled in.
2. **Roughly eight to twelve minutes.** Seven areas below. Do not march through
   them in order if the conversation wants a different order, and do not ask
   every follow-up listed. Those are prompts for you to work from, and reading
   them aloud would be tedious. If the answers are coming back short, go faster
   and finish early. If they are enjoyable, let it run.

Open with something like: "I want to learn how you work so I stop guessing.
About ten minutes, and at the end I will write it down so you never have to
explain it twice. First one: think of the last time you decided something was
solid enough to act on. What made it solid?"

Use `AskUserQuestion` only where the answer is genuinely a choice between a few
tastes (memo length, how to express probabilities). Everything else is open
prose. Never present a wall of multiple-choice questions.

## The seven areas

The questions below are phrased the way you would ask them.

**1. What "verified enough" means.**
How do you decide a claim is solid enough to act on? Do you need the primary
document, or is a reliable secondary report enough? When have you been burned by
something that looked verified? Do you want to see the verification work, or just
the conclusion with sources attached? What should never be asserted without a
document behind it?

**2. Sources trusted and sources distrusted.**
Which publications, filings, data vendors, and people do you take at face value?
Which do you discount, and why? How do you treat a company press release against
a court filing against a sell-side note against a message board? Is there a
source you want flagged every time it is cited?

**3. What deserves a deep dive versus a quick read.**
What kinds of question do you want answered in two lines? What kinds do you want
a full workup on? What signals that something is worth hours? Where has an
analyst wasted your time with depth you did not need? Ask for one example of
each, since the examples calibrate better than the principle.

**4. Memo length and hedging taste.**
How long should a normal writeup be? One screen, two pages, a paragraph with
links? Conclusion first or reasoning first? How do you feel about hedging: does
careful qualification read as honesty or as cowardice? What should happen to a
claim that is probably true but unproven, buried in a caveat or promoted with the
caveat attached?

**5. Standing interests.**
What are you watching right now, and what are you always watching? Venues (which
courts, which exchanges, which prediction markets), sectors, specific tickers,
specific cases or dockets, named companies, named judges, recurring event types.
Ask which of these are permanent interests as opposed to this month's file, and
record the difference.

**6. Pet peeves.**
What makes you close a document immediately? Filler openings, hedge-everything
prose, jargon, bullet soup, false confidence, fake enthusiasm, being asked to
approve things you already approved, being told what you just said? Ask directly:
"what do assistants do that annoys you?" The answer is usually specific and
usually the most useful thing in the whole interview.

**7. How probabilities should be expressed.**
Numbers, ranges, words, or odds? Is "likely" a useful word or a meaningless one?
Should a base rate be quoted whenever one exists? Do you want a confidence figure
attached to a claim, or is that false precision? Ask which of these reads better:
"roughly 30%, mostly on the timing risk", "unlikely", or "2 to 1 against".

Along the way, if a workflow habit, a naming convention, a folder where things
are kept, or a person the work goes to comes up, capture that too. It goes in a
"working notes" line.

One small factual item to slip in wherever it fits, rather than making a moment
of it: the address to send to SEC EDGAR as the contact in the `User-Agent`
header. Ask for it plainly, with the one-line reason, which is that EDGAR returns
403 to anonymous clients and a made-up address is worse than none. It is not a
secret and it is not a login, so a work address is the usual answer. If the
answer is no, drop the field and the EDGAR skill will ask when it first needs
one.

## Then write it down

The interview is worth nothing if it lives only in this conversation. Write it
into the **global** memory file so it applies in every project, on every repo, in
every session.

**Step 1. Read the existing file first.** Read `~/.claude/CLAUDE.md`. If it does
not exist, you will create it with just the block below. If it does exist, read
all of it before writing anything. There is other content in there that matters
and it is not yours to touch.

**Step 2. Get today's date, then write the fenced block.** The block carries a
date stamp, and your own sense of the date is not evidence. Read it from the
environment before writing: run `date -u +%F`, or take it from the session
context if that already states today's date. Never write a remembered date into
someone's permanent config.

The section is delimited by these exact marker lines:

```
<!-- BEGIN lacuna desk profile -->
## Lacuna desk profile

_Written by `/lacuna:interview` on <YYYY-MM-DD>. Edit this freely; re-running
the interview replaces everything between the markers and nothing outside them._

**Verified enough:** <what has to be true before a claim counts as solid>

**Trusted sources:** <list>

**Distrusted or flag-on-sight sources:** <list>

**Deep dive versus quick read:** <the rule, with an example of each>

**Memo shape:** <length, conclusion-first or reasoning-first, hedging taste>

**Probabilities:** <how to express them, base rates, confidence figures>

**Standing interests:** <venues, sectors, tickers, cases, permanent ones marked>

**Current file:** <what is on the desk this month, if it was named>

**Pet peeves:** <list, in their words where possible>

**Working notes:** <habits, conventions, folders, who work goes to>

**SEC contact email:** <the address to send as the EDGAR User-Agent contact>
<!-- END lacuna desk profile -->
```

Fill it with the actual answers, in their words where you can, in plain prose.
Short is fine. A line the analyst recognises as their own is worth more than
three lines of your paraphrase. Drop any field there was nothing to say about
rather than padding it.

**Step 3. Place it idempotently.**

- If both marker lines are already present in the file, replace only the text
  between them, markers included, and leave every other byte of the file
  exactly as it was. Do not reorder, reformat, or reflow the surrounding
  content.
- If both markers are absent, append the block to the end of the file with one
  blank line before it.
- If exactly one of the two markers is present, stop. A half-written or
  hand-trimmed section is not something you can safely guess the boundary of.
  Show the marker line you found, say which one is missing, and ask whether to
  treat the rest of the file as profile text to replace or to repair the missing
  marker by hand first.
- If either marker is present more than once, or the END marker appears before
  the BEGIN marker, stop. Do not guess. Show the confusing lines and ask which
  block to replace.
- Never delete or rewrite content outside the markers, and never replace the
  whole file with your own version of it. Do the write as a targeted string
  replacement of the old marked section (`Edit`, old string starting at the
  BEGIN marker and ending at the END marker) or as an append. Never a
  whole-file `Write`, because that puts every other byte in the file at the
  mercy of your recollection of it.

**Step 3b. Confirm you broke nothing.** Read the file back. Check that the
content above the BEGIN marker and below the END marker is byte-identical to what
you read in Step 1, and that the file still ends where it should. If anything
outside the markers moved, say so plainly and restore it from what you read in
Step 1 before going on. Only report the profile as written once this check
passes.

**Step 4. Offer the project-level copy, with the warning attached.** Ask whether
the block should also go into the current project's `./CLAUDE.md`, which is
useful when a project has its own narrower conventions. Say the thing that is
easy to miss before writing anything: `./CLAUDE.md` is usually tracked in git and
shared with everyone else working on the repo, so a profile written there means
personal preferences, distrusted sources, and standing positions can be committed
and pushed. Check first and report what you found: `git ls-files --error-unmatch
CLAUDE.md` succeeding means the file is already tracked, and `git check-ignore -q
CLAUDE.md` succeeding means it is ignored and safe. Then ask. If the answer is
yes, write the same block into that file under the same markers, following the
same idempotency rules; if the project file does not exist, creating it is fine.
If the answer is no, leave it, and say that the global file covers every project
anyway.

## Close

Two sentences summarising what you learned, in your own words, specific enough
that the analyst can tell whether you were listening. Something like: "So:
primary documents or it does not count, memos short with the answer at the top,
probabilities as numbers with the driver named, and never open a message by
telling you what you just asked. Standing interests are Delaware Chancery,
appraisal cases, and anything touching the two tickers you named."

Then point onward: "That is saved to your global CLAUDE.md, so it applies
everywhere from now on. Edit it whenever it stops being true. If you have not run
`/lacuna:start` yet, that is the five-minute tour of what this desk can actually
do."
