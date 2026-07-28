---
description: Check one thing. Give it a case citation to confirm the case exists, a claim about a filing to check against the actual filed text, or a memo file path to run the full ten-check report without blocking.
argument-hint: "<claim, citation, or file path>"
---

# /lacuna:verify $ARGUMENTS

Verify exactly one thing and answer bluntly. Do not research around the question, do not
volunteer a thesis, and do not soften a negative into a maybe.

## Resolve the binary path

The session banner prints `LACUNA BINARY: python3 "<absolute path>"`. If it is not visible
(for example after a compaction), run `cat .lacuna/bin-path` and use its contents. That
value is `$LACUNA` below; substitute the resolved absolute path when you issue the Bash
call. One network operation per Bash call.

## Mode detection

Read `$ARGUMENTS` and pick exactly one mode.

| Shape | Mode |
|---|---|
| Ends in `.md`, or names an existing path | **File** |
| Matches a reporter citation, for example `402 F.4th 1188`, `347 U.S. 483`, `2024 WL 118822` | **Case citation** |
| Anything else: a sentence about what a company said, filed or disclosed | **Filing claim** |

If two modes are plausible, say which one you chose and why in one line before running.

---

## Mode 1. Case citation

```
python3 "$LACUNA" court cite -
```

with the citation text on stdin. Key on the per-item `status` field inside the JSON body,
never on the HTTP status. Answer with exactly one of these four verdicts:

- **VERIFIED.** Give the resolved case name, court, year, and the CourtListener URL.
- **NOT FOUND.** *"CourtListener has no case at that citation. Treat it as fabricated until
  someone produces the reporter volume."*
- **AMBIGUOUS.** More than one cluster matched. List the candidates and stop.
- **MALFORMED REPORTER.** The reporter abbreviation is not one CourtListener recognises.
  Show what it parsed.

Then, in every case, add the caveat verbatim:

> NOT CHECKED: whether this case is still good law, and whether it supports the point it is
> cited for. No free citator exists. A lawyer must read the case.

If the tool exits with `SETUP REQUIRED` because there is no CourtListener token, say so and
point at `/lacuna:setup`. Do not answer from model knowledge. A remembered case is not a
verified case.

---

## Mode 2. Filing claim

1. Resolve the company to a CIK: `python3 "$LACUNA" resolve "<company>"`. Exit 7 means
   ambiguous; show the candidates and stop.
2. List the plausible filings: `python3 "$LACUNA" edgar filings <CIK> --form <form>`.
3. Fetch the specific document: `python3 "$LACUNA" edgar doc <accession>`.
4. Search the fetched body for the claim. Quote the actual sentence, or report its absence.

Answer with one of four verdicts, and always scope the negative to what you actually
searched:

- **CONFIRMED IN `<accession>` (`<form>`, filed `<date>`).** Followed by the quoted text.
- **NOT FOUND IN `<accession>` (`<form>`, filed `<date>`).** Followed by one line stating
  which forms, which date range and which exhibits were searched and which were not.
- **PARTIALLY CHECKED.** Use this when the filing set you could search does not cover the
  claim's likely home, for example when the claim would live in an exhibit that is a PDF or
  in a form outside the range you pulled. Name the gap.
- **DATA UNAVAILABLE.** The source returned an unexpected status or an unparseable body.
  Repeat the tool's own message. Never render this as "nothing found".

"Not found in the documents I searched" and "the company never said that" are different
statements. Only ever make the first one. A verification tool that lets a novice read a
partial search as a global negative becomes a source of new false beliefs.

---

## Mode 3. File path

```
python3 "$LACUNA" verify --explain <path>
```

`--explain` runs the identical ten-check suite, prints the identical report, blocks
nothing, and does not touch `.lacuna/verified.json`. This is the escape hatch when the Stop
hook is refusing a memo and the user needs to see why without fighting the loop.

Present the report as a table: check id, severity, line, what is wrong, what to do about it.
Then give the one-sentence bottom line: whether the memo would currently pass the gate.

If the file carries `VERIFICATION FAILED, DO NOT RELY ON THIS MEMO`, lead with that. It
means the gate fired three times on the same finding set and gave up blocking, so the
failures are permanent in the file until a human fixes them.

---

## Never

- Never answer any of the three modes from model knowledge. If the tool did not return it,
  you did not verify it.
- Never claim a case is good law, or that it supports the proposition it is cited for.
  Neither check exists in any free source.
- Never turn a verification request into a research run. If the user wants the surrounding
  work, point them at `/lacuna:research`.
