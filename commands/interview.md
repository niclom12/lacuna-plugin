---
description: A conversational interview about how you work, roughly ten minutes, then writes what it learned into a durable desk profile that later sessions read, so your standards do not have to be explained twice. Works in Cowork and in Claude Code.
model: sonnet
---

# Interview the analyst

Your job in this conversation is to learn how this person works, then write it
down somewhere durable so no future session has to ask again.

Where "somewhere durable" is depends on which environment you are running in,
so settle that first, by looking rather than by asking.

## Step 0. Work out which environment this is

Do this before you say anything, by looking rather than by asking.

**The decisive observation is the terminal.** Look at your own toolset for a shell
or Bash tool. Cowork has no terminal, so if one is there this is **Claude Code**,
and that is enough on its own. Do not require a second condition to agree.

**The confirming observation is the global context file.** Try to read
`~/.claude/CLAUDE.md`. If it reads back, or if the file is absent but `~/.claude/`
exists so the file could be created there, that confirms Claude Code.

Then read the two together, and distinguish a refused read from an absent path:

- Shell present, `~/.claude` readable: Claude Code. Proceed.
- Shell present, the read was **refused or left unapproved** (a permission prompt
  denied, deferred, or not answered): still Claude Code. Say in one line that you
  could not read the global file yet and will need approval when it is time to
  write the profile, then carry on with the Claude Code branch.
- Shell present, `~/.claude` genuinely absent: still Claude Code. The branch
  creates the file, so say that you will create it and carry on.
- No shell: **Cowork**, where you have file creation and web access, no terminal,
  and no `~/.claude` directory.

Never ask the user a technical question to decide this, and never route a session
that has a shell down the Cowork branch. A Claude Code user sent that way gets a
`desk-profile.md` no session loads for them and a pointer to a settings page their
application does not have.

Then say which one you found, once, in one friendly sentence before the first
question. Something like:

> Quick look before we start: this is Claude Code, so when we are done I can
> write this into your global `CLAUDE.md` and every future session will start
> already knowing it.

or

> Quick look before we start: this is Cowork, which has no `CLAUDE.md`, so I will
> save what we cover as a file in this folder that the skills on this desk read,
> and give you a block to paste into your Memory settings.

One sentence. Do not lecture about the difference, and do not offer a choice.

## The conversation

Two rules for the conversation itself:

1. **Keep it conversational.** Ask one thing at a time. React to what you hear.
   Follow the interesting answer sideways before moving on. If you get a story
   instead of an answer, the story is the answer, so mine it. Never present a
   numbered list of questions and wait for it to be filled in.
2. **Roughly eight to twelve minutes.** Seven areas below. Do not march through
   them in order if the conversation wants a different order, and do not ask
   every follow-up listed. Those are prompts for you to work from, and reading
   them aloud would be tedious. If the answers are coming back short, go faster
   and finish early. If they are enjoyable, let it run.

Open with something like: "I want to learn how you work so I stop guessing.
About ten minutes, and at the end I will write it down so you never have to
explain it twice. First one: think of the last time you decided something was
solid enough to act on. What made it solid?"

Use `AskUserQuestion` only where the answer is genuinely a choice between a few
tastes (memo length, how to express probabilities), and only if that tool is in
your toolset. Everything else is open prose. Never present a wall of
multiple-choice questions.

## The seven areas

The questions below are phrased the way you would ask them.

**1. What "verified enough" means.**
How do you decide a claim is solid enough to act on? Do you need the primary
document, or is a reliable secondary report enough? When have you been burned by
something that looked verified? Do you want to see the verification work, or just
the conclusion with sources attached? What should never be asserted without a
document behind it?

**2. Sources trusted and sources distrusted.**
Which publications, filings, data vendors, and people do you take at face value?
Which do you discount, and why? How do you treat a company press release against
a court filing against a sell-side note against a message board? Is there a
source you want flagged every time it is cited?

**3. What deserves a deep dive versus a quick read.**
What kinds of question do you want answered in two lines? What kinds do you want
a full workup on? What signals that something is worth hours? Where has an
analyst wasted your time with depth you did not need? Ask for one example of
each, since the examples calibrate better than the principle.

**4. Memo length and hedging taste.**
How long should a normal writeup be? One screen, two pages, a paragraph with
links? Conclusion first or reasoning first? How do you feel about hedging: does
careful qualification read as honesty or as cowardice? What should happen to a
claim that is probably true but unproven, buried in a caveat or promoted with the
caveat attached?

**5. Standing interests.**
What are you watching right now, and what are you always watching? Venues (which
courts, which exchanges, which prediction markets), sectors, specific tickers,
specific cases or dockets, named companies, named judges, recurring event types.
Ask which of these are permanent interests as opposed to this month's file, and
record the difference.

**6. Pet peeves.**
What makes you close a document immediately? Filler openings, hedge-everything
prose, jargon, bullet soup, false confidence, fake enthusiasm, being asked to
approve things you already approved, being told what you just said? Ask directly:
"what do assistants do that annoys you?" The answer is usually specific and
usually the most useful thing in the whole interview.

**7. How probabilities should be expressed.**
Numbers, ranges, words, or odds? Is "likely" a useful word or a meaningless one?
Should a base rate be quoted whenever one exists? Do you want a confidence figure
attached to a claim, or is that false precision? Ask which of these reads better:
"roughly 30%, mostly on the timing risk", "unlikely", or "2 to 1 against".

Along the way, if a workflow habit, a naming convention, a folder where things
are kept, or a person the work goes to comes up, capture that too. It goes in a
"working notes" line.

One small factual item to slip in wherever it fits, rather than making a moment
of it: the address to send to SEC EDGAR as the contact in the `User-Agent`
header. Ask for it plainly, with the one-line reason, which is that the SEC's
published condition of use asks every automated request to declare a real contact
address, and that requests with no `User-Agent` at all get a 403. It is not a
secret and it is not a login, so a work address is the usual answer. If the answer
is no, drop the field and the EDGAR skill will ask when it first needs one.

Say the honest caveat that goes with the branch you are on, in one clause rather
than a paragraph. **In Claude Code:** the header gets set exactly, so the address
is used on every EDGAR call. **In Cowork:** a web fetch tool sends its own
`User-Agent` and usually will not let you change it, so the address is recorded
for the day this desk runs in Claude Code rather than applied here. Ask for it
anyway, because the profile travels and the analyst should not have to be asked
twice.

## The profile block

Both environments write the same block, with the same marker lines, so a later
run of this interview can find it and update it in place. The markers are HTML
comments, which stay invisible when the file is rendered.

Get today's date from the environment before you write it. Your own sense of the
date is not evidence, and a remembered date in someone's durable config is worse
than no date. **In Claude Code:** run `date -u +%F`. **In Cowork:** take it from
whatever the session context states about today's date. If nothing in the
environment states it, ask in one short line and move on.

These are the exact marker lines and the exact shape of the block:

```
<!-- BEGIN lacuna desk profile -->
## Lacuna desk profile

_Written by `/lacuna:interview` on <YYYY-MM-DD>. Edit these lines freely. Notes
you want to keep across re-runs go outside the markers, because re-running the
interview replaces everything between them and nothing outside them._

**Verified enough:** <what has to be true before a claim counts as solid>

**Trusted sources:** <list>

**Distrusted or flag-on-sight sources:** <list>

**Deep dive versus quick read:** <the rule, with an example of each>

**Memo shape:** <length, conclusion-first or reasoning-first, hedging taste>

**Probabilities:** <how to express them, base rates, confidence figures>

**Standing interests:** <venues, sectors, tickers, cases, permanent ones marked>

**Current file:** <what is on the desk this month, if it was named>

**Pet peeves:** <list, in their words where possible>

**Working notes:** <habits, conventions, folders, who work goes to>

**SEC contact email:** <the address to send as the EDGAR User-Agent contact>
<!-- END lacuna desk profile -->
```

Fill it with the actual answers, in their words where you can, in plain prose.
Short is fine. A line the analyst recognises as their own is worth more than
three lines of your paraphrase. Drop any field there was nothing to say about
rather than padding it.

Now follow the branch for the environment you detected.

---

## In Claude Code: write it into the global CLAUDE.md

The interview is worth nothing if it lives only in this conversation. Write it
into the **global** memory file so it applies in every project, on every repo, in
every session.

**Step 1. Read the existing file first.** Read `~/.claude/CLAUDE.md`. If it does
not exist, you will create it with just the block above. If it does exist, read
all of it before writing anything. There is other content in there that matters
and it is not yours to touch.

**Step 2. Place the block idempotently.**

- If both marker lines are already present in the file, this is a re-run and
  something is about to be destroyed. Show the analyst the current block content
  first, say that re-running replaces all of it, and ask whether anything in there
  is worth keeping. Move anything they want kept to outside the markers before you
  write. Then replace only the text between the markers, markers included, and
  leave every other byte of the file exactly as it was. Do not reorder, reformat,
  or reflow the surrounding content.
- If both markers are absent, append the block to the end of the file with one
  blank line before it.
- If exactly one of the two markers is present, stop. A half-written or
  hand-trimmed section is not something you can safely guess the boundary of.
  Show the marker line you found, say which one is missing, and ask whether to
  treat the rest of the file as profile text to replace or to repair the missing
  marker by hand first.
- If either marker is present more than once, or the END marker appears before
  the BEGIN marker, stop. Do not guess. Show the confusing lines and ask which
  block to replace.
- Never delete or rewrite content outside the markers, and never replace the
  whole file with your own version of it. Do the write as a targeted string
  replacement of the old marked section (`Edit`, old string starting at the
  BEGIN marker and ending at the END marker) or as an append. Never a
  whole-file `Write`, because that puts every other byte in the file at the
  mercy of your recollection of it.

**Step 3. Confirm you broke nothing.** Read the file back. Check that the
content above the BEGIN marker and below the END marker is byte-identical to what
you read in Step 1, and that the file still ends where it should. If anything
outside the markers moved, say so plainly and restore it from what you read in
Step 1 before going on. Only report the profile as written once this check
passes.

**Step 4. Offer the project-level copy, with the warning attached.** Ask whether
the block should also go into the current project's `./CLAUDE.md`, which is
useful when a project has its own narrower conventions. Say the thing that is
easy to miss before writing anything: `./CLAUDE.md` is usually tracked in git and
shared with everyone else working on the repo, so a profile written there means
personal preferences, distrusted sources, and standing positions can be committed
and pushed. Check first and report what you found: `git ls-files --error-unmatch
CLAUDE.md` succeeding means the file is already tracked, and `git check-ignore -q
CLAUDE.md` succeeding means it is ignored and safe. Then ask. If the answer is
yes, write the same block into that file under the same markers, following the
same idempotency rules; if the project file does not exist, creating it is fine.
If the answer is no, leave it, and say that the global file covers every project
anyway.

---

## In Cowork: write a file, state the facts, say where memory lives

Cowork has no `CLAUDE.md` and no `~/.claude` directory, so there is no global
config file to edit. Three things take its place, and you do all three.

**(a) Write `desk-profile.md` in the current working folder.** Same block, same
marker lines, so a later run of this interview finds it and updates it in place.

- First check whether `desk-profile.md` already exists in this folder, and read
  it if it does.
- If it exists and carries both markers, this is a re-run. Show the analyst the
  current block content, say that re-running replaces all of it, and ask whether
  anything in there is worth keeping; move what they want kept to outside the
  markers first. Then replace only the text between them, markers included, and
  leave the rest of the file exactly as it was. Someone may have added their own
  notes around it, and someone may have added notes inside it too.
- If it exists with neither marker, append the block at the end with one blank
  line before it.
- If it exists with exactly one marker, or with a marker repeated, or with END
  before BEGIN, stop and ask which block to replace rather than guessing the
  boundary.
- If it does not exist, create it with a `# Desk profile` heading line, a blank
  line, then the block.

Tell them the filename and the one-line reason it is a file: it is plain
markdown they can read, edit, move, or delete, and re-running the interview
updates it in place instead of piling up a second copy.

**(b) State the durable facts back in the conversation, compactly and
explicitly.** Cowork builds a memory profile from what is said in conversations,
so saying the facts plainly is what makes them stick. After writing the file,
post a short block of flat declarative lines, in the first person about the
analyst, with no hedging and no narrative wrapping. Something in this shape:

> Recording these as standing preferences for future sessions:
> - I treat a claim as verified only when the primary document is in hand.
> - I want memos of one screen or less, conclusion in the first line.
> - I want probabilities as numbers with the main driver named.
> - I distrust <sources> and want them flagged whenever cited.
> - I permanently follow <venues, sectors, tickers, cases>.
> - My SEC EDGAR contact address is <address>.

Use their actual answers. Keep each line to one fact so nothing gets lost in a
compound sentence.

Then, in one sentence, tell them where that memory lives and how to be certain
of it: Cowork keeps a memory profile it distils from conversations, viewable and
editable at the profile icon > Settings > Capabilities > Memory, and pasting the
profile block in there is the way to be sure of it rather than trusting the
distillation.

**(c) Say what makes it apply, and be precise about it.** One short paragraph, and
no overselling. Cowork does not auto-load any file, so what makes this profile
apply is that the skills on this desk open `desk-profile.md` from the working
folder themselves before they write anything the analyst reads. Two consequences
worth stating plainly:

- Keep the file in the folder you actually work in. Moved somewhere else, it is
  a document rather than a profile.
- Work you do in a different folder starts without it, so either copy the file
  across or paste the block into the Memory page, which is not folder-scoped.

---

## Close

Two sentences summarising what you learned, in your own words, specific enough
that the analyst can tell whether you were listening. Something like: "So:
primary documents or it does not count, memos short with the answer at the top,
probabilities as numbers with the driver named, and never open a message by
telling you what you just said. Standing interests are Delaware Chancery,
appraisal cases, and anything touching the two tickers you named."

Then say where it went, in the wording that matches the branch you took.

**In Claude Code:** "That is saved to your global `CLAUDE.md`, so it applies
everywhere from now on. Edit it whenever it stops being true."

**In Cowork:** "That is saved as `desk-profile.md` in this folder, and the skills
on this desk read it from here before they write anything for you. Edit it
whenever it stops being true. I have also stated the facts back in the
conversation, which is what Cowork's memory distils from; if you want to be
certain of them rather than trusting that, paste the block into profile icon >
Settings > Capabilities > Memory yourself."

Then point onward, in either case: "If you have not run `/lacuna:start` yet,
that is the five-minute tour of what this desk can actually do."
