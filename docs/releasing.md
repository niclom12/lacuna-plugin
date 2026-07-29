# Releasing lacuna

## Two validate commands, both required

`claude plugin validate` does something different depending on what you point it
at, and running only one of them is the trap. Run both from the repo root and
require exit 0 from both.

**1. The marketplace manifest, at the repo root.** This is the entry
`/plugin marketplace add` reads.

```bash
claude plugin validate .
```

The root path resolves to `.claude-plugin/marketplace.json`, so this checks that
manifest and nothing else. It prints `Validating marketplace manifest: …` and one
line of result. It never opens a skill, a command, or an agent file, so a skill
with broken frontmatter passes it.

**2. The plugin manifest and the bundle, named explicitly.** This is the
structure gate, and the path has to be given in full.

```bash
claude plugin validate .claude-plugin/plugin.json --strict
```

This one prints `Validating plugin manifest: …` and then walks the bundle. It
opens every `SKILL.md`, command, and agent file and validates the frontmatter,
printing a `Validating skill: <path>` line for anything it has a complaint about.
`--strict` turns warnings into a non-zero exit, which is what makes broken
frontmatter fail rather than pass with a note.

Two things this second command does not do, so do not read a pass as more than it
is. It does not check that any skill exists at all: delete `skills/`, `commands/`,
and `agents/` and it still exits 0. And `--strict` on the marketplace target
(`claude plugin validate . --strict`) adds nothing here, because the marketplace
manifest is not where frontmatter lives.

## Frontmatter parse sweep

`--strict` catches frontmatter that fails to parse, and the failure mode when it
slips through is quiet: the skill loads with every field dropped, so it has no
description, no trigger surface, and never fires. The usual cause is a bare
`colon space` inside an unquoted description. Quote any description containing
a colon.

A direct sweep over every frontmatter block, independent of the CLI, which also
catches a `SKILL.md` missing `name` or `description` entirely:

```bash
python3 - <<'PY'
import pathlib, sys, yaml
bad = 0
for p in sorted(pathlib.Path('.').rglob('*.md')):
    if '.git' in p.parts:
        continue
    text = p.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        continue
    end = text.find('\n---', 3)
    if end == -1:
        print(f'UNTERMINATED {p}')
        bad += 1
        continue
    try:
        meta = yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError as e:
        print(f'PARSE FAIL {p}: {e}')
        bad += 1
        continue
    missing = [k for k in ('name', 'description') if not meta.get(k)]
    if missing and p.name == 'SKILL.md':
        print(f'MISSING {missing} {p}')
        bad += 1
print('clean' if not bad else f'{bad} problem(s)')
sys.exit(1 if bad else 0)
PY
```

## Version agreement

Three files carry a version and all three are released together, so all three
have to agree: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`
(`metadata.version`), and the top heading in `CHANGELOG.md`. A mismatch has
shipped from this repo once already.

```bash
python3 - <<'PY'
import json, pathlib, re, sys
plugin = json.loads(pathlib.Path('.claude-plugin/plugin.json').read_text())['version']
market = json.loads(pathlib.Path('.claude-plugin/marketplace.json').read_text())['metadata']['version']
head = re.search(r'^## \[([0-9][^\]]*)\]', pathlib.Path('CHANGELOG.md').read_text(), re.M).group(1)
print(f'plugin.json={plugin} marketplace.json={market} CHANGELOG={head}')
ok = plugin == market == head
print('agree' if ok else 'MISMATCH')
sys.exit(0 if ok else 1)
PY
```

## Style sweep

The shipped copy has no em-dashes (U+2014). Vendored licence text is exempt,
since it is not ours to edit. The pattern is built with `printf` so this file
does not trip its own check.

```bash
grep -rn "$(printf '\u2014')" . --exclude-dir=.git --exclude-dir=licenses \
  && echo 'EM-DASH FOUND' || echo 'clean'
```

## Before tagging

- Both validate commands exit 0.
- The frontmatter sweep prints `clean`.
- The version check prints `agree`.
- The style sweep prints `clean`.
- Nothing in `templates/`, `docs/`, or the skills refers to a command that no
  longer exists. `grep -rn '/lacuna:' .` should name only the commands present
  in `commands/`.
- Nothing refers to a plugin file by a bare relative path. Commands run with the
  user's project as the working directory, so a path into this plugin has to go
  through `${CLAUDE_PLUGIN_ROOT}`, which Claude Code substitutes in command and
  skill markdown bodies.
- A headless load probe from a directory outside this repo comes back clean:

  ```bash
  cd /tmp && claude -p "say ok" --plugin-dir <path-to-repo> \
    --output-format stream-json --verbose < /dev/null
  ```

  The init event lists the plugin, its version, and its skills, commands, and
  agents. Check the counts against what is on disk and check for any plugin
  error in the stream.
