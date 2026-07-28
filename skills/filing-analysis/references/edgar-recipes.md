# EDGAR recipes

Exact invocations and the query language. Resolve `$LACUNA` from the session banner line
`LACUNA BINARY: python3 "<absolute path>"`, or from `cat .lacuna/bin-path` when the banner
is not visible, and substitute the absolute path when you issue the Bash call.

One network operation per Bash call. SEC is paced at 150 ms behind a shared cross-process
lock, and every request carries the configured contact email as its User-Agent.

---

## Full-text search syntax

EDGAR full-text search is a query language. It does **not** accept natural language. A
sentence typed into it returns a term-soup result set that looks plausible and means
nothing.

| Operator | Form | Effect |
|---|---|---|
| implicit AND | `securities investigation` | Both terms must appear |
| exact phrase | `"motion to dismiss"` | Quoted, adjacent, in order |
| OR | `settlement OR judgment` | Either term |
| NOT | `investigation NOT internal` | Excludes the second term |
| proximity | `fraud NEAR(10) investigation` | Within 10 words, either order |
| prefix | `arbitrat*` | Trailing wildcard only. A leading wildcard is not supported. |

Good queries are short and quoted. `"class action complaint"` beats
`find me any class action complaints filed against this company`.

```
python3 "$LACUNA" edgar search "\"class action complaint\"" --forms 8-K --since 2026-04-01
```

## The 2001 coverage floor

Full-text coverage begins in **2001**. A `--since` earlier than that is refused with an
explicit "outside EDGAR full-text coverage" message and a non-zero exit.

This refusal exists because a silent zero from a pre-2001 query is an invitation to fill the
gap from memory. Historical filings still exist in the archives and are reachable by
accession; they are simply not full-text searchable.

## The 10,000 window trap

EDGAR caps the full-text window at 10,000 results and returns
`hits.total.value: 10000` with `relation: "gte"`.

**That number is never reported as a count.** The correct rendering is:

> more than 10,000 matches, narrow by ticker, form or date

Reporting "10,000 filings mention this" is a fabricated statistic, and it is one a reader
cannot check without repeating the query. Narrow with `--forms` and `--since` until the
relation is `eq`, then the count is real.

---

## Recipe 1: resolve a company

```
python3 "$LACUNA" resolve "Meridian Biosciences"
```

Exit 7 with a candidate list means ambiguous. Stop and ask. Do not take the first row.

## Recipe 2: the recent 8-K stream

```
python3 "$LACUNA" edgar filings MRDN --form 8-K
```

Read the accessions and dates. Then fetch the ones whose date is near a docket event or a
price move.

## Recipe 3: the litigation disclosure in the last annual report

```
python3 "$LACUNA" edgar filings 0001234567 --form 10-K
```

Fetch the most recent, then read Item 3 and the commitments-and-contingencies note. Quote
both, and give the accession on the same line as the quote.

## Recipe 4: find the non-reliance filings

```
python3 "$LACUNA" edgar search "\"non-reliance\"" --forms 8-K --since 2025-01-01
```

Item 4.02 is the strongest single predictor of a securities class action in this data set.
If one exists inside the alleged class period, it belongs in `## Verified facts` with its
accession and its quoted text.

## Recipe 5: the 13D chain

```
python3 "$LACUNA" edgar filings 0001234567 --form "SC 13D"
```

Fetch each amendment and compare Item 4 across them. A 13G holder refiling on 13D is the
activist tell.

## Recipe 6: fetch one document

```
python3 "$LACUNA" edgar doc 0001234567-26-000123
```

Accession format is `NNNNNNNNNN-NN-NNNNNN`. The body arrives inside the untrusted-content
fence and is cached raw for quote checking.

---

## Accession numbers and constructed URLs

An accession has a canonical archive URL. Check C5 allows a constructed
`https://www.sec.gov/Archives/...` URL **provided the accession it carries is in the
ledger**, which is why fetching the document first matters even when you only intend to link
it. A link to a document you never retrieved is a fabricated citation with a plausible shape.

Never construct an accession number. Get it from `edgar filings` or `edgar search`.

## When a request fails

| Symptom | Meaning | What the memo says |
|---|---|---|
| `DATA UNAVAILABLE: SEC returned 403` | Missing or malformed contact email in config | Run `/lacuna:setup`. Nothing goes in the memo until it is fixed. |
| `RATE LIMITED` | Above the 150 ms floor, usually from a parallel run | Wait the stated seconds and retry the one call. |
| `NETWORK BLOCKED` | TLS interception on a corporate network | The certificate fix. Report it as an infrastructure gap. |
| `AMBIGUOUS` | More than one company matched | Show the candidates. Ask. |

None of these is ever rendered as "no filings found".
