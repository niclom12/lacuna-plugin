---
name: equity-research
description: Use when asked to research a company, build or refresh a view on a ticker, work out what a business actually earns and what a lawsuit could cost it, size the exposure in a legal matter against the company's own numbers, assess management or competitive position, or sanity-check what a stock is worth. Writes a company research note in markdown for a name the desk is trading around a legal event. Covers the note structure, where each fact comes from, the rule that every claim about a company links to the filing it came from, and how to size a valuation without a spreadsheet or a paid terminal. Every source it draws on is reachable by a web fetch or a bundled connector, so the note can be built in Cowork or in Claude Code.
---

<!-- Adapted for lacuna from anthropics/financial-services (Apache-2.0),
     plugins/vertical-plugins/equity-research/skills/initiating-coverage/
     (SKILL.md, references/task1-company-research.md, references/task3-valuation.md).
     Licence text: licenses/APACHE-2.0.txt
     Changes: markdown output instead of xlsx/docx/charts, no paid data platforms,
     scope narrowed to companies the desk is trading around a legal event, and every
     factual claim now has to name the filing it came from. -->

# Equity research

A research note here answers one question: if this legal matter goes badly, what does it
cost, and does the price already reflect it. Everything in the note serves that question.
The full institutional initiation format is a six-week product for a different desk. This
is a working note that a person reads in ten minutes and can act on.

Output is a markdown file. No spreadsheet, no deck, no chart pack. Write it into the working
folder, one file per name, so it sits beside the desk profile and the rest of the matter's
material. That works the same way in Cowork and in Claude Code.

**Read the desk profile first.** If `desk-profile.md` is in the working folder, open it and
follow it: it carries what counts as verified for this analyst, distrusted sources, note length
and hedging taste, how probabilities get expressed, and pet peeves. In Claude Code the same
profile sits in a fenced `lacuna desk profile` block in `~/.claude/CLAUDE.md` and loads by
itself. In Cowork nothing loads it for you, so opening the file is what makes it apply.
`/lacuna:interview` is what writes it.

## Where the facts come from

Almost everything you need is free.

| Fact | Source |
|---|---|
| What the business does, segments, customer concentration | 10-K Item 1 |
| What management admits could go wrong | 10-K Item 1A risk factors |
| Revenue, margins, cash, debt | 10-K and 10-Q financial statements |
| The legal matters and any accrual | 10-K Item 3 plus the contingencies note |
| Management background, pay, ownership | DEF 14A proxy |
| Events since the last annual report | 8-K stream |
| Who owns it and who turned active | 13D, 13G and their amendments |

The `edgar-research` skill has the endpoints and the fetch recipes. Use it rather than
guessing URLs. Each recipe there names the URL first and then gives two ways to reach it, a
fetch-tool form that works anywhere and a terminal form that is Claude Code only, so a note
can be built in either environment. Nothing in this skill needs a terminal of its own: the
filings arrive through a fetch and the note is a markdown file you write.

If a filing could not be retrieved, whether the endpoint refused the fetch or the document
does not exist, the note says which of those two it was and names the document it wanted.
That is a line in the note rather than a reason to leave the claim unsourced.

Court-record facts come through the `docket-research` skill, which reaches CourtListener as a
connector. That is available in both environments too, so the note never depends on a
Claude Code-only path for its legal half.

Company websites, investor presentations and press coverage fill in colour. Label them as
company-sourced when you use them, because an investor deck is marketing with a compliance
review, and its numbers are chosen.

## Citation discipline

**Every factual claim about the company links to the source it came from.** Not a form type,
not "per recent filings". The actual document.

```
Revenue was $1.42bn in FY2025, up 8% (10-K filed 2026-02-18, accession
0001234567-26-000045, consolidated statements of operations).
https://www.sec.gov/Archives/edgar/data/1234567/000123456726000045/xyz-20251231.htm
```

Three habits carry this:

1. **Fetch before you write.** If the document was not retrieved, the note says
   "unverified" and names what would settle it. A plausible sentence with no filing behind
   it is the one thing this desk cannot ship.
2. **Numbers come from the filed statements themselves.** A figure taken from a press
   release, a summary table or your own recollection gets checked against the statement in
   the filing before it goes in.
3. **Estimates are labelled as yours.** Anything you calculated says so, and shows the
   inputs, so the reader can disagree with the assumption rather than the arithmetic.

If a claim cannot survive a reader clicking through to the source, it does not belong in the
note.

## Note structure

Roughly 1,500 to 3,000 words. Sections earn their length by carrying information.

**1. The view** (150 words). What you think and why, up front. The legal matter, what a bad
outcome costs, whether the price looks like it knows. If the note is inconclusive, say that
here rather than at the end.

**2. The legal matter** (300 to 600 words). What is alleged, who is suing, where, and where
it stands. Quote the company's own characterisation from Item 3 or the relevant 8-K, with
the accession. The court record is the other half of this picture, so use the
`docket-research` skill for it and point at that work here rather than repeating it.

**3. What the exposure is worth** (200 to 400 words). Set the claimed or plausible damages
against numbers the company itself reports: annual revenue, operating cash flow, net cash,
and any accrual already taken. A $400m claim against a company with $2bn of net cash is a
different trade from the same claim against one with a covenant test next quarter. Say which
of these numbers is filed and which is your estimate.

**4. The business** (400 to 700 words). How it makes money, the segments and their growth,
customer or geographic concentration, and the two or three drivers that actually move
earnings. Skip the history lesson unless the history is the fact pattern.

**5. Management and ownership** (150 to 300 words). Who runs it, how long they have been
there, insider ownership, and any departure whose timing matters. One tight paragraph per
person who is relevant to the matter beats four full bios.

**6. What breaks the view** (200 to 400 words). Three to six specific risks, each one a thing
that could happen rather than a category. "The class survives the motion to dismiss and the
range in the contingencies note doubles" is a risk. "Litigation risk" is a heading.

**7. Price and valuation** (200 to 400 words). See below.

**8. Sources.** Every filing cited, with accession numbers and links. This section is the
receipt for the rest of the note.

## Valuation without a paid data platform

You do not need a five-tab model. You need a defensible number and honesty about its width.

- **Anchor on what is filed.** Revenue, EBIT, free cash flow, net cash and share count all
  come out of the last 10-K and 10-Q. Cite them.
- **One multiple, argued.** Pick the measure that suits the business, name the comparable
  companies, and explain why the multiple is where you put it. A ratio with a stated reason
  beats a discounted cash flow with fifteen unexamined assumptions.
- **Scenarios instead of a point.** Three lines: the matter goes away, the matter settles in
  the disclosed range, the matter goes badly. Value each. The spread between them is the
  actual output of the work.
- **Say what is priced in.** Compare the current price against those three. If the market
  already sits at the bad case, that is the finding.
- **Where a number came from a peer, a screen or a press report, say so.** A comparable
  multiple you could not verify is labelled as approximate.

Two things to leave out. Do not produce a discounted cash flow whose assumptions you cannot
each defend in a sentence. Do not attach a precise price target to a case whose outcome
distribution is genuinely unknown; a range with reasoning is more useful and more honest.

## Verification, scaled to the stakes

Match the checking to what rides on the note. The `verification-habits` skill has the
general form of this; the three tiers below are what it looks like for a company note.

- **Quick read for context.** Fetch the last 10-K and the recent 8-Ks. Cite what you used.
  Mark the rest unverified.
- **A note that informs a position.** Every number traced to a filed statement, the
  contingencies note read in full, the 8-K stream walked from the start of the alleged
  period, and one pass re-reading your own note against its sources looking for claims that
  drifted.
- **A note the desk will act on with size.** Add the prior year's 10-K to see what the
  disclosure said before, read the proxy, check the 13D and 13G chain, and have someone else
  click three citations at random.

The final pass is always the same question, asked honestly: which sentences here would I
have to withdraw if the reader opened the filing.

## What this note never contains

- A characterisation of a document that was not fetched.
- A number without a source, including numbers that feel like common knowledge.
- Data behind a paid platform. If the desk does not have a licence for it, the note says
  the figure is unavailable and moves on.
- A sentence resting on a fetch that was refused. A blocked endpoint gets reported as
  blocked, with the document it was going to settle.
- Legal advice, or a prediction dressed as a certainty. The note describes exposure and
  probability, and it never places a trade.
