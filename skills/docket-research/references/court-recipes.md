# Court recipes

Exact invocations. Resolve `$LACUNA` from the session banner line
`LACUNA BINARY: python3 "<absolute path>"`, or from `cat .lacuna/bin-path` when the banner
is not visible, and substitute the absolute path when you issue the Bash call.

One network operation per Bash call. CourtListener is paced at 1200 ms behind a shared
cross-process lock.

---

## 1. Securities class actions filed recently

```
python3 "$LACUNA" court search "securities fraud class action" --type r --court "nysd cand txsd"
```

`--type r` searches RECAP dockets rather than opinions, which is what you want for a matter
filed in the last few months. Opinions (`--type o`) will not contain it, because no opinion
exists yet.

Narrow by court when you can. A national search returns thousands and the first page is not
a sample of anything.

## 2. Cert petitions

```
python3 "$LACUNA" court search "petition for a writ of certiorari <party>" --type o
```

Then, for the docket itself:

```
python3 "$LACUNA" court docket "<docket number>" --court scotus
```

What to read for: the distribution date, the conference date, whether a response was
called for, and whether the Solicitor General was invited to file a brief (CVSG). A CVSG
adds six to twelve months and is itself a substantive signal.

## 3. Oral argument and SG amicus deadlines

```
python3 "$LACUNA" court search "<case name> oral argument" --type r
```

Argument calendars are published in advance. A calendar entry gives you a date, a court and
a time zone, which is everything a `scheduled` catalyst item needs. Quote the entry.

## 4. MDL consolidation

```
python3 "$LACUNA" court search "transfer order MDL <subject>" --type r
```

MDL numbers are `MDL No. NNNN` and are assigned by the JPML. Two traps:

- An MDL number is not a docket number. It does not match `\d:\d{2}-[a-z]{2}-\d{4,6}` and it
  will not resolve through `court docket`.
- If the search returns nothing, the required answer is that no such MDL was found. An MDL
  that does not exist is a common shape for a fabricated case reference, because the format
  is easy to imitate.

## 5. Class certification

```
python3 "$LACUNA" court search "motion for class certification <party>" --type r
```

Read for: whether the motion is filed, whether it is fully briefed, whether a hearing is
set. Class certification is usually the largest single value inflection in a class action
and it is frequently years after filing.

## 6. Settlement approval sequence

```
python3 "$LACUNA" court search "preliminary approval class settlement <party>" --type r
```

The sequence, each step of which is a dated docket entry you can quote:

1. Motion for preliminary approval
2. Preliminary approval order (sets the notice plan)
3. Notice period
4. Objection and opt-out deadline
5. Fairness hearing under Rule 23(e)
6. Final approval order and judgment
7. Appeal window, then any objector appeal

## 7. Circuit appeals

```
python3 "$LACUNA" court search "<party>" --type r --court ca3
```

Court identifiers are CourtListener slugs: `ca1` through `ca11`, `cadc`, `cafc`, `scotus`,
and district slugs such as `nysd`, `cand`, `txsd`, `deld`. A wrong slug returns an empty
result set that reads as "no appeals", so confirm the slug before reporting a negative.

There is no deadline on a circuit decision. The only defensible reference class is published
median time to decision for that circuit, and it must be cited if used.

## 8. Books and records (DGCL Section 220)

```
python3 "$LACUNA" court search "Section 220 books and records <company>" --type o
```

Delaware Chancery. Fast, and frequently the precursor to a fiduciary-duty complaint. A
Section 220 demand surfacing before anything else is an early-warning signal worth stating
explicitly in `## Inference`, labelled as inference.

## 9. Bankruptcy

```
python3 "$LACUNA" court search "<debtor> chapter 11" --type r
```

Dated items worth calendaring, each quotable from the docket: disclosure statement hearing,
plan confirmation hearing, claims bar date, and any 363 sale milestones.

---

## 10. Verifying a docket number

```
python3 "$LACUNA" court docket "1:26-cv-04471" --court nysd
```

Returns `exists`, `court`, `case_name`, `assigned_to`, `parties`. Four assertions to make
before the number goes in a memo:

1. It exists.
2. The returned `court` matches the parenthetical you wrote, for example `(S.D.N.Y.)`.
3. The returned `case_name` appears literally in the memo within 200 characters of the
   number.
4. The returned `parties` include the memo subject.

`assigned_to` is the only permissible source for a judge surname in the memo.

---

## 11. Verifying citations, and the per-item status trap

```
python3 "$LACUNA" court cite -
```

Feed the whole text blob on stdin. The endpoint extracts every citation from the submitted
text in one round trip. Per-citation POSTs at a 1.2 s floor put a 20-citation memo past any
sane hook timeout, and a timed-out hook does not exit 2, which silently converts a
fail-closed gate into a fail-open one. `bin/lacuna` chunks at 60 citations or 60 kB,
whichever comes first, and caches every result in `.lacuna/cite-cache.json`, so a revision
loop costs nothing.

**The response is HTTP 200 even when every citation in it is fake.** Each element of the
returned array carries its own `status`:

| Per-item status | Meaning | What the memo must do |
|---|---|---|
| `200` | Found. `clusters` holds the matching case or cases. | Cite it. Add the caveat that good law and support for the proposition were not checked. |
| `300` | Ambiguous. More than one cluster matched. | Label it ambiguous and list the candidates. It is not a verified citation. |
| `404` | Not found. | Confine it to `## Rejected and unverified claims`. It may never be a premise. |
| `400` | Malformed reporter. | Show what was parsed. Confine it to the rejected section. |

HTTP-level statuses are a different question:

| HTTP status | Meaning | Behaviour |
|---|---|---|
| `401` / `403` | No token, or the token is rejected. | Cannot verify. Degrade: the memo carries `Case-law verification: OFF` and every case citation moves to the rejected section. This is an infrastructure failure and never blocks. |
| `429` | Rate limited. | Paced retry. Never rendered as "not found". |
| `5xx` | Upstream failure. | Infrastructure failure. Never rendered as "not found". |

The distinction between "this citation does not exist" and "I could not check" is the whole
value of the check. Collapsing them in either direction defeats it.
