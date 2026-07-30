---
name: earnings-analysis
description: "Use when asked for an earnings update, a post-earnings note, a quick take on a quarter, what changed in the new 10-Q, or how a result affects an existing view. Reads a quarterly result as a tradeable event for a company the desk already follows. Covers checking that you have the actual latest quarter rather than a remembered one, leading with the beat or miss and quantifying it, reading guidance changes, and the litigation reads that only a fresh quarterly filing gives you: how the contingencies note moved since last quarter, new matters appearing in Item 3, restatement and non-reliance signals, and auditor changes. Every filing it needs comes through a plain fetch, so it works in Cowork and in Claude Code alike."
---

<!-- Adapted for lacuna from anthropics/financial-services (Apache-2.0),
     plugins/agent-plugins/earnings-reviewer/skills/earnings-analysis/
     (SKILL.md, references/best-practices.md, references/workflow.md).
     Licence text: licenses/APACHE-2.0.txt
     Changes: markdown output instead of docx and chart packs, no Bloomberg or FactSet
     consensus dependency, page and word targets dropped, and a litigation-delta
     section added because that is why this desk reads a 10-Q at all. -->

# Earnings analysis

A quarter is a scheduled event with a filing attached. For this desk it does two things: it
moves the price, and it forces the company to restate its legal exposure in writing. The
second is usually the more valuable half and it is the half most notes skip.

Short note, markdown, published while it still matters. Assume the reader already knows what
the company does. Write the file into the working folder beside the rest of the matter's
material, which works the same way in Cowork and in Claude Code.

Everything this note needs arrives through a fetch. Nothing here requires a terminal.

**Read the desk profile first.** If `desk-profile.md` is in the working folder, open it and
follow it: it carries what counts as verified for this analyst, distrusted sources, note length
and hedging taste, how probabilities get expressed, and pet peeves. In Claude Code the same
profile sits in a fenced `lacuna desk profile` block in `~/.claude/CLAUDE.md` and loads by
itself. In Cowork nothing loads it for you, so opening the file is what makes it apply.
`/lacuna:interview` is what writes it.

## Before anything else, confirm the quarter

The most common failure is analysing a quarter from memory. Model training data goes stale,
and a confident writeup of last year's results is worse than no writeup.

1. Note today's date explicitly.
2. Pull the filings list and find the newest 10-Q or 10-K, and the 8-K that carried the
   release. The `edgar-research` skill has the recipe, Recipe 2, and it gives both a
   fetch-tool form that works anywhere and a terminal form that is Claude Code only. Use
   whichever your environment offers.
3. Check the filing date against today. If the newest result is months old, the company has
   not reported yet and there is no note to write.
4. Write the filing date and accession number into the note before writing anything else.
5. If the filings list could not be retrieved at all, stop and say so. A quarter you could
   not confirm is not a quarter you can write about, and "the submissions endpoint was
   unreachable this session" is the honest version of that.

## Lead with the result

- **Beat or miss in the first sentence.** The reader decides whether to keep reading from
  that line.
- **Quantify it.** "Revenue of $1.24bn, $38m or 3% above the guided range midpoint" tells
  the reader something. "Strong quarter" does not.
- **Explain why.** A number that moved has a driver. Segment mix, pricing, a one-off, a
  charge. Name it and cite where you found it.
- **Consensus is paid data.** If the desk has no licensed consensus figure, do not invent one
  and do not lift one from memory. Compare against the company's own prior guidance, which is
  filed and quotable, and say plainly that the note is measured against guidance because
  consensus was unavailable. An unquantified beat honestly labelled beats a fabricated one.
- **Headline the takeaway.** "Q2: services beat offsets hardware miss, contingency range
  doubles" earns its line. "Q2 Earnings Update" does not.

## The litigation delta

This is the section this desk exists for. Open the new filing beside the prior quarter's and
read for movement.

| Where | What you are looking for |
|---|---|
| Contingencies note | A new accrual, a widened or narrowed range of reasonably possible loss, or a phrase change between "cannot be estimated", "reasonably possible" and "probable and estimable" |
| Item 3, Legal Proceedings | Matters appearing for the first time, matters quietly dropped, a changed procedural description |
| 8-K item 4.02 | Non-reliance on previously issued financials. The company saying its own numbers were wrong. Treat this as the strongest single signal in the set. |
| 8-K item 4.01 | A change of auditor, especially near a restatement or a disclosure change |
| Risk factors | New or materially rewritten language, which often lands one quarter before the matter itself is disclosed |
| Going concern and subsequent events | Where a matter too new for Item 3 first surfaces |

Quote both quarters when the language moved, and give both accession numbers on the same
lines as the quotes. A phrase change is the finding, so the reader needs to see both phrasings
to agree with you.

If nothing moved, say that. "The contingencies note is unchanged from the prior quarter
(accessions X and Y)" is a real result and it is worth knowing.

## Guidance and estimates

- If the company guides, analyse the guide. Old range against new range, and what management
  said about the change.
- If the company withdrew or declined to guide, that is itself the story. Say it.
- When you revise your own view, show old and new side by side with the reason. A revised
  number without a reason is unreviewable.
- If a revision is large enough to move your valuation, update the valuation in the same
  note. Leaving them inconsistent creates two views of one company.

## Note structure

1. **Headline and the take.** Two or three sentences. Beat or miss, quantified, and what it
   does to the view.
2. **The numbers.** One compact table of the metrics that matter for this company, current
   quarter against prior year and against prior guidance. Five to ten rows is plenty. Leave
   the full profit and loss statement in the filing where the reader can find it.
3. **What drove it.** Segment or driver level, with the filing cited.
4. **The litigation delta.** As above. Quote the movement.
5. **Guidance.** Old against new, with management's stated reason.
6. **View.** Unchanged, strengthened or broken, and what would change it next.
7. **Sources.** Release, 10-Q or 10-K, and the 8-K, each with accession number and link.

## Citations

Same rule as everywhere on this desk. Every figure names the document it came from, and every
SEC document gets its archive link.

```
Source: Q2 FY2026 10-Q filed 2026-05-08, accession 0001234567-26-000112.
https://www.sec.gov/Archives/edgar/data/1234567/000123456726000112/xyz-20260331.htm
```

The earnings call transcript is often useful and is often behind a paywall. Where you use
one, name the provider and the date. Where you could not get it, say the call was not
reviewed rather than characterising what management said on it.

## What this note never contains

- A quarter you did not fetch, or a metric from a remembered version of the filing.
- A figure attributed to a filing whose fetch was refused. A blocked endpoint gets named as
  blocked.
- A consensus number with no licensed source behind it.
- A beat or a miss with no denominator, so the reader cannot tell whether 3% or 30% moved.
- Two pages explaining what the company does. That belongs in the research note.
