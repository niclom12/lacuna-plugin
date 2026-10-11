---
name: add-monitor
description: "Use when the person asks to monitor, watch, track or be alerted about something: a company or topic in the news, a court docket or case, a prediction market, a web page, or a state court case. Sends news and court docket requests to the news-watch skill, where the person sets them up themselves. For a prediction market, a web page or a state court case, gathers the few details a monitor needs and drafts a short, ready-to-send request to Nic, who sets those monitors up. Works in Cowork and in Claude Code."
---

<!-- Original to lacuna. -->

# Adding a monitor

The Lacuna desk runs several kinds of monitor. Two of them the person sets up
themselves, through the news desk connection: a news watch on a company or
topic, and a watch on a federal court docket. The others (prediction market
alerts, web page change alerts, state court case alerts) are set up by Nic on
the desk's own machines. This skill sorts the request, sends news and dockets
to the right place, and turns everything else into a short request Nic can act
on without writing back with questions.

Be honest about that split. Never say or imply that a market, page or state
court monitor has been set up, is pending, or will start on its own.

## Writing rules

The person may never have opened a terminal, so nothing technical reaches
them: no internal names, no field names, no raw output, no commands.

- Never use the em dash character, and never the antithesis pattern.
- Short plain sentences.
- Every reply ends with two lines, `Done:` and `Recommended:`. The one
  exception is a question you are waiting on, which ends with the question.
- An error is one or two plain sentences plus who to ask, which is Nic.

## Step 1. Sort the request

- **A company or topic in the news** ("watch Northwind Kettle Works", "tell me
  when there is news on the ferry strike"): hand over to the `news-watch` skill
  and follow it from "Watching a company". If the news desk is not connected,
  that skill hands over to `news-connect`. Nothing else in this skill applies.
- **A federal docket or case** ("alert me on filings in case 1:26-cv-00000",
  "watch the Ninth Circuit appeal 25-8059", "track the cert petition 26-299"):
  hand over to the `news-watch` skill and follow it from "Watching a court
  docket". That covers the federal district courts, the circuit courts and the
  Supreme Court. If the news desk is not connected, that skill hands over to
  `news-connect`. If the connection turns out to be read-only, or the docket
  tools refuse it, come back here and use the docket branch below instead.
- **A prediction market** ("tell me when this market moves"): the market
  branch.
- **A web page** ("alert me when this page changes"): the page branch.
- **A state court case** ("watch this county court case"): the state court
  branch.

If it is unclear, ask one question: "Is this about news coverage, a court case,
a prediction market, or a web page?"

## Step 2. Gather the minimum, one question at a time

Ask only for what is missing. If the person already gave it, do not ask again.

- **Docket** (only when the person cannot add it themselves, see Step 1): the
  case number and the court ("1:26-cv-00000, District of Delaware"). The party
  names help if they have them.
- **Prediction market:** the link to the market. Optionally the price or move
  they care about ("tell me if it crosses 70 cents").
- **Web page:** the page's address, and which part of the page matters if it is
  not the whole page.
- **State court case:** the state, the court, and the case number.

For every kind, also ask for **one sentence on what a change would mean** to
them: "What would it mean for you if this moved?" That sentence is what turns an
alert into something they can act on, and Nic needs it.

## Step 3. Draft the request

Write it ready to paste, addressed to Nic, in this shape:

```
Hi Nic,

Please could you set up a prediction market alert for me.

Market: https://polymarket.com/event/northwind-kettle-works-merger-closes-by-june-30
What to watch: a move above 70 cents on YES
Why it matters: a close above 70 would mean the market expects the merger to clear, and I would trim the position.

Thanks,
<their name>
```

Change the first line and the fields to fit the kind: "a page change alert"
with the page address and the part of the page, "a state court case monitor"
with state, court and case number, or "a docket monitor" with the case and
court when the person could not add it themselves. Leave `<their name>` for them to fill in
unless they told you their name.

## Step 4. Say plainly what happens next

After the draft, two short lines:

> Done: I have drafted the request above; Nic sets up this kind of monitor
> himself, so nothing is watching it yet.
> Recommended: send it to Nic however you normally reach him.

Do not send it anywhere yourself, and do not offer to. Never say the request
has been sent. For a market, a page or a state court case, never say or imply
that the person could set it up themselves; for a docket, the one thing that
would let them is a news desk code that can make changes, from Nic.
