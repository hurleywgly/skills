# skills

A collection of agent skills I use every day — built for AI coding agents (Claude Code, Codex, and more).

Each skill is a self-contained capability you can drop into your own setup: research loops, design loops, knowledge transfer, daily briefs, second opinions, and more. They're zero-dependency by design (built on file ops, search, and your agent's native tools) and portable across any agent that supports the [open skills ecosystem](https://github.com/vercel-labs/skills).

## Install

Add any single skill:

```bash
npx skills add hurleywgly/skills --skill ink
```

Add it for a specific agent (e.g. Claude Code):

```bash
npx skills add hurleywgly/skills --skill ink -a claude-code
```

Browse everything, or grab it all:

```bash
npx skills add hurleywgly/skills --list
npx skills add hurleywgly/skills --all
```

**Manual:** copy any `skills/<name>/` folder into your agent's skills directory (e.g. `~/.claude/skills/<name>/` for Claude Code, or `.agents/skills/<name>/` for Codex).

## The skills

### 🔎 Research faster
| Skill | What it does |
|-------|--------------|
| [research](skills/research) | Send agents to dig up insights across the web |
| [mine](skills/mine) | Have agents sift one or many sources and find gems on your behalf |

### 🗣️ Communicate better
| Skill | What it does |
|-------|--------------|
| [ink](skills/ink) | Visualize just about anything in HTML |
| [primer](skills/primer) | Learn a hard topic from a simple visual explainer |
| [design](skills/design) | Explore directions, pick one, and refine it with outside critique |
| [js-art](skills/js-art) | Wall art drawn in code that looks hand-made |

### 🧠 Think sharper
| Skill | What it does |
|-------|--------------|
| [think](skills/think) | Harden any idea before it becomes a plan |
| [pitch-me](skills/pitch-me) | Get N wildly different ideas before you commit to one |
| [claude](skills/claude) | A Claude gut-check when another model is driving |
| [codex](skills/codex) | A Codex gut-check when Claude is driving |

### 📦 Keep projects alive
| Skill | What it does |
|-------|--------------|
| [capsule](skills/capsule) | Portable, actionable knowledge transfer between agents |
| [channel](skills/channel) | Load any package's persona and become it on demand |
| [projector](skills/projector) | Package an expert agent harness in minutes |
| [update-from-session](skills/update-from-session) | Turn each working session into lasting memory |

### 📡 Stay informed
| Skill | What it does |
|-------|--------------|
| [daily-brief](skills/daily-brief) | A chief-of-staff brief on what actually matters today |
| [pull-digg](skills/pull-digg) | Staying on top of the AI-news firehose |
| [events](skills/events) | Surface the local events worth your time, scored to you |

## Using them

- **Claude Code:** type `/<name>`, for example `/think should we ship the free tier first?`. Skills without a manual-only flag also load on their own when your request matches.
- **Codex:** type `$<name>` or pick from `/skills`.
- **Manual-only skills:** `research`, `design`, `capsule`, `mine`, `channel`, `events`, `pull-digg`, and `update-from-session` run long, spend money, or write files, so they only run when you call them by name. That is set for Claude Code (`disable-model-invocation` in `SKILL.md`) and for Codex (`agents/openai.yaml`).
- **Dependencies between skills:** `pitch-me` renders through `ink` and uses `codex` or `claude` for its outside take when one is installed. `design` prefers the Figma MCP server and works without it, and uses `codex` or `claude` as its outside reviewer when one is installed. `codex` and `claude` need their own CLI, logged in with a subscription.

## Compatibility

These skills run wherever the [`skills`](https://github.com/vercel-labs/skills) CLI installs them: Claude Code, Codex, Cursor, opencode, and dozens of other agents. Each skill's `SKILL.md` is the portable contract; the `README.md` explains what it's for.

## Contributing

Skills here must stay workspace-agnostic: no absolute paths, no personal names in the logic, and a fallback wherever a step names one host's tool. Keep `SKILL.md` under 500 lines and move optional detail into `references/`. Run the linter before opening a PR:

```bash
python3 scripts/validate.py
```

## License

MIT © Ryan Wigley
