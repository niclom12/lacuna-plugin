---
description: A five-minute plain-language orientation. What this desk can do, how to talk to it, how permissions and plan mode work, where case files live, and how to connect the free court-data server.
---

# Orientation

Walk the user through the tour below. Keep it to about five minutes of reading.
Deliver it in your own voice, in short chunks, and stop for questions whenever
one comes. The user is smart and new to this, so no jargon without a
plain-English gloss, and no apologising for the tool. Address the user as "you"
throughout.

Before you start talking, look at what is actually installed. List the
directories under `${CLAUDE_PLUGIN_ROOT}/skills/` and read the `description`
line out of each `SKILL.md`, then list `${CLAUDE_PLUGIN_ROOT}/agents/` and do
the same. That path is this plugin's own install directory and it is filled in
for you before you read this; the session's working directory is the user's
project, so never reach for a bare relative path like `skills/`. Describe the
real set you found in section 1. Do not describe a set you remember.

---

## 1. What is on this desk

There is no engine here. There is a set of written practices that get loaded
into my context when they are relevant, and reading them changes how I work.

Name every skill you found, one line each, saying what it changes about my
output rather than restating its description. They sort roughly into three
groups, so use those as headings: the **legal** side (dockets, opinions,
citations, timelines, case briefings), the **company** side (SEC filings,
quarterly results, company notes), and the **practice** (how a task gets sized,
how claims get checked, how a long session stays cheap).

Mention the subagents you found under `${CLAUDE_PLUGIN_ROOT}/agents/` too. Same
idea in a separate context window:
`docket-watcher` sweeps every case the desk tracks, pulls what was filed since
the last check, flags the dated events worth a look, and writes a report. Say
that asking for "any new filings" or "sweep the dockets before the open" is what
starts it.

Then say the honest thing about all of it: these are prose files, I read them,
they work because they are good advice. Nothing in this plugin blocks me or
checks up on me. If a memo is wrong, the fix is that you say so.

## 2. How to talk to me

Say what you want, the way you would to a competent colleague. There is no
syntax to learn and no keyword that unlocks a better mode.

> "Pull the docket for the Delaware appraisal case against X and tell me what
> happened at the last hearing."

> "Read the last two 10-Qs for TICKER and tell me if the litigation reserve
> moved."

> "Is this actually verified or are you guessing?"

Things worth saying explicitly:

- **Specific beats polite.** "Two paragraphs, conclusion first, links on every
  fact" gets a better answer than "please do a good job".
- **Context is free.** Telling me why you are asking, what you already believe,
  and what you would do with the answer changes the answer for the better.
- **Interrupt me.** Press Escape and redirect. A wrong direction caught in
  thirty seconds costs nothing.
- **Push back.** "Where did that number come from" and "which of those did you
  actually look up" are the two most useful sentences you can type, and I
  should always be able to answer both.
- The slash commands are only shortcuts to longer instructions. Everything they
  do, you can also just ask for.

## 3. Permissions, and turning the prompts down

By default I ask before I do anything that touches your machine or the network:
writing a file, running a shell command, fetching a page. That is deliberate for
the first few sessions, because watching the approvals is how you learn what I
actually do. This default is called **Manual** mode, and the status line at the
bottom of the screen shows `⏸ manual mode on`.

Once you trust the shape of it, the prompts become friction. Three ways to turn
them down, and they do different things.

**`Shift+Tab` cycles the mode.** It steps Manual → accept edits → plan mode and
back around, and the status line names the one you are in: `⏵⏵ accept edits on`,
`⏸ plan mode on`. Be precise about what accept edits covers, because the obvious
guess is wrong. It auto-approves my file writes and edits inside the working
directory, plus a handful of filesystem commands (`mkdir`, `touch`, `mv`, `cp`,
`rm`, `sed`). It does **not** cover network access. This desk does every EDGAR
fetch with `curl`, so in accept edits mode those still prompt, every one of them.
Flipping to accept edits and expecting quiet EDGAR work is the disappointment
worth heading off.

**Per-tool rules are what kill the repeat prompts.** This is the durable fix and
the right one for the fetching. Two routes to it:

- When a prompt appears, pick the **"Yes, don't ask again"** option rather than
  plain yes. For a shell command that rule is saved for good, into
  `.claude/settings.local.json` at the root of the repo you are working in, and
  it holds in later sessions there. For a file edit it only lasts until the
  session ends.
- Or write the rules yourself. `/permissions` opens the standing rules and lets
  you add, inspect, and remove them; the same rules can be typed straight into
  `.claude/settings.json` in the project. The shape for the EDGAR work, where
  every call this desk makes is `curl -s -A "$SEC_UA" <url>`:

  ```json
  {
    "permissions": {
      "allow": [
        "Bash(curl -s -A *)",
        "WebFetch(domain:www.sec.gov)",
        "WebFetch(domain:*.courtlistener.com)"
      ]
    }
  }
  ```

  Say the honest caveat with it. That first rule matches the command shape and
  not the destination, so it allows that curl form against any URL. Rules that
  try to pin the URL down are unreliable, because a redirect, a shell variable,
  or an extra flag walks straight past them. If the goal is a narrower network
  rather than fewer prompts, the tool for that is a `deny` rule.

**Auto mode, if the account has it.** When it is available it appears in the
`Shift+Tab` cycle and the status line reads `⏵⏵ auto mode on`. Instead of
prompting you, a separate classifier model reviews each action first and blocks
anything that escalates beyond what you asked for. Read-only HTTP requests are
allowed by default in it, which is most of what this desk does. It is the least
interrupted way to work and it is not a safety guarantee, so it suits a long
research run better than a first session.

Two caveats over all of it. Auto-accepting edits means I can overwrite a file
without asking first, so keep the work in a folder that is in git or backed up.
And I stay exactly as capable of being wrong with the prompts off, so the
verification habits matter more once they are down rather than less.

Suggest staying in Manual today, and turning things down after a run has gone
the way you expected.

## 4. Plan mode, for the bigger asks

For anything with real stakes or several steps, plan mode is the good habit.
`Shift+Tab` round to plan mode, or just say "plan this first, do not do it
yet". I research and come back with an approach; nothing gets written or run
until you approve it.

Worth it when the question is expensive to get wrong, when you know something
about the trade that is not in any document, or when you want to see my
reasoning before I spend twenty minutes on it. Skip it for a lookup.

## 5. The memory files are yours

Two plain markdown files, both editable, no special format:

- `~/.claude/CLAUDE.md` applies to every project on this machine. Standing
  preferences go here.
- `./CLAUDE.md` in a project folder applies to that project. Narrower
  conventions go here.

I read them at the start of every session and follow what is in them. If you
write "never open a reply by restating my question" in there, that is the end of
it. `/lacuna:interview` writes your working style into the global file for you,
but hand-editing is entirely fine and often faster. Suggest opening the global
one at some point and looking, so it is clear that it is a text file rather than
a setting.

## 6. Where the case files live

Work on a tracked case accumulates in a `cases/` folder inside whatever project
you are working in: `cases/<case-id>/memo.md` for the thesis and the verified
facts, `cases/<case-id>/chronology.md` for the dated spine, docket sweeps in
`cases/reports/`. The case-id is a short slug we agree on, something like
`acme-appraisal`. You do not have to build any of it in advance, because I
create the folder the first time there is something to put in it. Ask for a
briefing on a case with nothing on file and I will say so rather than inventing
one.

## 7. Connecting the court data

Federal court records come from CourtListener, run by the non-profit Free Law
Project. The plugin ships the connection; you just have to approve it once.

Type `/mcp` to see the servers available. Select **CourtListener**, and the first
time it is used it opens a browser page to sign in and authorise. After that it
stays connected and you never see it again.

It is **free**. There is no card and no trial. Two things to set expectations:
it covers federal courts, so state trial courts are largely missing, and the
document archive is contributed by users, so a filing nobody bought may not be
there. Both of those show up as coverage limits in anything I write.

## 8. Where to read more

`${CLAUDE_PLUGIN_ROOT}/docs/useful-things.md` is a short pointer page. Read it
if you want the detail, or take the summary: the court data sources including
the commercial option for state courts, the two Anthropic repos this plugin
borrowed skills from and what else is in them, keyless ways into SEC EDGAR, and
links to the Claude Code documentation on skills, plugins, and memory. Worth ten
minutes when you are curious rather than working.

---

## Close

Ask if anything was unclear, and answer it. Then, unless the interview has
already been run, point at it:

> If you have not run `/lacuna:interview` yet, that is the other ten minutes
> worth spending. It asks how you decide something is verified, which sources
> you trust, how long you want memos, how you want probabilities put, and the
> contact address the SEC wants on an EDGAR request. Then it writes the answers
> into your global CLAUDE.md so every session starts knowing them.

If it has already been run, say so, say where the profile lives, and offer to
start on something real instead.
