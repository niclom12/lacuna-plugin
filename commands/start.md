---
description: A five-minute plain-language orientation. What this desk can do, how to talk to it, the controls that apply in your environment, where case files live, and how to connect the free court-data server. Works in Cowork and in Claude Code.
---

# Orientation

Walk the user through the tour below. Keep it to about five minutes of reading.
Deliver it in your own voice, in short chunks, and stop for questions whenever
one comes. The user is smart and new to this, so no jargon without a
plain-English gloss, and no apologising for the tool. Address the user as "you"
throughout.

## Step 0. Work out which environment this is, then say so once

This plugin runs in two places and the practical controls differ. Settle which
one you are in before you start talking, by looking rather than by asking.

**The decisive observation is the terminal.** Look at your own toolset for a shell
or Bash tool. Cowork has no terminal, so if one is there this is **Claude Code**,
and that settles it on its own.

**The confirming observation is the global context file.** Try to read
`~/.claude/CLAUDE.md`, counting it as present if it reads back and also if the
file is absent but `~/.claude/` exists.

If there is no shell, this is **Cowork**, where you have file creation and web
access, no terminal, and no `~/.claude`. If there is a shell but the read of
`~/.claude/CLAUDE.md` was refused, left unapproved, or came back absent, this is
still Claude Code: a denied permission prompt is not evidence about the
environment. Never ask the user a technical question to decide this.

State it once, in a sentence, then move on:

> One thing first so I give you the right instructions: this is Claude Code, so
> the controls I describe are the terminal ones.

or

> One thing first so I give you the right instructions: this is Cowork, so I
> will skip the terminal material and stick to what you actually have.

Then show only the branch for that environment. Do not narrate the other one,
and do not present both and let the user pick.

## Before you talk: look at what is actually installed

Describe the real set of skills you found. Do not describe a set you remember.

**In Claude Code:** list the directories under `${CLAUDE_PLUGIN_ROOT}/skills/`
and read the `description` line out of each `SKILL.md`, then list
`${CLAUDE_PLUGIN_ROOT}/agents/` and do the same. That path is this plugin's own
install directory and it is filled in for you before you read this; the session's
working directory is the user's project, so never reach for a bare relative path
like `skills/`.

**In Cowork:** you cannot list a directory with a shell command, and
`${CLAUDE_PLUGIN_ROOT}` may not resolve. The plugin's skills are already present
in your own list of available skills, so read the names and one-line descriptions
from there and use those.

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

There is also a docket sweep across every case the desk tracks: what was filed
since the last check, the dated events worth a look, and a written report. The
method is a skill, `docket-sweep`, so it loads in both environments and asking for
it in plain language is what starts it. Something like "sweep the dockets for
everything we track and tell me what moved since Friday".

**In Claude Code** there is one extra piece: `docket-watcher`, a subagent that does
nothing but load that skill and run it, so the sweep reads several hundred docket
entries in its own context window and this conversation receives only the report.
Mention any other subagents you found the same way.

**In Cowork** subagents bundled in a plugin are not something to rely on yet, so
that wrapper may not be loaded. The sweep is unaffected, because the method is in
the skill rather than in the wrapper. The same request gets the same procedure and
the same report, read in this conversation instead of in a separate one.

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
- **Redirect early.** Stop me and say the new direction the moment you see one.
  A wrong turn caught in thirty seconds costs nothing. In Claude Code the key
  for that is Escape.
- **Push back.** "Where did that number come from" and "which of those did you
  actually look up" are the two most useful sentences you can type, and I
  should always be able to answer both.
- The slash commands are only shortcuts to longer instructions. Everything they
  do, you can also just ask for.

---

# Branch A. In Claude Code

Use sections 3A to 5A only when you detected Claude Code.

## 3A. Permissions, and turning the prompts down

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
`rm`, `sed`). It does **not** cover network access. EDGAR fetches go through
`WebFetch` by default and through `curl` when a shell is the better route, and
accept edits covers neither, so in that mode every fetch still prompts. Flipping
to accept edits and expecting quiet EDGAR work is the disappointment worth heading
off.

**Per-tool rules are what kill the repeat prompts.** This is the durable fix and
the right one for the fetching. Because the fetching arrives by two routes, the
durable fix needs a rule for each. Two ways to get there:

- When a prompt appears, pick the **"Yes, don't ask again"** option rather than
  plain yes. For a shell command that rule is saved for good, into
  `.claude/settings.local.json` at the root of the repo you are working in, and
  it holds in later sessions there. For a file edit it only lasts until the
  session ends.
- Or write the rules yourself. `/permissions` opens the standing rules and lets
  you add, inspect, and remove them; the same rules can be typed straight into
  `.claude/settings.json` in the project. The shape for the EDGAR and court work,
  covering both routes, where the shell form of an EDGAR call is
  `curl -s -A "$SEC_UA" <url>`:

  ```json
  {
    "permissions": {
      "allow": [
        "WebFetch(domain:www.sec.gov)",
        "WebFetch(domain:data.sec.gov)",
        "WebFetch(domain:efts.sec.gov)",
        "WebFetch(domain:*.courtlistener.com)",
        "Bash(curl -s -A *)"
      ]
    }
  }
  ```

  Say the honest caveat with it. That last rule matches the command shape and
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

## 4A. Plan mode, for the bigger asks

For anything with real stakes or several steps, plan mode is the good habit.
`Shift+Tab` round to plan mode, or just say "plan this first, do not do it
yet". I research and come back with an approach; nothing gets written or run
until you approve it.

Worth it when the question is expensive to get wrong, when you know something
about the trade that is not in any document, or when you want to see my
reasoning before I spend twenty minutes on it. Skip it for a lookup.

## 5A. The memory files are yours

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

---

# Branch B. In Cowork

Use sections 3B to 5B only when you detected Cowork. There is no terminal here,
no permission-mode cycle, and no settings file to edit, so none of that is worth
describing. What follows is what actually applies.

## 3B. How this plugin is installed and managed

Everything on this desk arrived as one plugin, and the place to see it is
**Customize > Plugins**.

- **Browse plugins** lists what is available in the public directory and installs
  with a click. This desk is not in that directory, so searching it for `lacuna`
  finds nothing.
- A **marketplace** can be synced from a GitHub repository or a git URL, which is
  how this plugin got here, how anyone else installs it, and how you would pick up
  a new version of it.
- A custom plugin file can also be uploaded directly.
- The same panel is where you see what is installed, and where you turn a plugin
  off if you want a session without it.

One thing worth knowing so nothing surprises you later: plugins are currently
saved locally to your own machine. A colleague does not get this desk because
you installed it. Sharing across an organisation is coming, and until then the
route to a second person is that they sync the same marketplace or install the
same file.

## 4B. Connectors, and how tools get switched on

The outside data this desk reaches comes through connectors that ship with the
plugin. The one that matters here is CourtListener, and section 7 below covers
what it holds.

Describe the outcome to look for rather than a menu path, because the exact
wording of the panel moves. What you are checking is that the CourtListener tools
appear in the tool list for the session. If they do, it is connected and the first
use will open a browser page to sign in once. If they do not, it needs enabling,
and the likely place for that is this plugin's own entry under
**Customize > Plugins**.

Say the recovery line too, so a hunt for a toggle that is somewhere else is not a
dead end: if those tools never appear, I will tell you plainly rather than
pretending, work the legal questions over the open web instead, and tag every fact
`[web, verify]` so you know the authoritative source was not used.

## 5B. The memory profile

There is no `CLAUDE.md` file in Cowork. Instead, Claude keeps a memory profile
distilled from your conversations, and you can read and edit it at the **profile
icon > Settings > Capabilities > Memory**. Anything in there shapes future
sessions.

Two practical consequences worth passing on:

- Saying a preference plainly and directly is how it gets remembered. "I want
  memos of one screen, conclusion first, and probabilities as numbers" is more
  likely to stick than the same taste implied across ten messages.
- If you want to be certain of something rather than trusting the distillation,
  open that Memory page and write it there yourself.

`/lacuna:interview` is ten minutes of questions about how you work. In Cowork it
saves the answers as `desk-profile.md` in the folder you are working in, and states
them back in the conversation, which is the raw material the memory profile is
distilled from. Two honest notes on how it then applies: the skills on this desk
open that file themselves before writing anything for you, so it is present in the
session if you keep it in the folder you work in, and pasting the same block into
the Memory page is the only way to be sure of it rather than trusting the
distillation.

## Invoking the commands

Type `/` and the command list appears; this plugin's entries are prefixed with
`lacuna`, so `/lacuna:start` is this tour and `/lacuna:interview` is the
interview. Every command is just a longer instruction written down, so anything a
command does you can also ask for in your own words.

---

# Both environments

Sections 6 to 8 apply everywhere.

## 6. Where the case files live

Work on a tracked case accumulates in a `cases/` folder inside whatever project
or folder you are working in: `cases/<case-id>/memo.md` for the thesis and the
verified facts, `cases/<case-id>/chronology.md` for the dated spine, docket
sweeps in `cases/reports/`. The case-id is a short slug we agree on, something
like `acme-appraisal`. You do not have to build any of it in advance, because I
create the folder the first time there is something to put in it. Ask for a
briefing on a case with nothing on file and I will say so rather than inventing
one.

That convention is the whole filing system. It means a case picked up three
months from now starts from what was actually verified rather than from memory,
and it means you can read the files without me.

## 7. Connecting the court data

Federal court records come from CourtListener, run by the non-profit Free Law
Project. The plugin ships the connection; you just have to approve it once.

**In Claude Code:** type `/mcp` to see the servers available, select
**CourtListener**, and the first time it is used it opens a browser page to sign
in and authorise.

**In Cowork:** the sign-in works the same way, and the thing to check is that the
CourtListener tools are in the session's tool list. Where they are missing, the
connector needs enabling, and the likely place is this plugin's entry under
**Customize > Plugins**. If they do not appear after that, say so plainly and fall
back to the open web with every fact tagged `[web, verify]`.

Either way it is a one-time sign-in. After that it stays connected and you never
see it again.

It is **free**. There is no card and no trial. Two things to set expectations:
it covers federal courts, so state trial courts are largely missing, and the
document archive is contributed by users, so a filing nobody bought may not be
there. Both of those show up as coverage limits in anything I write.

## 8. Where to read more

There is a short pointer page called `useful-things.md`, in this plugin's `docs/`
folder. Read it if you want the detail, or take the summary: the court data
sources including the commercial option for state courts, the two Anthropic repos
this plugin borrowed skills from and what else is in them, keyless ways into SEC
EDGAR, and links to the documentation on skills, plugins, and memory. Worth ten
minutes when you are curious rather than working.

**In Claude Code** the path is `${CLAUDE_PLUGIN_ROOT}/docs/useful-things.md`, so
just ask me to read it. **In Cowork**, if that path does not resolve, the same
file is readable in the plugin's repository at
`https://github.com/niclom12/lacuna-plugin/blob/main/docs/useful-things.md`.

---

## Close

Ask if anything was unclear, and answer it. Then, unless the interview has
already been run, point at it:

> If you have not run `/lacuna:interview` yet, that is the other ten minutes
> worth spending. It asks how you decide something is verified, which sources
> you trust, how long you want memos, how you want probabilities put, and the
> contact address the SEC wants on an EDGAR request. Then it writes the answers
> into a desk profile that later sessions read, so you never explain it twice.

If it has already been run, say so, say where the profile lives (the global
`CLAUDE.md` in Claude Code, `desk-profile.md` in the working folder in Cowork),
and offer to start on something real instead.
