---
description: Set up the lacuna research desk. Probes every data source, asks three questions, installs the CourtListener token, writes the shim, scopes permissions, and creates the workspace. About three minutes. Re-runnable and idempotent.
argument-hint: "[--check | --reset]"
---

# /lacuna:setup

You are setting up a litigation research desk for someone who is not a lawyer, not a
trader by training, and not AI-savvy. Speak plainly. Never show a stack trace. Never
ask a question whose answer the user cannot possibly know yet.

Run steps 1 through 9 below in order. The whole flow is idempotent: re-running it must
converge to the same end state without duplicating anything.

## Argument handling

- `--check`: run step 1 only, print the two probe tables, then stop.
- `--reset`: before step 1, run the config wipe (`python3 "$LACUNA" config set` has no
  delete verb, so instead delete the config file whose path `python3 "$LACUNA" check --json`
  reports under `state_dir`) and then run every step as if this were a first install.
- No argument: run every step.

## Resolving the binary (do this first, every time)

There is no `lacuna` on your PATH inside the Bash tool. Resolve the path like this:

1. Look for the session banner line `LACUNA BINARY: python3 "<absolute path>"`. That
   `<absolute path>` is `$LACUNA`.
2. If the banner is not visible (for example after a compaction), run
   `cat .lacuna/bin-path` and use its contents.
3. If `.lacuna/bin-path` does not exist yet, ask the user to quit and reopen Claude Code
   so the SessionStart hook can write it, then stop.

Every call in this file is written as:

```
python3 "$LACUNA" check --json
```

Substitute the resolved absolute path in place of `$LACUNA` when you actually issue the
Bash call, so the scoped permission rule written in step 6 matches the command string.

Issue exactly one network operation per Bash call. Never chain several paced calls into
one invocation: the tool timeout kills the call mid-sleep and the user sees a truncated
error with no partial results. Give each call a generous explicit timeout (120000 ms).

---

## Step 1. Probe

Run:

```
python3 "$LACUNA" check --json
```

Render the result as two markdown tables. Do not paste raw JSON at the user.

**Required**

| Check | State | What it means |
|---|---|---|
| python3 | ok / down | |
| TLS | ok / down | |
| SEC EDGAR | ok / throttled / setup / down | |
| CourtListener search | ok / throttled / setup / down | |

**Optional**

| Check | State | What it means if it is down |
|---|---|---|
| GDELT news | ok / throttled / down | News search is down right now. Memos will say "news unavailable" instead of guessing. You can still work. |
| CourtListener citation verification | ok / off / down | Case citations cannot be machine-checked. Every memo will carry a "Case-law verification: OFF" banner and every case citation will be confined to the rejected section. Step 4 fixes this. |

Four states: `ok`, `throttled, retry`, `setup`, `down`.

- `throttled, retry`: wait the pacing floor for that source and probe that one row a second
  time before you call anything down. GDELT rate-limits regularly, so a single throttle is
  a normal afternoon rather than a broken install.
- `setup`: a setting a later step of this command supplies is not there yet. On a clean
  machine SEC EDGAR reads `setup` on this first probe, because the contact email you are
  about to give in step 2 is what fixes it. **This never stops the flow.** `check` exits 0
  in that state; say the one line ("expected before step 2") and move on.
- `down`: unreachable.

Gate: if a **required** row is `down`, stop and tell the user what to try, in this order:
`NETWORK BLOCKED` means the certificate fix (section 8 of the README); a required source
down with a clean TLS check usually means try again in a few minutes.

Optional rows being down never stops setup, and a `setup` row never stops setup.

## Step 2. Three questions

Ask these with `AskUserQuestion`, one question per call or batched, with concrete
options. If `AskUserQuestion` is unavailable, ask them as plain numbered questions in
chat and accept free text.

**Q1. Contact email.** Required. Say plainly: *"The SEC requires a real contact address
on every request. This is a courtesy identifier. It is stored on this machine only and it
is safe to share."* Free-text answer. Validate that it contains `@` and a dot after it. On
a malformed address, ask once more rather than guessing.

Write it:

```
python3 "$LACUNA" config set contact_email "<their address>"
```

**Q2. Which two venues matter most?** Options, pick up to two:
Delaware Chancery / ITC Section 337 / PTAB / agency enforcement / FDA / EU and UK /
bankruptcy / securities class actions. Store as a comma-joined list:

```
python3 "$LACUNA" config set venues "securities class actions,Delaware Chancery"
```

**Q3. Which tickers or sectors do you already watch?** Free text is fine. Store:

```
python3 "$LACUNA" config set watch_tickers "AAPL,MRNA,regional banks"
```

Do not ask anything else here. Questions about memo length, hedging, or what "too
illiquid" means produce low-quality guesses before the user has seen a single memo.
Those are elicited from the first artifact instead: after the first `/lacuna:research`
completes, ask exactly two calibration questions about that memo ("too long or about
right", "too hedged or about right") and append the answers to `cases/profile.md`.

## Step 3. Restricted list

Ask, every run, including re-runs: *"Are there any companies or parties this desk must
not research or trade? Blank is a fine answer."*

`restricted_tickers`, `restricted_parties` and `allowlist_extra` are compliance settings.
The PreToolUse hook **denies** `config set` on all three from any session-issued Bash call,
including this one, because a session that can empty its own restricted list has no
restricted list. So hand the user two lines to run **in their own terminal** (the shim from
step 4 is already installed by the time you reach this step):

```
lacuna config set restricted_tickers "<comma list, or the empty string>"
lacuna config set restricted_parties "<comma list, or the empty string>"
```

If `command -v lacuna` did not resolve in step 4, give the absolute-path form instead:
`python3 "<resolved absolute path>" config set restricted_tickers "..."`.

Ask them to paste back the confirmation line each command prints, then run
`python3 "$LACUNA" config show` to read the stored values back and repeat them out loud.

Tell the user what this does: a memo whose subject or tickers hit this list is blocked
by the verifier with "restricted name, escalate to compliance", and the hit is recorded
in `.lacuna/restricted-hits.jsonl`.

## Step 4. Shim

Do this before the token step: the token step hands the user a command to type, and this
is what makes that command work.

Write `~/.local/bin/lacuna` so the human has a working invocation in their own terminal:

```
#!/bin/sh
exec python3 "<resolved absolute path to bin/lacuna>" "$@"
```

`chmod 755` it, then verify with `command -v lacuna`. If it resolves, tell the user they
can type `lacuna check` in their own terminal, and remember that it did for steps 3 and 5.
If `~/.local/bin` is not on their PATH, say so plainly and use the absolute-path form
everywhere below instead. Do not edit their shell profile.

## Step 5. CourtListener token (default yes)

Run `python3 "$LACUNA" config show` first. If a token is already present (it prints as
`present (…last4)`), say so and skip to step 6.

Otherwise ask for it. This is the single most important safety feature in the plugin,
so ask on every setup run until it exists. Frame it honestly: *"Free, no credit card,
email signup, about ninety seconds. It is what lets me check that a case citation
points at a real case. Without it, every case citation I produce gets filed under
'unverified' and the memo carries a banner saying case-law verification is off."*

Give the sign-up URL: `https://www.courtlistener.com/help/api/rest/` (create an account,
then copy the API token from the profile page).

Offer three ways to hand it over, in this order:

1. **Save it to a file.** *"Click Save in your browser, or paste it into a file, then
   tell me the filename."* Read the file, write the token with
   `python3 "$LACUNA" config set courtlistener_token "<value>"`, then delete the file
   and confirm the deletion out loud.
2. **Run one command yourself.** Give them a fully resolved, copy-pasteable line. If
   `command -v lacuna` resolved in step 4, that is:
   `lacuna config set courtlistener_token YOUR_TOKEN_HERE`
   Otherwise give the absolute-path form, with the real path substituted:
   `python3 "<resolved absolute path to bin/lacuna>" config set courtlistener_token YOUR_TOKEN_HERE`
3. **Paste it in chat.** One honest line: *"it goes into the transcript file on this
   machine and does not leave your computer."* For a free, rate-limit-only, no-billing
   token that is an acceptable trade.

If the user declines, state plainly what stays off (citation existence checking, the
`## Rejected and unverified claims` confinement rule applies to every case citation, and
every memo carries the OFF banner), record nothing, and move on. Ask again next run.

## Step 6. Permissions

Without this, a single research run raises 10 to 20 permission dialogs and the user
reaches for the broadest "allow all Bash" option, which is strictly worse for safety
than a scoped rule and permanently defeats the deny wall.

Read `<project>/.claude/settings.json` if it exists. Merge (do not overwrite) these
entries, creating the file and its parent directory when absent:

```json
{"permissions": {
  "allow": ["Bash(python3 /abs/path/to/bin/lacuna:*)"],
  "deny": ["WebFetch(domain:app.alpaca.markets)", "WebFetch(domain:clob.polymarket.com)"]}}
```

Substitute the real resolved absolute path. Preserve every existing key and every
existing array element; append only. Then read the file back and show the user the three
lines you added, in plain English:

- *"Line 1 lets me run the lacuna tool without asking you every time."*
- *"Lines 2 and 3 stop me from reaching two trading venues. This desk produces research.
  A human places every order."*

Never suggest an allow-all rule. Tell the user removal is documented in the README.

## Step 7. Workspace and confidentiality

1. Create `cases/` if absent.
2. Run `python3 "$LACUNA" template profile > cases/profile.md`, then replace every
   `[PLACEHOLDER]` **that stands in a field position** (after a `: ` or on its own after a
   `- `) with the answers from steps 2 and 3. Under `## Notes`, `- none` is already the
   shipped value; leave it unless the user gave you something. The gate is line-anchored,
   so the template's own prose is safe; only a field left unfilled makes a data subcommand
   exit 5. Confirm by running `python3 "$LACUNA" check --json` and seeing it not exit 5.
3. Create `.lacuna/` if absent.
4. Append `.lacuna/` and `cases/` to `.gitignore`, checking first for existing entries so
   re-running does not duplicate them, creating the file if absent, and skipping silently
   if `git rev-parse --git-dir` fails.

Then ask one question: *"Will other people see this repo?"* If a remote is configured and
you cannot verify it is private, warn plainly that memos may contain privileged work
product and offer to keep `cases/` untracked. Tracking memos in git is an explicit opt-in;
if the user opts in, remove the `cases/` line you just added and say what changed.

## Step 8. Re-probe with real requests

Two live calls, one per Bash invocation, using the newly configured contact email:

```
python3 "$LACUNA" edgar search "securities class action" --forms 8-K
```

```
printf '347 U.S. 483' | python3 "$LACUNA" court cite -
```

The citation must be piped in on the same command, exactly as written above. `court cite -`
reads stdin, and with empty stdin it prints "no reporter-style citations were found" and
exits 0, so a run that verified nothing would read as a success. Use that citation and no
other: it is *Brown v. Board of Education*, it is settled, and it will not surface a live
controversy in a transcript on a client machine.

Print the second probe table. Say "Case-law verification: ON" only if the output names
`347 U.S. 483` with a found status (`VERIFIED`, or status 200). Any other output means the
check is OFF, including "no reporter-style citations were found", an error prefix, or an
empty result. Report it as OFF in those words and say which of the two causes it was: no
token installed, or the lookup was unreachable.

## Step 9. Close

Say exactly this shape:

> You're set up. Try `/lacuna:research <company or case name>`.

Then one short summary: which sources are live, whether case-law verification is on, where
the memos will land (`cases/<case-id>/memo.md`), and the fact that a research run takes
typically 10 to 25 minutes, with progress lines while it works.

If anything optional stayed down, restate its one-line consequence so the user is not
surprised later.
