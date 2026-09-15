---
name: setup
description: "Use when someone has just installed the lacuna plugin and wants to get going, says they were told to run the setup, asks what to do first, or asks how to start using the news. Confirms the desk is loaded, connects the news desk with the code Nic sent, handles the restart, and says in plain words what to ask for next. Works in Claude Code. In Cowork it sets up everything except the news desk, which needs Claude Code for now."
---

<!-- Original to lacuna. -->

# First time setup

This is the first thing a person runs after installing the plugin. It gets
them from "it is installed" to "I can ask it things", and the only thing they
ever type is the news desk code Nic sent them.

The person may never have opened a terminal. This file keeps two things
apart. **What you do** is technical and is for you. **What you say** is the
only part that reaches them, and it is plain.

## What you say, always

- No technical words at all. Not plugin file, marketplace, server, token,
  key, MCP, command, terminal, shell, settings file, restart the process. Say
  "the desk", "your code", "the news desk", "close Claude Code and open it
  again".
- Never show raw output, an address, a command, or an error trace.
- Never use the em dash character, and never the antithesis pattern. Short
  plain sentences.
- **Every reply ends with two lines.** The only exception is a question you
  are waiting on, which ends with the question.

  > Done: <what happened, in one sentence>.
  > Recommended: <the one thing to do next>.

- An error is one or two plain sentences plus "ask Nic".

## Step 1. What you do: confirm the desk is actually loaded

Do this by looking rather than by asking.

**Which environment is this?** Look at your own toolset for a shell or Bash
tool. A shell means Claude Code. No shell means Cowork. Never ask.

**Is the desk here?** In Claude Code, list the skill directories:

```bash
ls "${CLAUDE_PLUGIN_ROOT}/skills"
```

In Cowork, `${CLAUDE_PLUGIN_ROOT}` may not resolve, and the plugin's skills
are already in your own list of available skills, so read them from there.

If the skills are not there at all, the install did not take.

> The desk is not loaded here yet. That usually means Claude Code needs
> closing and opening again after installing.
> Done: nothing is set up yet.
> Recommended: close Claude Code, open it again, and say "set up the desk".
> If it still is not here, ask Nic.

If they are there, say so in one line and go on. Do not list them all here,
because `/lacuna:start` is the tour and this is the setup.

> The desk is loaded. It can read court records, read company filings, and
> follow the news.

## Step 2. What you do: the news desk code

**In Cowork**, say this and go to step 4:

> The news desk needs Claude Code for now, so it is not available here.
> Everything else on the desk works.

**In Claude Code**, load the `news-connect` skill and follow it from its step
1. That skill is the one authority on the code flow: it works out whether the
news desk is already connected, whether a connection is saved but not loaded
yet, and whether there is no connection at all. It asks for the code, checks
it, saves it, and handles a cut-off or refused code in one plain sentence
each. Do not repeat any of that logic here, and never ask for or repeat the
code yourself.

If the person has no code, `news-connect` already tells them to ask Nic for
"a news desk code". Add one sentence they will find useful:

> Market data is a separate thing from the news, and Nic sends a separate
> code for that one.

## Step 3. The restart

`news-connect` ends with its own connected message, and that message already
includes the restart. Do not repeat it in different words. The one thing
worth adding, if the person sounds worried about losing something:

> Nothing is lost by closing it. The companies being watched live on the news
> desk rather than on your computer.

Stop there. Everything after the restart happens in the next session.

## Step 4. What you say: what to ask for next

Close with examples they could type, not a description of what the desk can
do. Pick the branch that applies.

**If the news desk connected:**

> Once you have closed Claude Code and opened it again, you can say things
> like:
>
> - "what is the news on Acme"
> - "what companies are being watched"
> - "watch Acme"
> - "send Acme to my phone"
>
> Done: the desk is set up and the news desk is connected for you.
> Recommended: close Claude Code, open it again, and ask "what companies are
> being watched".

**If there is no news code yet, or this is Cowork:**

> You can already say things like:
>
> - "pull the court file on the Acme appraisal case and tell me what happened
>   at the last hearing"
> - "read Acme's last two quarterly reports and tell me if the legal reserve
>   moved"
> - "write me a note on Acme with a link on every fact"
>
> Done: the desk is set up and ready to use.
> Recommended: type `/lacuna:start` for a five minute tour, and ask Nic for a
> news desk code when you want the news as well.
