# Useful things

Pointers only. Everything below is either something this plugin
already leans on, something it borrowed from, or something worth knowing exists
when the desk runs into a wall. Read it when you are curious rather than when
you are working.

## CourtListener, and the hosted MCP server

CourtListener is run by the [Free Law Project](https://free.law/), a US
non-profit, and it is the backbone of the legal side of this desk: federal
dockets, opinions, oral arguments, judges, and a citation lookup that will tell
you whether a case you have been handed actually exists. It offers a hosted MCP
server at `https://mcp.courtlistener.com/`, which is how this plugin talks to it
and which is already declared in the `.mcp.json` here. Connect it with `/mcp`,
pick **CourtListener**, approve the browser sign-in once, and it stays connected.
It is free, and two limits are worth internalising: coverage is federal, so state
trial courts are mostly absent, and resolving a citation proves the case is real
without telling you whether it is still good law. For state trial courts there is
[Trellis](https://trellis.law/), which is commercial and paid, and which would
be the thing to add if a case you care about turns out to live in a county
superior court. Nothing in this plugin talks to Trellis today.

## anthropics/claude-for-legal

<https://github.com/anthropics/claude-for-legal>, Apache-2.0. Anthropic's open
collection of legal skills for Claude. Two of the skills here come from its
`litigation-legal` plugin: `chronology` and `matter-briefing`, both rebuilt for a
trading desk by stripping the attorney framing (privilege gates, work-product
headers, advocacy posture) and keeping the method. The CourtListener MCP server
entry in this plugin's `.mcp.json` comes from there too. Every adapted file
carries a provenance comment at the top saying exactly what changed. The wider
repo is aimed at people practising law rather than trading around it: drafting,
review, discovery, and matter-management workflows. Browse its `skills/`
directories for the current list, since it moves. The skills are plain markdown,
so anything useful can be dropped into `~/.claude/skills/` by hand.

## anthropics/financial-services

<https://github.com/anthropics/financial-services>, Apache-2.0. The same idea for
finance. `earnings-analysis` here is adapted from its `earnings-reviewer` plugin
and `equity-research` from the `initiating-coverage` skill in its equity-research
plugin, in both cases with the docx and xlsx output, the chart packs, and the paid
data-platform dependencies removed, and with a litigation angle added because that
is why this desk opens a 10-Q at all. The wider repo covers the workflows a
research or investment team runs day to day, which is a much broader brief than
sizing legal exposure. Worth a browse when you want something quantitative this
desk does not cover.

## The superpowers plugin

<https://github.com/obra/superpowers>, MIT, by Jesse Vincent, and available
through the official Claude Code plugin marketplace. It is a large library of
process skills: brainstorming before building, test-driven development,
systematic debugging, verifying before claiming completion, dispatching
parallel agents. It is written for software work, and it is the best available
demonstration of the idea that a skill is just written discipline the model
reads. This plugin's `verification-habits` skill is adapted from its
`verification-before-completion` skill, with attribution and the licence copied
into `licenses/`. Installing superpowers alongside lacuna is a reasonable
thing to do; the two do not collide.

## SEC EDGAR full-text search

EDGAR full-text search needs no key and no account. The human interface is at
<https://www.sec.gov/edgar/search/> and searches the text of filed documents
back to 2001. The JSON endpoint behind it is
`https://efts.sec.gov/LATEST/search-index?q=<your+terms>`, which accepts the
same filters the UI shows (form type, date range, company) and returns
structured hits you can work with programmatically. Two conditions: the SEC
requires a descriptive `User-Agent` header with a contact email on every
automated request, and it asks that you stay under roughly ten requests a
second. Alongside it, `data.sec.gov` serves per-company structured data with no
key either, including `submissions/CIK##########.json` for a filing history and
`api/xbrl/companyfacts/CIK##########.json` for every reported XBRL fact. Those
three endpoints between them cover most of what this desk needs from the SEC.

## The RECAP archive

<https://www.courtlistener.com/recap/>. PACER, the federal courts' own docket
system, charges by the page. RECAP is the free archive of documents that other
people have already paid for: a browser extension uploads a copy whenever a
user buys a filing, and CourtListener serves it back to everyone. This is why
some dockets on CourtListener have every PDF attached and others have only the
entry text. A document being missing means nobody bought it yet rather than it
not existing. Installing the RECAP extension is worth it if you ever pay PACER
directly, since it contributes what you buy back to the commons.

## eyecite

<https://github.com/freelawproject/eyecite>. A Python library, also from the
Free Law Project, that pulls legal citations out of raw text: full cites, short
cites, supra, id, and the tangle of reporter formats they come in. If you ever
want to check a long document mechanically rather than by reading, this is the
tool that turns prose into a list of citations you can then resolve against
CourtListener one by one. It is the programmatic version of what
`verification-habits` asks for by hand.

## Claude Code documentation

Three pages worth reading, in this order. Skills, at
<https://docs.claude.com/en/docs/claude-code/skills>, explains the format every
practice file in this plugin uses, and how Claude decides to load one. Memory,
at <https://docs.claude.com/en/docs/claude-code/memory>, explains `CLAUDE.md`
and the difference between the global file and a project file. Plugins, at
<https://docs.claude.com/en/docs/claude-code/plugins>, explains how a bundle
like this one is put together and how to make your own. If you only read one,
read the memory page, because that file is the highest-leverage thing on this
desk that you control directly.
