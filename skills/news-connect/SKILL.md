---
name: news-connect
description: "Use when the person wants to connect to the Lacuna news desk, has a news desk code from Nic to paste, asks how to get one, asks why the news is not working, or wants to disconnect. Takes the code, checks it works, saves the connection for this person only, and says in plain words what they can now do. Works in Claude Code. The news desk is not available in Cowork yet, and the skill says so."
---

<!-- Original to lacuna. -->

# Connecting the news desk

The Lacuna news desk follows a list of companies across a few dozen news
outlets and the companies' own filings, and keeps the stories that matter. Nic
runs it. To use it a person needs a **news desk code**: one line of letters
and numbers that Nic sends them privately. The code starts `lacuna-news:v1:`.

The person you are talking to has never opened a terminal and should never
need to. This file keeps two things apart. **What you do** is technical and is
for you. **What you say** is the only part that reaches the person, and it is
plain.

## What you say, always

- Never say, and never paste into the conversation: the contents of the code,
  any address inside it, any command, any raw output, or an error trace. Do not
  decode the code to "have a look".
- No technical words at all. Not server, token, key, MCP, header, JSON, scope,
  transport, config, terminal, shell. Say "the news desk", "your code", "the
  connection".
- Never use the em dash character, and never the antithesis pattern. Short
  plain sentences.
- Every reply ends with two lines, and after a change those two lines are the
  whole reply:

  > Done: <what happened, in one sentence>.
  > Recommended: <the one thing to do next>.

- An error is one or two plain sentences plus who to ask, which is Nic. Never
  give a cause the person cannot act on.
- The one exception to the two lines is a question waiting for a yes, such as
  whether to replace an existing connection: it ends with the question, and
  the two lines come after the person answers.

## What you do, step 0: which environment is this?

Look at your own toolset for a shell or Bash tool, exactly as `/lacuna:start`
does. A shell means **Claude Code**. No shell means **Cowork**. Never ask the
person a technical question to decide this.

**In Cowork**, say this and stop:

> The news desk needs Claude Code for now, so it is not available here.
> Done: nothing changed.
> Recommended: open Claude Code, say "connect the news" there, and paste the
> same code.

Do not suggest a workaround, and do not ask for the code in Cowork.

## What you do, step 1: is it already connected?

In Claude Code, first look for `mcp__lacuna-news__news_status` in your own
tool list. If it is there, the desk is connected and answering in this
session. Call it, then report with the "connected" message in step 4, without
the restart sentence, and with ACCESS filled in from the record file described
in step 3 (or "I will find out whether you can add companies the first time you
ask" when that file is missing).

If the tool is not in your list, check whether a connection is saved but not
loaded yet. Throw the output away, because it would show the code's contents:

```bash
claude mcp get lacuna-news >/dev/null 2>&1 && echo saved || echo none
```

- `saved`: a connection exists from an earlier session. Say:

  > You are already connected. If you have a new code from Nic I can replace
  > the old connection with it; your companies and settings live on the desk,
  > so nothing is lost either way. Do you want to replace it?

  Replace only on a clear yes. On a no, or if the person just wants the news:

  > Done: nothing changed; the news desk is connected.
  > Recommended: close Claude Code, open it again, and ask "what companies are
  > being watched".

- `none`: go to step 2.

## What you do, step 2: get the code

If the person has not pasted a code yet, ask for it:

> Paste the news desk code Nic sent you. It is one line starting with
> `lacuna-news:v1:`.

If they do not have one:

> Done: nothing changed, because connecting needs a code.
> Recommended: ask Nic for "a news desk code" and paste it here when it
> arrives.

Before using what they paste, keep only the characters `A-Z a-z 0-9 : _ -`.
A real code contains nothing else, and this keeps a stray quote or space from
breaking anything. Never repeat the code back.

## What you do, step 3: check it and save it, in one command

Run this once, with the cleaned code in place of `CODE`. Set `REPLACE=1` only
when the person said yes to replacing an existing connection. It decodes the
code, proves it works by asking the desk for its status, and only then saves
the connection for this person (user scope, so every project they open has
it). It prints one line of `name=value` pairs and nothing else, and none of
those values is secret.

It also writes two small things next to the person's Claude Code settings,
neither of which carries anything secret:

- `lacuna-news.json`, holding only the access level and the name that came
  in the code. `/lacuna:news` reads it later to say whether the person can add
  companies, because the desk itself does not report that in its status.
- A fenced section in the global `CLAUDE.md` there, between
  `<!-- lacuna-news:start -->` and `<!-- lacuna-news:end -->`, telling every
  later session to load the `news-watch` skill before touching a news tool.
  Without it a session answers news questions straight from the tools and
  none of the plain-words rules apply. The section is replaced on
  reconnect and removed on disconnect, and nothing outside the markers is
  touched, exactly as `/lacuna:interview` treats its own section.

The format of the code is checked against `connection_code.py` in the desk's
own repository; it has not changed since 0.4.0.

```bash
LACUNA_CODE='CODE' MODE=connect REPLACE=0 python3 - <<'PY'
import base64, json, os, subprocess, sys, time, urllib.request, urllib.error
mode = os.environ.get("MODE", "check")
out = {}
def done(**kw):
    out.update(kw); print(" ".join(f"{k}={v}" for k, v in out.items())); sys.exit(0)
code = os.environ.get("LACUNA_CODE", "").strip().strip("'\"")
p = "lacuna-news:v1:"
try:
    assert code.startswith(p)
    r = code[len(p):]
    d = json.loads(base64.urlsafe_b64decode(r + "=" * (-len(r) % 4)))
    url, tok = d["url"], d["token"]
    assert url.startswith("http") and tok and " " not in tok
except Exception:
    done(result="malformed")
access = d.get("access", "unknown")
out["access"] = access
def rpc(body, sid=None):
    h = {"Authorization": "Bearer " + tok, "Content-Type": "application/json",
         "Accept": "application/json, text/event-stream"}
    if sid: h["Mcp-Session-Id"] = sid
    req = urllib.request.Request(url, json.dumps(body).encode(), h)
    with urllib.request.urlopen(req, timeout=20) as resp:
        raw = resp.read().decode()
        if raw.startswith("event:") or raw.startswith("data:"):
            raw = [l[5:] for l in raw.splitlines() if l.startswith("data:")][-1]
        return json.loads(raw), resp.headers.get("Mcp-Session-Id")
try:
    init, sid = rpc({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
        "protocolVersion": "2025-06-18", "capabilities": {},
        "clientInfo": {"name": "lacuna-news-connect", "version": "1"}}})
    res, _ = rpc({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                  "params": {"name": "news_status", "arguments": {}}}, sid)
except urllib.error.HTTPError as e:
    done(result="unauthorized" if e.code in (401, 403) else f"server_error_{e.code}")
except Exception:
    done(result="unreachable")
try:
    s = json.loads(res["result"]["content"][0]["text"])
    beat = s.get("last_heartbeat_age_s")
    prov = s.get("providers") or {}
    now = time.time()
    def down(v):
        try: return float(v) > now
        except (TypeError, ValueError): return False
    judging = not all(down(prov.get(k)) for k in ("claude_unavailable_until", "codex_unavailable_until"))
    out.update(companies=s.get("watches"), sources=s.get("source_count"),
               failing_sources=len(s.get("failing_sources") or []),
               collector_ok=bool(beat is not None and beat < 1800), judging_ok=judging)
except Exception:
    done(result="bad_reply")
if mode != "connect":
    done(result="ok")
have = subprocess.run(["claude", "mcp", "get", "lacuna-news"], capture_output=True).returncode == 0
if have and os.environ.get("REPLACE") != "1":
    done(result="already_connected")
if have:
    subprocess.run(["claude", "mcp", "remove", "--scope", "user", "lacuna-news"], capture_output=True)
add = subprocess.run(["claude", "mcp", "add", "--scope", "user", "--transport", "http", "lacuna-news",
                      url, "--header", "Authorization: Bearer " + tok], capture_output=True)
if add.returncode != 0:
    done(result="add_failed")
cfgdir = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(os.path.expanduser("~"), ".claude")
START, END = "<!-- lacuna-news:start -->", "<!-- lacuna-news:end -->"
block = START + """
# Lacuna news desk

The Lacuna news desk is connected for this person. Before answering anything
about news, the companies being watched, or news alerts, and before calling
any tool whose name starts `mcp__lacuna-news__`, load the `lacuna:news-watch`
skill and follow it. For connecting, disconnecting or a connection that is not
working, load `lacuna:news-connect`. The person is not technical: nothing
technical reaches them, and every reply ends with a Done line and a
Recommended line.
""" + END + "\n"
try:
    os.makedirs(cfgdir, exist_ok=True)
    with open(os.path.join(cfgdir, "lacuna-news.json"), "w") as fh:
        json.dump({"access": access, "name": d.get("name", ""),
                   "connected": int(now)}, fh)
    md = os.path.join(cfgdir, "CLAUDE.md")
    old = open(md).read() if os.path.exists(md) else ""
    if START in old and END in old:
        new = old[:old.index(START)] + block + old[old.index(END) + len(END):].lstrip("\n")
    else:
        new = old + ("\n" if old and not old.endswith("\n") else "") + ("\n" if old else "") + block
    open(md, "w").write(new)
except OSError:
    pass
done(result="connected")
PY
```

If `python3` is missing, say: "Connecting needs one small program that is
missing on this computer. Ask Nic and tell him that." Then the two lines, with
Done as "nothing changed".

## What you do, step 4: read the result and tell the person

Read the `result` value and give the matching message. One or two sentences,
then the two lines. No field names, no values they did not ask for.

- **`malformed`** (a cut-off, incomplete or altered code):

  > That code is not complete, so I could not use it. Codes are one long line
  > and it is easy to lose the end when copying.
  > Done: nothing changed.
  > Recommended: copy the whole line from Nic's message again and paste it
  > here.

- **`unauthorized`** (the desk refused it):

  > The news desk did not accept that code. It may have been switched off or
  > copied wrongly.
  > Done: nothing changed.
  > Recommended: ask Nic for a fresh news desk code.

- **`unreachable`**:

  > I could not reach the news desk just now.
  > Done: nothing changed.
  > Recommended: check your internet connection and try again in a few minutes;
  > if it keeps happening, tell Nic.

- **`server_error_<n>`** or **`bad_reply`**:

  > The news desk answered, but not properly.
  > Done: nothing changed.
  > Recommended: try again in a few minutes, and tell Nic if it keeps
  > happening.

- **`already_connected`**: the code works and a connection already exists. Ask
  the replace question from step 1, and on a yes run step 3 again with
  `REPLACE=1`.

- **`add_failed`**: the code works, but the connection could not be saved on
  this computer.

  > Your code works, but I could not save the connection on this computer.
  > Done: nothing changed.
  > Recommended: tell Nic, and say that the code worked but saving the
  > connection failed. He will know what to check.

- **`connected`**: report in this shape, filled in from the line:

  > Connected to the news desk. It is following COMPANIES companies across
  > SOURCES news feeds, and RUNNING. ACCESS.
  >
  > One more step: close Claude Code and open it again. New connections only
  > load when Claude Code starts, and your companies and settings are kept on
  > the desk, so nothing is lost by restarting.
  >
  > Done: the news desk is connected for you.
  > Recommended: after the restart, ask "what companies are being watched".

  - RUNNING is "everything is running" when `failing_sources=0`,
    `collector_ok=True` and `judging_ok=True`. Otherwise say plainly what is
    not, in one clause: "one or two news feeds are not answering at the
    moment, which the desk handles on its own" for a few failing sources;
    "the desk has not checked in recently, so tell Nic" when
    `collector_ok=False`; "stories are arriving but are not being sorted for
    importance right now, which Nic will know about" when `judging_ok=False`.
  - ACCESS is "You can read the news. Adding or changing companies needs a
    different code, which you can ask Nic for" when `access=read`, and "You
    can read the news and add or change the companies being watched" when
    `access=write`. The desk checks this on every request, so if Nic changes
    it later the desk will say so at the time.

## After a restart

When `mcp__lacuna-news__news_status` is in your tool list, the connection is
live. If the person comes back to check, call it and give the connected
message without the restart paragraph. If the tools are still missing after a
restart, run step 1 again before guessing, and never show the output of
`claude mcp get`, because it contains the code's contents. If that still gets
nowhere:

> The connection is saved but the news desk is not showing up for me.
> Done: nothing changed.
> Recommended: tell Nic; say that you connected, restarted, and the news desk
> still does not appear.

## Disconnecting

"Disconnect the news" or "remove the news desk" means:

```bash
claude mcp remove --scope user lacuna-news >/dev/null 2>&1 && echo removed || echo not-found
rm -f "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/lacuna-news.json"
python3 - <<'PY'
import os
md = os.path.join(os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude"), "CLAUDE.md")
S, E = "<!-- lacuna-news:start -->", "<!-- lacuna-news:end -->"
if os.path.exists(md):
    t = open(md).read()
    if S in t and E in t:
        open(md, "w").write(t[:t.index(S)].rstrip("\n") + "\n" + t[t.index(E) + len(E):].lstrip("\n"))
PY
```

Then:

> Done: the news desk is disconnected on this computer; your companies and
> settings are still on the desk.
> Recommended: tell Nic if you will not use it again, so he can switch your
> code off.
