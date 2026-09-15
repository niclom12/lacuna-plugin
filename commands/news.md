---
description: The one door to the news desk. Connects it if it is not connected yet, and otherwise says in three plain lines how it is doing and what you can ask for. Works in Claude Code; in Cowork it says the news desk needs Claude Code for now.
---

# The news desk

This is the page a person is pointed at when they have never used the news
desk. They may never have opened a terminal. Everything you say to them is
plain: no technical words, no commands, no addresses, no raw output. If a
message needs a technical word, it is the wrong message.

Every reply ends with two lines: `Done:` and `Recommended:`.

## Step 0. Which environment is this?

Look at your own toolset for a shell or Bash tool, exactly as `/lacuna:start`
does. A shell means Claude Code. No shell means Cowork. Never ask.

**In Cowork**, say this and stop:

> The news desk needs Claude Code for now, so it is not available here.
> Done: nothing changed.
> Recommended: open Claude Code and type `/lacuna:news` there.

## Step 1. Is the desk connected?

**Connected** means the `mcp__lacuna-news__news_status` tool is in your own
tool list and answers when called. Call it. If it answers, go to step 3.

If it is not in your list, or it is there but fails, load the `news-connect`
skill and follow it from its step 1. That skill works out whether a
connection is saved but not loaded yet (in which case the person needs to
close Claude Code and open it again), whether there is no connection at all
(in which case it asks for the code, or tells them to ask Nic for "a news
desk code"), and it handles a cut-off or refused code with one plain sentence
each. Do not repeat that logic here; hand over.

**If the person has no code at all**, that is the common case for someone who
has only just installed the desk, and the answer is one sentence:

> The news desk needs a code, which Nic sends you privately. It is one long
> line of letters and numbers.
> Done: nothing changed, because connecting needs a code.
> Recommended: ask Nic for "a news desk code" and paste it here when it
> arrives.

Market data is a separate system with its own code, so if they mention it,
say that Nic sends a separate code for that one.

## Step 2. After connecting

The `news-connect` skill ends with its own connected message, including the
restart. Stop there. The status in step 3 is for the next session, once the
tools have loaded.

## Step 3. The three-line status

From the `news_status` result, and from `list_news_watches` when you need the
names, say three lines:

1. **How many companies.** "The news desk is following 12 companies." Name
   two or three of them if there are more than three, all of them if fewer.
   Mention any that are paused.
2. **Is everything running.** "Everything is running" when `failing_sources`
   is empty, `last_heartbeat_age_s` is under 1800, and neither provider in
   `providers` has an `unavailable_until` in the future. Otherwise one plain
   clause: "one or two news outlets are not answering at the moment, which
   the desk handles on its own"; "the desk has not checked in recently, so
   tell Nic"; "stories are arriving but are not being sorted for importance
   right now, which Nic will know about".
3. **Whether this person can add companies.** Read the record file
   `lacuna-news.json` next to the person's Claude Code settings (in
   `${CLAUDE_CONFIG_DIR:-$HOME/.claude}`), which the connect step wrote. If
   `access` is `write`: "You can add and change companies." If `read`: "You
   can read the news; adding or changing companies needs a different code
   from Nic." If the file is missing: "I will find out whether you can add
   companies the first time you ask; if not, I will say so."

Then offer the four things they can say next, as plain sentences they could
type:

> From here you can say:
> - "what is the news on <company>"
> - "watch <company>"
> - "send <company> to my phone" or "to my email"
> - "pause <company>" or "stop watching <company>"

Close with the two lines:

> Done: checked the news desk.
> Recommended: try "what is the news on <the first company>".

Never print the raw status, the tool result, a count of feeds by name, or any
address. The `news-watch` skill carries everything that happens after this
page.
