# Desk profile

Written by `/lacuna:setup`. Shared, diffable, reviewable. Every field below
is marked as unfilled until setup writes a real value into it, and every lacuna
data command refuses to run while any field is still unfilled.

To change anything here, either edit this file directly or re-run
`/lacuna:setup`, which is idempotent.

## Operator
- Contact email: [PLACEHOLDER]
  Sent to SEC EDGAR as the User-Agent on every request. SEC requires a real
  contact. This is not a secret and it is not a login.

## Venues that matter to this desk
The two venues chosen at setup. Research prioritises these angles first.

- Primary venue: [PLACEHOLDER]
- Secondary venue: [PLACEHOLDER]

Chosen from: Delaware Chancery, ITC Section 337, PTAB, agency enforcement,
FDA, EU and UK, bankruptcy, securities class actions.

## Tickers and sectors already watched
- Tickers: [PLACEHOLDER]
- Sectors: [PLACEHOLDER]

## Restricted names
Names this desk must not research or trade. A hit on either list blocks the
memo with "restricted name, escalate to compliance" and appends a line to
`.lacuna/restricted-hits.jsonl`. Re-asked on every setup run.

- Restricted tickers: [PLACEHOLDER]
- Restricted parties: [PLACEHOLDER]

## Calibration
Filled in after the first `/lacuna:research` memo, from two questions about
that memo. These two lines are the only fields that stay unset after setup,
so they carry a different marker and never gate the tools.

- Memo length preference: [not yet calibrated, answered after the first memo]
- Hedging preference: [not yet calibrated, answered after the first memo]

## Notes
Anything else the desk should know: house conventions, counsel contacts,
standing exclusions. Free text, read by the research agent as background.
Setup asks nothing for this section, so `none` is the correct starting value.

- none
