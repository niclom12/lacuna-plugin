---
name: memo-house-style
description: Writing or revising a litigation research memo under cases/. Use when producing, filling or editing a memo file, choosing section order or headings, applying source tags, deciding what belongs in verified facts versus inference versus speculation, or stating any probability, confidence or base rate about a legal or market outcome. Covers the fixed memo skeleton the lacuna verifier regexes on, the seven source tags, the no-silent-supplement rule, confidence discipline (reference class, decision point, what would change my mind), the question-as-posed reframing block required for pre-briefing probability requests, provenance classification for user-supplied material, and a rationalization prevention table.
---

# Memo house style

This is the output contract. Section order and section names are non-negotiable because
`bin/lacuna_verify.py` regexes on them. A renamed heading is an invisible failure: the
check that should have fired reports nothing.

## 1. Never retype the skeleton

Run `python3 "$LACUNA" template memo > cases/<case-id>/memo.md`, or Read
`<LACUNA_ROOT>/templates/memo.md` and Write it out literally, then fill the slots. The
session banner prints `LACUNA ROOT: <absolute path>` and `.lacuna/plugin-root` holds the
same value, so the root never has to be guessed. Either route injects the skeleton
deterministically. Recalling headings from memory is how section names drift.

Sections, in this order, all required:

`## Situation`, `## Thesis`, `## Verified facts`, `## Inference`, `## Speculation`,
`## Rejected and unverified claims`, `## Catalyst calendar`, `## Price evidence`,
`## Counter-evidence`, `## Falsification conditions`, `## Provenance`,
`## What was searched`, `## Action items`, `## Coverage limits`.

Frontmatter keys, all required: `case_id`, `subject`, `litigation_class`, `tickers`,
`status`, `distribution`, `contains_nonpublic`, `generated_by`, `model`, `operator`.

Header lines below the frontmatter: `As of:`, `Oldest source used:`,
`Case-law verification:`, then the citation caveat paragraph. Leave `As of:` and
`Oldest source used:` for the verifier to write from the retrieval ledger. Writing your
own timestamp there and being more than 60 seconds off blocks the memo.

The footer legend stays verbatim. If it is missing the verifier re-inserts it and reports
the omission.

## 2. What goes where

| Section | Admits | Refuses |
|---|---|---|
| `## Verified facts` | A fact, a source tag, a resolvable ledgered URL, a retrieval date, all on the same line | Anything you did not fetch this run, and any record of a search having been run. See section 4 |
| `## Inference` | Reasoning from the lines above, stated as reasoning | Any premise drawn from an unverified citation |
| `## Speculation` | Explicitly unsupported reading, labelled as such | Anything a reader could mistake for a finding |
| `## Rejected and unverified claims` | Every citation that did not resolve, every claim that could not be sourced | Nothing here may be used as a premise anywhere above |
| `## Provenance` | Every user-supplied claim or document, classified | An unclassified item |

The fact / inference / speculation split exists so a non-technical reader gets a visual cue
about which paragraphs they are allowed to act on. Blur it and the memo loses its only
safety affordance.

## 3. Source tags, never stripped

Every factual line in `## Verified facts` carries one of:

`[CourtListener]` `[SEC EDGAR]` `[GDELT]` `[market data]` `[web, verify]`
`[model knowledge, UNVERIFIED]` `[user provided]`

Rules:

- `[web, verify]` marks an untrusted host. It may never appear in `## Verified facts`.
- `[web, verify]` applies only to material the main session supplies, since the
  case-researcher agent has no web tools at all. The main session's own web access is held
  to the approved hosts by the pre-tool allowlist, so in the normal research flow this tag
  does not come up.
- `[model knowledge, UNVERIFIED]` may appear only in `## Speculation` or
  `## Rejected and unverified claims`.
- `[user provided]` requires a matching `## Provenance` entry.
- A line with a source tag and no URL is not a verified fact. Move it or source it.
- **A docket citation uses the public permalink**
  `https://www.courtlistener.com/docket/<id>/<slug>/`, which `court docket` prints on its
  `url:` line. Never cite the `/api/rest/v4/...` address the tool fetched. The API address
  returns 401 to any reader without a CourtListener token, so a memo built on it is a memo
  whose sources nobody outside this desk can open. Check C5 reads the docket id straight out
  of the permalink path, so the readable form provenances exactly as well.

## 4. The no-silent-supplement rule

When a tool returns thin results, state the result count and stop.

> `court search` for Section 220 demands returned 2 results.

**A search-outcome sentence never goes in `## Verified facts`.** "A search for X returned 0
results", "the lookup found nothing", "no opinion matched" and every rephrasing of them are
records of what this desk did rather than facts about the world, and `## What was searched`
is generated by the tool from the retrieval ledger and is the only place a search is
recorded. If the search concerned a citation that did not resolve, the citation itself goes
in `## Rejected and unverified claims`, naming it nowhere else. Check C3 blocks the case name
in `## Thesis`, `## Verified facts` and `## Inference` in any phrasing, negative phrasing
included, because a reader skimming the verified section carries the name away as something
this desk confirmed.

Never fill the gap from memory, and never widen the claim to cover the gap. A thin search
is a finding about the record. Reporting it honestly is the single feature a non-technical
reader can evaluate at a glance.

If a source failed, the memo says which one and what the failure was: `DATA UNAVAILABLE`,
`RATE LIMITED`, or `NETWORK BLOCKED`. An empty section that reads as "nothing there" when
the truth is "the request failed" is the failure this desk exists to eliminate.

## 5. Confidence discipline

Any estimate of an outcome (percentage, decimal, fraction, or verbal such as "more likely
than not" or "roughly three in four") carries three following lines:

```
Reference class: <what population, with a source tag and ledgered URL>
                 or the literal token [no empirical base rate, judgment only]
Decision point:  <the dated, sourced procedural event this resolves at>
What would change my mind: <a concrete observable>
```

Plus one line naming the estimate's **dominant uncertainty driver**: the single unknown
that moves the number most.

Hard rules:

- A base rate with no source is worse than no base rate. It defeats the reader's
  skepticism. If you cannot cite the population, write
  `[no empirical base rate, judgment only]`.
- An estimate above 0.85 or below 0.15 must name the deterministic event that justifies it
  (a filed stipulation, an entered order, a statutory deadline that has already run).
- There is no house default probability. Anchoring everything near the middle is
  anti-calibration; it hides evidence rather than reporting it.
- Language models are persistently overconfident at the high end and do measurably worse on
  financial questions than on political ones. Assume that applies to you.

## 6. The question-as-posed block

Whenever a probability is requested on a matter that has not been briefed, insert before
the estimate:

```
## Question as posed / question actually answerable
Asked: <their question, verbatim>
Answerable today: <the narrower question the record supports>
Procedural gate: <lead-plaintiff appointment | consolidation | amended complaint |
                  briefing schedule set | hearing held> on <date or "not yet set">
```

"Will this survive the motion to dismiss" is close to unanswerable at filing: there is no
operative complaint, no lead plaintiff, and no briefing. A well-formatted answer to an
ill-posed question is how this desk would produce its most confident wrong output. Reframe
first, then answer the answerable version, and say plainly that the estimate is provisional
until the gate clears.

## 7. Provenance

Every claim or document the user handed over gets a `## Provenance` line:

```
- user-supplied: "<the claim>" <sep> public:<ledgered url> | nonpublic | unknown <sep> used-as: <background|rejected>
```

Use the separator shape shown in `<LACUNA_ROOT>/templates/memo.md`. Classification is mechanical:

- **public** requires a ledgered URL on an allowlisted host that you fetched this run.
- **nonpublic** is anything you know came from a sealed, confidential or internal source.
- **unknown** is the default for anything handed over with no URL, including a pasted
  document. Unknown is not a temporary state to resolve by assuming; it stays unknown until
  someone produces the public filing.

A 6-gram distinctive to a `nonpublic` or `unknown` item may not appear in `## Thesis`,
`## Verified facts`, `## Catalyst calendar` or `## Price evidence`. Restating a user
assertion as a finding is the most common way a memo launders an unsourced claim into a
sourced-looking one.

`contains_nonpublic: true` forces `distribution: internal-only, do not act`.

## 8. Catalyst calendar

Copy the bullet shape from `<LACUNA_ROOT>/templates/memo.md` and fill every slot. An item labelled
`scheduled` requires all four of: the court, a time with an explicit time zone, a source
link, and the quoted docket entry text. Court deadlines are local-time and court-specific;
a bare date under a UTC header silently shifts a 16:00 PT hearing to the following day.

A deadline you computed is `expected` at best. See the `docket-research` skill.

## 9. Price evidence

This build has no price leg. There is no `price` subcommand, no price source, and therefore
no return figure that can be sourced. Leave `## Price evidence` as the DATA GAP line the
template ships with.

Never write `return_0d`, a percentage, or any characterisation of how the stock moved. A
remembered move is a fabricated statistic, and it is the one claim class with the fewest
independent checks on it. The verifier blocks any return or percentage in that section that
no ledgered `price` retrieval backs, which in this build means all of them.

## 10. Rationalization prevention

| The excuse | The answer |
|---|---|
| "I'm confident about this one" | Confidence is not evidence. |
| "I remember this case" | Memory is not a source. |
| "The number is probably right" | Then verify it, or label it. |
| "Different words, so the rule doesn't apply" | Spirit over letter. |
| "The user already told me this" | A user assertion is a provenance item. |
| "It would look thin otherwise" | Thin is a finding. Report the count. |

## 11. Honest limit of the checker

The confidence check is a lint. It catches common shapes: percentages, decimals, fractions,
and a fixed list of verbal hedges near a fixed list of outcome verbs. It will miss a novel
phrasing. Passing the lint is not evidence that the estimate is calibrated, so the analyst
still reads the section. Say so in the memo when it matters.
