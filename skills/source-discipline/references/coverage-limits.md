# Coverage limits, one page

What this desk can see, what it cannot, and what each gap means for a memo. Written for a
reader who is not a lawyer and not technical.

---

## The four sources

| Source | What it is | Window | Costs |
|---|---|---|---|
| CourtListener and RECAP | Federal court dockets and opinions, contributed and archived | Opinions go back to the founding. Docket entries only exist where a user has contributed them. | Free. A free token unlocks citation checking. |
| SEC EDGAR | Every filing a US public company makes | Full text from 2001. Archives older. | Free. Requires a real contact email. |
| GDELT | Worldwide news index | About 90 days | Free |
| price data | none in this build | nothing | There is no price leg. `## Price evidence` reports a DATA GAP and no return figure may be written |

---

## What is outside coverage

| Gap | What it means in practice |
|---|---|
| **State trial courts** | Every state. Delaware Superior, New York Supreme, California Superior. A matter there returns nothing, and the nothing means "not covered". |
| **Sealed and redacted docket entries** | Visible as an event with a date. Contents unavailable, and inference about them is forbidden. |
| **PACER entries nobody contributed** | RECAP is crowd-sourced. A docket may show 12 entries here and 200 on PACER. Thin dockets are common and must be reported as thin. |
| **EDGAR full text before 2001** | Searchable coverage starts in 2001. Older filings exist and are reachable by accession number, and cannot be found by searching their text. |
| **PDF and image exhibits** | Frequently unparsed. A quote from one carries `[quote not machine-checked, PDF source]`. |
| **Private companies, most foreign issuers** | Not in EDGAR. Absence from EDGAR is not absence of the event. |
| **News older than about 90 days** | Outside the GDELT window. Say so rather than reporting no coverage. |
| **Paywalled outlets** | Not indexed. |
| **Whether a case is still good law** | No free citator exists anywhere. Not checked, ever. |
| **Whether a case supports the point it is cited for** | No tool checks this. A lawyer reads the case. |
| **Prediction markets, order placement, position sizing** | Deliberately out of scope. This desk produces research and a human places every order. |

---

## The two checks that do exist, and exactly what they prove

**Citation existence.** `court cite` proves a reporter citation resolves to a real case in
CourtListener's database. It proves nothing about whether that case says what the memo says
it says.

**Docket identity.** `court docket` proves a docket number exists, and returns the court, the
caption, the assigned judge and the parties. This is the check that catches the most common
fabrication in this workflow, because a recently filed case has no reporter citation at all
and citation checking is structurally blind to it.

---

## How failures are worded

Six distinct outcomes. Only one of them means nothing was found.

| Wording in the memo | Meaning |
|---|---|
| `0 results` with the query printed | The search ran and matched nothing. |
| `outside coverage` | The thing may exist. This source cannot see it. |
| `DATA UNAVAILABLE` | The source returned something unexpected or unreadable. |
| `RATE LIMITED` | Throttled. Retry after the stated wait. |
| `NETWORK BLOCKED` | The network is intercepting secure connections. There is a fix. |
| `AMBIGUOUS` | More than one match. Candidates listed. A human picks. |

If a section of a memo is empty and none of these words appear, something went wrong
silently. Ask.

---

## The one-sentence version

This desk can prove that a case exists, that a docket exists and who is on it, that a filing
exists and what it actually says, and how a stock moved around a date. It cannot prove that
a case is still good law, that a case supports an argument, or that a state trial court
matter does or does not exist.
