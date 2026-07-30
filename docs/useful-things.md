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

## The Cowork plugin directory

<https://claude.com/plugins>. The browsable directory of plugins for Claude
Cowork, and the same list you see from **Customize > Plugins > Browse plugins**
inside Cowork itself. Worth a look for two reasons. It shows what other people
have decided is worth bundling, which is a fast education in what a plugin is
good for, and it is where you install anything you did not write yourself. This
plugin is not in the directory: it installs by pointing Cowork at this
repository's git URL, which syncs the marketplace manifest at
`.claude-plugin/marketplace.json`. One thing to know before you rely on a
plugin here: plugins currently save locally to the machine you install them on,
with org-wide sharing coming later, so a colleague installs their own copy
rather than picking up yours.

## anthropics/knowledge-work-plugins

<https://github.com/anthropics/knowledge-work-plugins>. Anthropic's own
collection of plugins built for Claude Cowork, which its README notes are also
compatible with Claude Code. This is the most useful reference in this file for
anyone extending lacuna, because it is the working answer to "what is a Cowork
plugin allowed to be". The answer turns out to be modest: markdown and JSON, no
code, no infrastructure, no build step. Skills, slash commands, connector
declarations in `.mcp.json`, and sub-agents, in the same directory layout Claude
Code uses. Read one of its plugins end to end before writing your own, and note
how much of the value sits in carefully written prose rather than in machinery.
The plugins themselves cover general knowledge work (documents, decks, research
workflows) rather than anything litigation-specific, so they complement this desk
instead of overlapping with it.

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
so anything useful can be lifted by hand. In Claude Code, drop a skill folder
into `~/.claude/skills/`. In Cowork, add it to a plugin you own and reinstall
that plugin from Customize > Plugins, since there is no local skills folder
to copy into.

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

## Documentation worth reading

Three Claude Code pages, in this order. Skills, at
<https://docs.claude.com/en/docs/claude-code/skills>, explains the format every
practice file in this plugin uses, and how Claude decides to load one. That
format is the same one Cowork reads, so this page is worth reading whichever
environment you work in. Memory,
at <https://docs.claude.com/en/docs/claude-code/memory>, explains `CLAUDE.md`
and the difference between the global file and a project file. Plugins, at
<https://docs.claude.com/en/docs/claude-code/plugins>, explains how a bundle
like this one is put together and how to make your own. If you only read one,
read the memory page, because a durable profile is the highest-leverage thing on
this desk that you control directly.

The memory page describes a Claude Code path specifically. Cowork has no
`CLAUDE.md` file and no `~/.claude` directory, and its equivalent is Claude's own
Memory profile, a picture of how you work that Claude distils from your
conversations. You can read it, correct it, and delete from it at **profile icon
> Settings > Capabilities > Memory**. Reading what it has written about you after
a week of real work is instructive, and it is where a standing preference belongs
in Cowork. `/lacuna:interview` also writes a `desk-profile.md` into your
workspace, which is a file you own outright and can edit with no interpretation
in between.
