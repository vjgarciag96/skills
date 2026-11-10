# skills

Agent skills shared by Claude Code and Codex.

## Install on a new laptop

Clone the repo to `~/.agents/skills`:

```sh
git clone https://github.com/vjgarciag96/skills.git ~/.agents/skills
```

Link each skill into Claude Code and Codex:

```sh
for t in ~/.claude/skills ~/.codex/skills; do
  mkdir -p "$t"
  for s in ~/.agents/skills/*/; do
    ln -sfn "${s%/}" "$t/$(basename "$s")"
  done
done
```

Run the loop again after pulling a new skill. Restart Claude Code or Codex to pick up changes.
