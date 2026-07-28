# lacuna

A Claude Code plugin that turns a fresh session into a litigation research desk.

## 1. What this does

It reads federal court dockets and SEC filings for you, checks that every case
and filing it cites is real and was actually retrieved, and writes up what it
found in a form you can act on. Anything it could not verify is kept in its own
section, clearly labelled, so you can see at a glance which paragraphs are
grounded and which are guesswork. It is built for people who are not lawyers,
not trained traders, and not especially interested in how AI works. It never
places a trade.

## 2. Install

**Before you start.** You need `git` installed and Python 3 available as
`python3`. Type `git --version` and `python3 --version` in a terminal. If
either prints an error, install it before going further.

This plugin is installed from a local checkout. There is no public marketplace
entry for it yet, so a `/plugin marketplace add <owner>/<repo>` line would fail
with a git error. Get the directory onto your machine (clone it, or copy the
folder someone handed you), then in Claude Code:

```
/plugin marketplace add ./lacuna-plugin
/plugin install lacuna@lacuna-tools
```

The path is the directory that contains `.claude-plugin/marketplace.json`.

**The checkout must be a git repository with at least one commit.** The plugin
stamps the commit SHA into every memo it writes, and that stamp is what ties a
memo to the exact set of guardrails that produced it. If you copied the folder
rather than cloning it, run this once inside it:

```
git init && git add -A && git commit -m "lacuna 0.1.0"
```

If you skip that, the session banner says so in a `WARNING:` line and every
memo carries `generated_by: lacuna@v0.1.0`, which names the release but not the
exact tree, so two installs of the same release are indistinguishable.

## 3. Confirm it installed

Type `/lacuna` in Claude Code. You should see three commands: `setup`,
`research`, `verify`. If you see nothing, quit Claude Code and reopen it, then
try again. Seeing the three commands is the success signal. If they are still
missing after a restart, run `/plugin` and check that `lacuna` is listed as
enabled.

## 4. Set up

Run `/lacuna:setup`. It takes about three minutes and asks you a handful of
questions.

It will ask for an email address. That goes to the SEC as a contact header on
every request, which the SEC requires. It is not a password and it is not
stored anywhere outside your machine.

It will also ask you to create one free account, at CourtListener, and paste in
the token it gives you. There is no card and no billing. That token is what
unlocks citation verification, which is the single most important thing this
plugin does. You can decline, and everything else still works, but every memo
produced without it carries a `Case-law verification: OFF` banner and confines
every case citation to the rejected section. Setup will ask again next time.

Setup is re-runnable and idempotent. Run it again any time to change your
answers. `/lacuna:setup --check` prints the connection table only.
`/lacuna:setup --reset` clears your settings and asks everything again.

## 5. The three commands

**`/lacuna:setup`** configures the desk. Covered above.

**`/lacuna:research <company, case name, or docket number>`** does the work. It
resolves your subject to a real docket and a real ticker, searches the courts
across at least three distinct legal angles, pulls the company's own SEC
filings, checks the news, and writes a memo to `cases/<case-id>/memo.md`.

It does **not** measure how the market moved around each catalyst. There is no
price leg in this build: `## Price evidence` is a documented gap, and any
return figure appearing there without a matching price retrieval in the ledger
blocks the memo. See section 6.

Expect three to eight minutes. You will see progress lines the whole way, like
`[2/6] searching CourtListener for "securities fraud"`. It is slow because the
sources are rate limited and the plugin respects those limits rather than
getting your office IP address blocked.

If the evidence is thin, the memo says so and stops. It will not pad.

**`/lacuna:verify <claim, citation, or file path>`** checks one thing. Give it
a case citation and you get back `VERIFIED`, `NOT FOUND`, `AMBIGUOUS` or
`MALFORMED REPORTER`. Give it a claim about a filing and you get either the
actual quoted text with its accession number, or a statement of what was
searched and what was not, scoped precisely. Give it a path to a memo and you
get the full verification report printed without blocking anything.

## 6. What it will not do

- **It will not place trades.** No order path exists in the code, and the
  plugin actively blocks broker and exchange hosts. A human places every order.
- **It will not tell you whether a case is still good law.** No free citator
  exists. Verifying that a case is real is a different question from verifying
  it has not been overruled, and this plugin only answers the first.
- **It will not tell you whether a case supports the point it is cited for.**
  That is a reading task for a lawyer. Every memo says so on its face.
- **It will not see state trial courts.** The available data covers federal
  dockets and state appellate opinions. State trial matters come back as
  "outside coverage" instead of an empty result you might read as "nothing
  there".
- **It will not invent a citation to fill a gap.** A citation that does not
  resolve is moved to `## Rejected and unverified claims` and is mechanically
  barred from being used as a premise anywhere else in the memo. The same rule
  covers a bare `X v. Y` case name with no reporter citation at all.
- **It will not give you price or return figures.** This build has no price
  leg. A partial one is worse than none: without split and halt handling a raw
  close series reports moves that did not happen. `## Price evidence` says
  "DATA GAP" and the verifier blocks any return figure written there that no
  ledgered price fetch backs.

### Known limits of the checks

The checks that run on every memo are deterministic code, and deterministic code
sees only what it was written to see. Stated plainly:

- **The confidence check is a lint over common phrasings.** It looks for
  percentages, decimals, "three in four", "more likely than not" and a short list
  of outcome verbs, read over each paragraph. A probability expressed in wording
  it does not carry, or split far enough from the outcome it refers to, goes
  unchallenged.
- **The nonpublic-leak check matches exact wording.** It compares word runs from
  `## Provenance` against the guarded sections. Reworded material carries the same
  information past it. It catches copy-paste, and a paraphrase defeats it.
- **URL provenance stops at the host and the identifier.** The verifier requires
  that an allowlisted URL carry an accession, docket or CIK that appears in the
  ledger. That proves those were retrieved. It cannot prove that the specific
  document path in the link is the one that was fetched.
- **None of this replaces a human reading the memo.** Every check is a floor
  under obvious fabrication. Passing them means no check caught anything, which is
  a much weaker claim than the memo being right.

## 7. Why the friction exists

There are now over 1,500 court decisions worldwide involving AI-fabricated
material in filings, and the count is climbing every month. In one widely
reported matter the court imposed a six-figure sanction, with the aggravating
factor being that counsel refiled after being put on notice that the citations
were fake.

The pattern is always the same. A model produces a citation that looks exactly
like a real one. Asked to check its own work, it confirms its own invention,
because checking a citation by recalling it is the same operation that produced
it. So every check in this plugin that matters runs outside the model as plain
deterministic code, against the actual response from the actual court database,
and it runs automatically on a file hash rather than waiting for anyone to
remember to ask for it.

That is why setup asks for a token, why research takes minutes instead of
seconds, and why the memo sometimes comes back and tells you it could not
verify something you were sure about.

## 8. When something looks wrong

**`command not found: lacuna`** in a Claude Code turn. There is no PATH entry
for plugin binaries. Every invocation goes through `python3` and an absolute
path. That path is printed at the top of every session as a line beginning
`LACUNA BINARY:`, and it is written to `.lacuna/bin-path` in your project. If
the session banner has scrolled away or the conversation was compacted, read
that file:

```
cat .lacuna/bin-path
```

then paste the path it prints into the call:

```
python3 "/absolute/path/to/bin/lacuna" check
```

(Inside a Claude Code turn, use the literal path. Command substitution such as
`$(cat ...)` is denied by the egress wall, because a wall that cannot read the
command it is approving is not a wall.)

**`DATA UNAVAILABLE: SEC returned 403`.** The SEC is rejecting requests that
carry no real contact address, which means your contact email is missing or has
a typo. Run `/lacuna:setup` and check it.

**`NETWORK BLOCKED: ...`.** Your network is inspecting secure connections and
Python does not trust its certificate. On macOS, run the "Install Certificates"
command that shipped with your Python install. Otherwise ask IT for your
organisation's certificate file and point the plugin at it:

```
python3 "/absolute/path/to/bin/lacuna" config set ca_bundle /path/to/your-ca-bundle.pem
```

**`RATE LIMITED: ...`.** A source is throttling you. The message names how many
seconds to wait. Waiting is the fix. If it is CourtListener and you have not
added the free token yet, adding it raises your limit.

**A memo was blocked by the verifier.** Read the message. It names the exact
line and the exact span that failed, and it names the remedy. To see the same
report without anything being blocked, run `/lacuna:verify` on the file path,
which prints the full explanation and changes nothing.

Every one of these paths ends the same way: run `lacuna check` to see where
your settings are stored, which sources are reachable, and which version of the
plugin you are on. Never guess at the settings location. `lacuna check` prints
the directory it is actually using.

## 9. Costs

Zero. Every source is free and keyless except CourtListener's citation
verification endpoint, which needs a free account with no card. There are no
paid API keys, no subscriptions, and no per-page charges. In particular this
plugin does not touch PACER, which bills real money per page.

## 10. Privacy and retention

Everything stays on your machine. Nothing is uploaded anywhere.

`.lacuna/cache/` holds the raw bodies of everything fetched, truncated to the
first 2 MB per document. It exists so the verifier can check quotes against
what the source actually said. It is pruned automatically at 200 MB or 30 days,
whichever comes first, on every write. There is no `cache gc` subcommand in
this build; to prune it by hand, delete files under `.lacuna/cache/` yourself.
Deleting a cached body does not corrupt anything, but a memo quoting a source
whose body is gone will block on re-verification until you refetch it.

`.lacuna/ledger.jsonl` records every request the desk made. It is append-only,
because a memo's freshness claims are only meaningful if the retrieval record
cannot be quietly edited.

If a case turns out to involve privileged or nonpublic material and you need it
gone, **there is no `purge` subcommand in this build.** Do it by hand:

1. Delete or redact `cases/<case-id>/memo.md` yourself.
2. Open `.lacuna/ledger.jsonl`, find every line whose `case_id` is that case,
   and note each `sha256` value. Delete `.lacuna/cache/<sha256>.txt` for each.
   Those files are the retrieved source bodies.
3. Leave `.lacuna/ledger.jsonl` alone. It is append-only by design: it records
   what was fetched and when, not what the documents said, and a freshness
   claim is only meaningful if the retrieval record cannot be quietly edited.
   If your situation requires the ledger lines gone too, delete the whole
   `.lacuna/` directory rather than editing lines out of it, and say so to
   whoever asked, because every memo's `As of:` stamp then has nothing behind
   it.

`cases/` and `.lacuna/` are both added to your `.gitignore` at setup, because
the default assumption is that memos are work product that may be privileged.
Tracking them in git is an explicit opt-in that setup asks you about.

## 11. Versions and rollback

`lacuna check` prints the plugin's git SHA. Every memo carries
`generated_by: lacuna@<sha>` in its frontmatter, so any memo can be traced back
to the exact set of guardrails that produced it, which matters if a memo ever
ends up in front of a court. `CHANGELOG.md` records what changed in each
version.

To roll back, check out an earlier commit in your local clone and reinstall:

```
git -C ./lacuna-plugin log --oneline
git -C ./lacuna-plugin checkout <the sha you want>
```

then in Claude Code:

```
/plugin marketplace remove lacuna-tools
/plugin marketplace add ./lacuna-plugin
/plugin install lacuna@lacuna-tools
```

## 12. Uninstall

```
/plugin uninstall lacuna@lacuna-tools
/plugin marketplace remove lacuna-tools
```

Then open `.claude/settings.json` in your project and delete the line under
`permissions.allow` that begins `Bash(python3` and points at the lacuna binary,
along with the two `WebFetch(domain:...)` entries under `permissions.deny` that
setup added. Your `cases/` directory and its memos are yours and are left
untouched. Delete `.lacuna/` if you also want the cache and the retrieval
ledger gone.

---

Internal research tooling. Not legal advice. Not investment advice. Not a
recommendation to buy or sell any security.
