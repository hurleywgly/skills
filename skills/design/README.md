# Design

A design loop shaped like the double diamond: explore several directions, converge on one with a reason, then build section by section with critique from an outside reviewer until it converges.

## Use

```
/design <description> | new [--type style-board|screen-design] | run <brief-path> [--canvas figma|html|<tool>] [--budget N] [--autonomous] [--stretch]
```

## Requirements

Prefers the Figma MCP server; works without it on an HTML/SVG canvas. Optional: a second-opinion skill for the outside critique.

## Install

Copy this folder into your agent's skills directory (for example `~/.claude/skills/design` or `~/.agents/skills/design`). `SKILL.md` is the skill; `agents/openai.yaml` carries the Codex display name and invocation policy.

## License

MIT. See `LICENSE`.
