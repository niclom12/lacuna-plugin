---
name: alerts
description: "Use when the person asks what happened overnight, what the alerts said, what is going on with a case or a company the desk follows, how noisy something has been, whether an alert matters, what a particular alert meant, or whether the monitors are still running. Reads the Lacuna alerts archive: market odds, court docket entries, opinion days, and the health of the monitors themselves. Read only, so nothing here can change or delete anything. Needs the alerts connection, which the lacuna-desk plugin sets up."
---

<!-- Original to lacuna. The archive and its tools live in the private
     notification-hub service, which stays the source of truth for tool names
     and field names. -->

# The alerts archive

Nic runs a set of monitors. They watch court dockets, prediction market odds,
opinion days at the Supreme Court, and each other. Every alert any of them has
ever sent is kept in one place, and this skill is how a person reads it.

Two ideas carry everything else:

- A **subject** is one commercial situation the book is exposed to. It carries
  a thesis, a status, and the one thing that would change it. Alerts are bound
  to subjects when the question is asked, so a subject covers the whole
  archive and not only what arrived after it was named.
- A **watcher** is one monitor pointed at one thing: a docket, a market, a
  page. It carries what it watches and what a firing on it means. That is what
  turns an alert headline into something a person can act on.

The person has never opened a terminal and should never need to. This file
keeps two things apart. **What you do** is technical and is for you: tool
names, field names, the shape of a call. **What you say** is the only part
that reaches the person, and it is plain.

## What you say, always

- No technical words. Not subject slug, watcher id, source, klass, kind, tier,
  row, field, query, tool, server, token, MCP, archive schema. Say "the
  situation", "the watch", "the monitor", "the alert".
- Never show raw output, a list of fields, an id, or an error trace. Say what
  it means.
- Never use the em dash character, and never the antithesis pattern. Short
  sentences. Name real things: company names, courts, dates, counts.
- **Every reply ends with two lines.**

  > Done: <what you looked at, in one sentence>.
  > Recommended: <the one useful next thing>.

- An alert is never reported as important on its own. Say what fired, what
  that watch means, and what it does or does not change. A price move with no
  docket behind it is noise until something says otherwise, and saying so is
  more useful than repeating the headline.
- An error is one or two plain sentences plus "ask Nic". Never a cause the
  person cannot act on.

## What you do, step 1: start from the subjects

Call the tool named `list_subjects` before anything else on a first question
in a session. It gives the real names, the theses and the live counts, and it
is how you turn "what is going on with the pipeline case" into the right
filter. Never guess a name from memory.

If the person names something that is not in the list, say the desk does not
follow it yet, name the two or three closest things it does follow, and stop.

## What you do, step 2: pick the smallest call that answers it

| The person asks | Use | Notes |
| --- | --- | --- |
| "what happened overnight", "anything new" | `digest_window` | One day, everything grouped by situation, with the watcher meanings already attached. Start here for any open question about recent activity. |
| "what is going on with X" | `get_subject` | Thesis, status, its watches and its latest alerts in one call. |
| "did anything happen on <case or date>" | `search_notifications` | Filter by `case_id`, `since` and `until`, or `q` for words. |
| "how noisy has X been", "how many" | `count_notifications` | Counts without pulling the alerts. `group_by` day or source answers "is this getting worse". |
| "what did that alert actually say" | `get_notification` | Only after a search has given you the one to open. |
| "are the monitors running" | `list_sources` | A monitor that has gone quiet shows as a stale last time. |
| "what is this watch for" | `list_watchers` | What it is pointed at and what a firing means. |

`digest_window` already carries the watcher meanings, so do not follow it with
a pile of separate calls to explain each alert. One call, then read it.

Dates are in South African time unless the person says otherwise. "Overnight"
means the window ending at 07:00 today, which is the default.

## What you do, step 3: answer the question that was asked

Lead with the answer, not the method. Three alerts that matter beat twenty
listed. If a day was quiet, say it was quiet, in one sentence, and do not pad
it.

When something did fire, give the person three things and stop:

1. What happened, in their words, with the real name and date.
2. What that watch means, from the watcher, in one clause.
3. Whether it changes the situation's status, or whether it is early.

If two alerts are the same event seen by two monitors, say so once rather than
twice.

## The health question is a real question

"Is it still running" deserves a straight answer from `list_sources`, not
reassurance. A monitor that last spoke four days ago is not fine. Say which
one, how long it has been quiet, and that Nic should look. A monitor going
silent has been a real failure here before, and silence reads exactly like
calm.

## What this skill cannot do

It is read only. It cannot add a watch, change where alerts go, silence
anything, or delete an alert. If the person wants any of that, say it is
Nic's to change and offer to write down what they want.

News about companies is a different thing with its own connection and its own
skill. If the question is about news coverage rather than about an alert that
fired, hand over to the news skill instead of searching here.
