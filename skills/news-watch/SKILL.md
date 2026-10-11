---
name: news-watch
description: "Use when the person asks what the news is on a company, which companies the news desk is watching, or whether the news desk is running; wants to start, change, pause, resume or stop watching a company or a court docket; wants a company's news sent to their email or phone, or stopped; says the news is noisy, about the wrong company, or that one outlet should be quietened or checked more or less often. Works through the Lacuna news desk connection. Drafts everything itself, reads it back as one plain sentence, and saves only on a yes. Needs the news desk connected (the news-connect skill), which works in Claude Code."
---

<!-- Original to lacuna. Ported from the desk's private news-watch skill, which
     stays the source of truth; a test in the private repository fails when the
     tool names here drift from the desk's, or when this file stops describing
     notify handling or set_source_interval. -->

# The news desk

The Lacuna news desk reads a few dozen news outlets, runs searches, and reads
companies' own filings, and keeps the stories about each company on its list.
Each company on the list is a **watch**. This skill is how a person asks what
the news is, adds a company, changes where its news goes, and pauses, quietens
or stops a watch.

The person has never opened a terminal and should never need to. This file
keeps two things apart. **What you do** is technical and is for you: tool
names, field names, the shape of a call. **What you say** is the only part
that reaches the person, and it is plain.

## What you say, always

- No technical words. Not slug, alias, query, CIK, ticker field, JSON, tool,
  server, token, MCP, endpoint, feed id, interval, override. Say "the company",
  "the names it goes by", "the searches", "its own filings", "the news
  outlet", "how often it is checked".
- Never show raw output, a list of fields, or an error trace. Say what it
  means.
- Never use the em dash character, and never the antithesis pattern. Short
  sentences. Name real things: company names, outlets, dates, story counts.
- **Every reply ends with two lines.** After a change, or a refused change,
  those two lines are the whole reply:

  > Done: Northwind Kettle Works is now being watched, and news starts
  > arriving within about ten minutes.
  > Recommended: ask "any news on Northwind Kettle" tomorrow to see what it
  > found.

  After a question ("what is the news on X"), the answer comes first and the
  two lines close it: Done says what was looked at ("Done: checked the last
  seven days of Northwind Kettle news."), Recommended says the one useful next
  thing. The one exception is a read-back that is waiting for a yes: it ends
  with "Save it?" or "Go ahead?", and the two lines come after the person
  answers.
- An error is one or two plain sentences plus who to ask, which is Nic. Never
  a cause the person cannot act on.
- **Nothing is saved without a yes.** Adding or changing a watch starts real
  checking and real alerts. Read the draft back as one plain sentence, wait,
  then save.

## Before anything: is the desk connected?

**In Cowork** the news desk is not available yet. Say in one sentence that it
needs Claude Code for now, give the two lines, and stop.

**In Claude Code**, look for the `mcp__lacuna-news__` tools in your tool
list. If they are missing, hand over to the `news-connect` skill. Never answer
a news question from memory or from a web search and present it as though it
came from the desk.

## What you do: the tools

Reading, available to every connection:

- `mcp__lacuna-news__search_news` finds stories, one row per story.
- `mcp__lacuna-news__get_story` opens one story: every outlet that carried it,
  the relevance verdicts, and the article text when the desk fetched it.
- `mcp__lacuna-news__list_news_watches` lists the watches, how much each is
  finding, and its `notify` block: the email addresses and WhatsApp numbers
  its alerts go to beyond the desk, both lists always present and possibly
  empty.
- `mcp__lacuna-news__news_status` reports feed health, mutes, check timings
  (`interval_s` and any `interval_override_s` per feed), and whether stories
  are being judged.

Writing, which needs write access:

- `mcp__lacuna-news__add_news_watch`
- `mcp__lacuna-news__update_news_watch`
- `mcp__lacuna-news__pause_news_watch`
- `mcp__lacuna-news__resume_news_watch`
- `mcp__lacuna-news__remove_news_watch`
- `mcp__lacuna-news__mute_source`
- `mcp__lacuna-news__unmute_source`
- `mcp__lacuna-news__set_source_interval`

Court docket watches, on the same connection:

- `mcp__lacuna-news__list_courts` lists the courts a docket watch can use.
  Reading.
- `mcp__lacuna-news__list_docket_watches` lists every docket watch, with its
  `id`, docket number, case, who its alerts go to, and whether it is paused.
  Reading.
- `mcp__lacuna-news__add_docket_watch`, `mcp__lacuna-news__update_docket_watch`,
  `mcp__lacuna-news__pause_docket_watch`, `mcp__lacuna-news__resume_docket_watch`
  and `mcp__lacuna-news__remove_docket_watch` change them. Writing.

### Read-only connections

New people get read access by default. A write tool called on a read
connection comes back with a plain result containing `"error": "token cannot
write"`. When that happens, stop. Do not retry, and do not try another write
tool to get around it. Say:

> Not saved: this connection can read the news but cannot add or change
> anything.
> Recommended: ask Nic for a news desk code that can make changes, then say
> "connect the news" and paste it.

**Before drafting any change**, find out whether this connection can write,
so the person never approves something that cannot be saved. Read the record
file the connect step wrote, with its output kept to yourself:

```bash
cat "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/lacuna-news.json" 2>/dev/null || echo none
```

If it says `"access": "read"`, or a write was refused earlier in this
session, say this first and then ask whether they still want to see the
draft:

> One thing first: this connection can read the news but cannot add or change
> anything, so I can draft this but not save it. Do you still want the draft,
> or shall I stop here?

If it says `write`, or the file is missing, go ahead and draft.

### The desk's own rules, so you can explain them

- A new watch starts being checked within about ten minutes. The first pass
  over each feed is filed quietly, so a new watch never floods anyone with old
  stories.
- One development sends one email. A ruling written up by nine outlets is one
  alert; the other eight arrive the next day as a single follow-up naming them.
  Nothing is thrown away, it is grouped.
- Every alert is read before it is sent. The desk fetches the article, puts it
  in front of a model with the recent headlines on that case, and asks whether
  this is a material development. Nothing goes out that has not been through
  that, including the company's own filings and wire releases.
- Email addresses on a watch get every alert the desk gets for it.
- A WhatsApp number gets far less: only a story judged to matter that was
  published within the last 48 hours, and a short roll-up on a busy day. Old
  stories never buzz a phone. A WhatsApp group can be a recipient too, written
  as its group id, `120363000000000000@g.us`.
- Feeds are checked on the desk's own schedule. A person can change one feed's
  timing between once a minute and once a day; the desk will not go faster
  than once a minute so the news sites do not block it.
- The desk itself always gets every alert, whatever a person sets for
  themselves.

## Asking what the news is

Triggers: "what is the news on Northwind Kettle", "any news this week", "what
companies are being watched", "what is the latest on the first company".

**What you do.**

1. If they named no company, or you do not know its slug, call
   `list_news_watches` first. The slug is the `slug` field; never say it.
2. Call `search_news` with `watch` set to the slug, and `since` when they
   named a period. Add `q` for a topic inside the watch, and `semantic: true`
   when the topic is an idea rather than a word ("anything on the plant
   closure").
3. Use `get_story` when they ask about one story. The article text is often
   only a stub, because many outlets serve almost nothing to a plain fetch.
   Say the text is not available rather than summarising a stub as though it
   were the article.
4. If a search finds nothing, call `news_status` so you can say whether quiet
   means no news or a desk that is not checking.

**What you say.** One line per story, newest first, with the desk's reason
underneath when it gave one:

> 9 Sep, Reuters, carried by 3 outlets: Northwind Kettle Works wins state
> approval for new plant.
> The approval is the decision this watch is waiting for.

The outlet count matters: three outlets carrying a story within an hour is
itself information. A story with no reason underneath has not been sorted for
importance yet; say so rather than leaving a blank. Never show a story's id or
any other number from the result that is not a date or a count.

Then, always, the two lines, even after a question:

> Done: checked the last seven days of Northwind Kettle news.
> Recommended: ask "open the plant approval story" if you want the full
> article.

When listing the companies, say each name in plain words with how many stories
it found this week, and whether any is paused.

## Watching a company

Triggers: "watch Northwind Kettle Works", "add Harbourlight Ferries to the
news", "start tracking news on Quillfeather Paper".

### What you do: draft everything yourself

- **Slug**: the company name in lowercase with hyphens, punctuation dropped.
  `Northwind Kettle Works` becomes `northwind-kettle-works`. Check
  `list_news_watches` with `status: all` first; if the company is already
  there, offer to resume or change it instead of adding it twice.
- **Name**: what a person calls it, "Northwind Kettle Works".
- **Aliases** are the words that must appear in a headline or summary for a
  story to be kept. Draft three or four: the legal name as filed ("Northwind
  Kettle Works Inc."), the short name people write ("Northwind Kettle"), and a
  well-known product or case name if one is always in the headlines. A company
  whose name is a common word needs the longer form and never the bare word.
  Never put the ticker in the aliases.
- **Tickers** are the exchange symbols in capitals, one per listing (an ADR
  counts separately). The desk looks for them in the article text only where
  the writing marks them as a ticker (`$NWKW`, `(NWKW)`, `NASDAQ: NWKW`,
  `NWKW shares`), so a short ticker cannot match an ordinary word. Leave them
  out for a private company.
- **Queries** are Google News searches, run about every ten minutes. Draft two
  or three, each pairing a name with what matters: `"Northwind Kettle" plant`,
  `"Northwind Kettle" (lawsuit OR recall OR ruling)`. Keep them narrow; a
  search on the bare name returns the whole business press.
- **CIKs**: the SEC's number for the company, digits only. With it the desk
  picks up the company's own filings within a minute of them posting, and they
  are then read and judged like any other story before anything is sent. Look it up in the SEC's
  ticker file, `https://www.sec.gov/files/company_tickers.json`, following the
  `edgar-research` skill for the contact address the SEC requires on the
  request. A private or non-US company has none; that is fine.
- **`what_moves_it`**: one or two sentences on the news that would actually
  matter to this person. Every headline is compared against it, and a vague
  sentence is what makes a watch noisy. Write it from what the person said
  about why they care. If they said nothing, ask one short question: "What
  news on them would matter to you?"
- **`notify`**: ask once, in these words or close to them: "Where should the
  news go: an email address, a WhatsApp number, both, or just the desk?"
  "Just the desk" is the default and needs no field. Build
  `{"emails": [...], "whatsapp": [...]}` from the answer. The desk refuses a
  number that is not in international form with the plus sign
  (`+14155550123`) and an email that does not look like an address, so read
  back exactly what they gave you, and if the desk refuses it, ask them to
  check it rather than guessing a correction. Take the address or number as
  given: do not question whether it is real, and do not comment on its
  domain or provider. If they gave the destination in the same breath as the
  company, do not ask again.

### What you say: read it back as one sentence, then wait

The read-back is one sentence (two at most, for something unusual) and the
question "Save it?". No bullets, no headings, no lists of searches. The person
is approving the idea, and the detail stays with you.

> I will watch for news on Northwind Kettle Works (also written Northwind
> Kettle), search for anything on its new plant and any lawsuit or recall,
> pick up its own filings, treat a decision on the plant or a product recall
> as the news that matters, and send everything to the desk and to
> jo@example.com. Save it?

Add one short sentence for anything unusual: no filings because it is a
private company, or a name that could be confused with something else. Then
stop and wait.

On a no, change what they asked for and read the whole sentence back again.
Never save a partly agreed draft.

### What you do: save on a yes

Call `add_news_watch` with `slug`, `name`, `aliases`, `tickers`, `queries`,
`ciks`, `what_moves_it` and, when they named an address or a number, `notify`.
Confirm from what the tool returned rather than what you sent, because the
desk tidies the fields. Say where the news goes in the first line:

> Done: Northwind Kettle Works is now being watched, with news going to the
> desk and to jo@example.com; it starts within about ten minutes, and the
> first pass is filed quietly so you are not flooded with old stories.
> Recommended: ask "any news on Northwind Kettle" tomorrow to see what it has
> found.

## Sending a company's news to me, or stopping it

Triggers: "send Northwind to my phone", "email me the Harbourlight news",
"also send Quillfeather to Sam", "stop sending Northwind to me", "take me off
the Harbourlight alerts", "stop texting me about Quillfeather".

**What you do.**

1. Call `list_news_watches` and read the watch's `notify`: its current
   `emails` and `whatsapp` lists.
2. Build the new set. `notify` replaces the whole set, so an added number is
   the old numbers plus the new one, and a dropped address is the old list
   without it. Stopping everything for this person is
   `{"emails": [], "whatsapp": []}` when they are the only recipient, or the
   remaining recipients when they are not. If you do not know which address
   or number is theirs, ask.
3. Read it back as one sentence and wait for a yes.
4. Call `update_news_watch` with the slug and `notify` only.

**What you say.** For adding a phone:

> Northwind Kettle news will go to the desk, to jo@example.com, and to your
> phone on +14155550123. Your phone only gets the stories that matter and are
> fresh; the email gets everything. Save it?

For stopping:

> You will stop getting Northwind Kettle news yourself. The desk still gets
> everything and the company is still being watched. Go ahead?

Then the two lines, for example:

> Done: Northwind Kettle news no longer comes to you; the desk still gets it
> and the watch is still running.
> Recommended: say "pause Northwind" if you want the watching itself to stop.

## Pausing, resuming and removing

**What you do.**

- **Pause** stops checking and keeps everything: the watch, its settings, its
  recipients and its stories. `pause_news_watch`, then `resume_news_watch` to
  start again.
- **Remove** stops the watch for good. The stories it already found stay
  searchable. `remove_news_watch`. Removing does not clear the recipients on
  the watch record; if the person wants their address or number gone as well,
  clear `notify` with `update_news_watch` first, then remove.

**What you say.** "Stop watching Harbourlight" could mean either, so say which
one you are about to do and why, and wait for a yes:

> I can pause Harbourlight Ferries, which keeps everything so you can pick it
> up again, or remove it, which stops it for good but keeps the stories it
> already found. Pause it?

Then the two lines:

> Done: Harbourlight Ferries is paused; its settings and stories are kept.
> Recommended: say "resume Harbourlight" when it matters again.

## Watching a court docket

A docket watch emails every new filing on one court case. It runs on the desk's
court monitor, not the news feeds, and the same connection changes it.

**What you do.**

1. Call `list_courts`. A district court in `rss_feeds` is read from the court's
   own feed. `scotus` is the Supreme Court. Any other court goes through
   CourtListener under its court id: `ca9` is the Ninth Circuit, `ca2` the
   Second, `cadc` the D.C. Circuit, `nysd` the Southern District of New York.
2. Ask who should get the alerts, if they did not say. Left out, they go to the
   desk's usual list.
3. Read it back as one sentence and wait for a yes.
4. Call `add_docket_watch` with `court`, `case_number`, and `alert_to` and `case`
   when known. CourtListener finds the docket from the court and number. If it
   finds none or several, say what it found and ask; never guess a docket id.
5. Leave `name_regex` out unless they ask for it. A loose name pattern alerts on
   other cases that share a party's name.

**What you say.**

> I'll watch the Ninth Circuit docket 25-8059, EDC v. PHMSA, and email new
> filings to you. Go ahead?

Then the two lines:

> Done: 25-8059 is watched from now on; what is already on the docket is not
> emailed, only new filings.
> Recommended: say "show my docket watches" to see them all.

**Changing, pausing and removing.** Call `list_docket_watches` for the `id`
first. `update_docket_watch` changes the label, the case, the recipients or a
pattern; an empty `alert_to` list goes back to the usual list.
`pause_docket_watch` keeps it and stops the alerts; `resume_docket_watch` starts
it again. `remove_docket_watch` deletes it for good, so say that and wait for a
yes. Every change is live within a minute, and the desk is told who changed what.

## Changing what is watched

Triggers: "Northwind also trades as Kettle Co now", "add their new product
name", "what matters has changed".

**What you do.** Call `update_news_watch` with the slug and only the fields
that change: `name`, `aliases`, `queries`, `tickers`, `ciks`,
`what_moves_it`. A list replaces the old list, so send the whole list.

**What you say.** Read the change back as one sentence, save on a yes, then
the two lines.

## When the news is noisy or about the wrong thing

Triggers: "these are about the wrong Harbourlight", "too many alerts",
"stop that outlet", "this is all repeats".

**What you say first.** Ask which of these it is, because each fix is
different: the stories are about something else with the same name; the
stories are about the right company and just do not matter; or one outlet
keeps repeating itself.

**What you do.**

- **Something else with the same name.** "Harbourlight" might also be a
  lighthouse museum. Call `update_news_watch` with `negative_aliases`,
  sending the whole list: `["Harbourlight Museum"]`. Say plainly what will
  now be thrown away, because a phrase that is too broad silently loses real
  news:

  > From now on any story mentioning "Harbourlight Museum" will be ignored
  > for this company. Go ahead?

- **Real news that does not matter.** Sharpen `what_moves_it` with
  `update_news_watch` so it says more exactly what would matter; the desk's
  sorting then cuts the rest. Read the new sentence back and save on a yes.

- **One outlet repeating itself.** Call `news_status`, find the feed by name,
  and call `mute_source` with `name` and `hours` (default 24, at most 720).
  Nothing is lost: the outlet is still read and its stories stay searchable;
  it just stops sending alerts for that long. Part of a name mutes every feed
  containing it, so check what matched before you confirm. `unmute_source`
  lifts it early.

  > I will quieten Business Wire for a day. Its stories are still collected,
  > they just will not alert anyone until tomorrow. Go ahead?

Every one of these is a change, so it ends with the two lines.

## Checking an outlet more or less often

Triggers: "check that feed less often", "check Northwind's searches every 20
minutes", "that outlet matters this week, check it more".

**What you do.**

1. Call `news_status` and find the feed or feeds: the `id`, `name`,
   `interval_s`, and whether `interval_override_s` is already set. A company's
   searches are the feeds whose `watch` is its slug; a request about "that
   company's feeds" means each of those.
2. Say the current timing and the new one back in plain words, and wait for a
   yes.
3. Call `set_source_interval` once per feed with `source` (the `id`, which is
   safest because names can repeat) and `seconds`. The desk accepts 60 to
   86400; the tool refuses anything outside that. Pass `seconds: null` to put
   a feed back on its normal timing. A shorter timing takes effect at once; a
   longer one starts after the check already booked. The change survives a
   restart of the desk.

**What you say.**

> Northwind Kettle's three searches are checked every 10 minutes now. Change
> them to every 20 minutes?

If they ask for faster than once a minute or slower than once a day:

> The desk will not go faster than once a minute, so the news sites do not
> block us, and it will not go slower than once a day. I can set it to once a
> minute. Go ahead?

Then the two lines:

> Done: Northwind Kettle's searches are now checked every 20 minutes.
> Recommended: say "put Northwind's searches back to normal" whenever you want
> the usual timing again.

## When something looks wrong

Call `news_status` before guessing. Plain readings:

- A feed failing a few times and backing off is being blocked for a while by
  the site. One such feed is not an outage. Say "one outlet is not answering
  at the moment, which the desk handles on its own".
- A feed listed as muted is quiet on purpose.
- A large queue of unjudged stories with both relevance providers unavailable
  means no alert is going out at all. Every alert now waits to be read and
  judged, filings included, so there is nothing that skips the queue. Nothing
  is lost: the stories wait and go out once a provider answers. Say exactly
  that, and that Nic will know about it.
- If the collector has not reported in for a long while, say "the desk has not
  checked in recently" and tell the person to let Nic know.

If the tools do not answer at all:

> The news desk is not answering just now.
> Done: nothing changed.
> Recommended: try again in a few minutes, and tell Nic if it keeps happening.
