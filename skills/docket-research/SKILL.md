---
name: docket-research
description: Researching a federal court docket, case or litigation posture. Use when searching CourtListener, reading a docket sheet, identifying which legal angle a matter sits on (cert petitions, oral argument and SG amicus timing, agency proceedings, circuit appeals, antitrust and HSR, DGCL Section 220, bankruptcy, class-action settlement approval), checking whether a case citation resolves to a real case, confirming a docket number and its court and caption, or converting a docket entry into a dated calendar item. Covers the named angles and their timing implications, how to read a scheduling order against a standing order, the sealed-entry rule, and the two refusals about deadlines and filing-type classification.
---

# Docket research

`<LACUNA_ROOT>` is the plugin root. The SessionStart banner prints it as `LACUNA ROOT: <absolute path>` and `.lacuna/plugin-root` holds the same value. Never guess it from a relative path.

## Running the tool

The session banner prints `LACUNA BINARY: python3 "<absolute path>"`. If it is not visible
(for example after a compaction), run `cat .lacuna/bin-path` and use its contents. That
value is `$LACUNA` below. Substitute the resolved absolute path when you issue the Bash
call so the scoped permission rule matches.

Issue one network operation per Bash call, with a generous explicit timeout. CourtListener
is paced at 1200 ms and the pacing lock is shared across subagents, so chaining calls into
one invocation gets the invocation killed mid-sleep.

Exact invocations live in `<LACUNA_ROOT>/skills/docket-research/references/court-recipes.md`.

## The three-angle minimum

A research run makes at least three `court search` calls across **distinct named legal
angles**. Three searches against one angle does not satisfy this. Name the angle in the
memo beside what it returned, including when it returned nothing.

| Angle | What it implies for timing |
|---|---|
| **Cert petitions** | Distribution to conference, then a decision at a scheduled conference date. A CVSG adds six to twelve months and is itself a signal. |
| **Oral argument and SG amicus** | Argument calendars are published a term ahead. An SG amicus invitation is a dated, observable event. |
| **Agency proceedings** | SEC, FTC, DOJ and ITC each have their own clock. An ITC Section 337 target date is set early and moves rarely, which makes it one of the few genuinely schedulable catalysts. |
| **Circuit appeals** | Notice of appeal, then briefing, then argument, then a decision with no deadline. Median time to decision by circuit is the only defensible reference class. |
| **Antitrust and HSR** | Second request timing is observable through company disclosure rather than through the docket. |
| **DGCL Section 220** | Books-and-records demands are fast, in Delaware Chancery, and frequently precede a fiduciary-duty complaint. A Section 220 hit is an early warning. |
| **Bankruptcy** | Plan confirmation, disclosure statement approval and claim bar dates are all dated, all published, and all move. |
| **Class-action settlement approval** | Preliminary approval, notice period, objection deadline, fairness hearing, final approval. The most calendarable sequence in this list. |
| **Securities class actions** | The PSLRA 60-day lead-plaintiff window from the first published notice is the single most useful early date. Nothing about the merits is answerable before an amended complaint and a briefing schedule. |

## Reading a docket sheet

A docket sheet is a list of events, each with a number, a date, a short clerk-written
description, and sometimes attachments. Three things a reader gets wrong:

1. **The description is written by the clerk.** It is a label applied at intake. It is not
   a reliable statement of what the document does. See refusal 2 below.
2. **A dated entry is when it was entered**, which may be days after it was signed or filed.
   Entered dates and filing dates diverge.
3. **The absence of an entry means nothing.** RECAP coverage is contributed by users. A
   docket with 12 entries in RECAP may have 200 on PACER. Say so when the record is thin.

### Scheduling order versus standing order

- A **scheduling order** is entered on this docket, in this case, and names dates for this
  matter. It is quotable as a source for a calendar entry.
- A **standing order** is a judge-wide or district-wide rule republished on the docket. It
  states defaults ("responses due within 14 days"), and applying it to compute a date for
  this case produces a lead requiring human verification rather than a calendar entry.
- A **notice of hearing** carries a specific time. It is the only entry that reliably gives
  you a time zone anchor.

If the entry does not name the date, you did not find the date. You inferred it.

## Refusal 1: never state a deadline without quoting the source docket entry

Every calendar item traceable to the docket carries the quoted entry text. If you cannot
quote it, the item is labelled `expected` or `speculated`, never `scheduled`, and the memo
says which entry it was derived from and what assumption was applied.

Every computed deadline is a **lead requiring human verification**. Local rules, chambers
rules, holidays, extensions granted by minute order and the three-day service rule all
change the answer, and none of them are visible in a search result.

## Refusal 2: never treat a filing-type classification as reliable without reading the filing

"Motion" in a docket description covers a motion to dismiss, a motion for an extension, and
a motion to seal. A memo that says "the motion to dismiss was filed" on the strength of a
clerk label is a fabricated characterisation. Fetch the document, or say the entry is
labelled a motion and its contents were not retrieved.

## Sealed and redacted entries

A sealed or redacted entry may be listed as an event with its **date and nothing else**.

Forbidden: inferring the contents, inferring the party, inferring the significance,
reasoning from the fact of sealing, or treating the sequence of surrounding entries as
evidence of what the sealed one says. Check C8 blocks it, and the reason it exists is that
a sealed complaint converted into a directional thesis is the worst real incident this desk
could produce.

Permitted: "Entry 43, filed 2026-06-02, sealed. Contents not available."

## Citation and docket identity

Two different checks, and the second is the one that matters most here.

- **Citation existence** (`court cite`) works only for cases with a reporter citation. A
  securities class action filed 40 days ago has none, so this check is structurally blind to
  the core workflow.
- **Docket identity** (`court docket`) is the check that catches the dominant hallucination
  class. For every docket number in the memo, confirm the docket exists, that the returned
  court matches the parenthetical you wrote, that the returned caption appears literally in
  the memo near the number, and that the party set includes the memo subject.

No judge surname appears in a memo unless it matches the `assigned_to` field of a resolved
docket. A judge name is the easiest thing in this domain to hallucinate confidently.

## Which docket URL goes in the memo

`court docket` prints six fields. The last one is `url:`, and it carries the public
permalink in the form `https://www.courtlistener.com/docket/<id>/<slug>/`. That is the
address a memo cites.

The `/api/rest/v4/dockets/<id>/` address the tool fetched stays out of the memo. It returns
401 to a reader who has no CourtListener token, which is every reader outside this desk, so
citing it hands the user a link they cannot open and a scorer a caption it cannot check. The
permalink opens in a browser with no token at all. Check C5 reads the docket id out of the
permalink path and matches it against the ledger, so the readable form is provenanced just
as tightly as the API form was.

The same holds for `court search`: its last column is already the permalink.

## Reading the per-citation statuses

`court cite` returns HTTP 200 with an array whose elements each carry their own `status`.
Keying on the HTTP status makes every fabricated citation read as verified. The mapping and
the exact shape are in `<LACUNA_ROOT>/skills/docket-research/references/court-recipes.md`.

## What is outside coverage

CourtListener and RECAP cover federal dockets and state appellate opinions. **State trial
courts are outside coverage.** A Delaware Superior Court or New York Supreme Court trial
docket returns nothing, and that nothing means "not covered" rather than "does not exist".
Say "outside coverage" in the memo. See the `source-discipline` skill.
