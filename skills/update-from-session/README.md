# update-from-session

> Turn each working session into lasting memory

Every session can teach you and your agent something, but most of that learning vanishes the moment the chat ends. This skill catches the decisions and patterns that actually matter and writes down only the stuff that compounds.

Built for AI coding agents (Claude Code, Codex, and more).

## Install

```bash
npx skills add hurleywgly/skills --skill update-from-session
```

Or add it for a specific agent, e.g. Claude Code:

```bash
npx skills add hurleywgly/skills --skill update-from-session -a claude-code
```

Manual: copy this folder into your agent's skills directory (e.g. `~/.claude/skills/update-from-session/` or `.agents/skills/update-from-session/`).

## What it does

- **Capture workflow patterns to memory.** At the end of a session, pull out what actually changed how you'd work next time — patterns, decisions, and surprises — then have the agent write them to durable memory files.

## Why it matters

Every session has the potential to teach you and your agent something. Most of that excitement vanishes the moment the chat ends. This skill reviews the key details and decisions made that cycle, then writes down only the stuff that compounds — not everything, just the keepers.

## How it fits your workflow

When you wrap up a real working session, run update-from-session to review what you solved, then let it write the keepers into memory and log the why behind any decision. Those memory files get referenced at the start of each new session, so the next one boots already knowing.

## Pairs well with

`mark` • `log-work`

## Usage

Run it as a session winds down:

```
/update-from-session
```

The skill walks the session, asks what's worth remembering, gut-checks each candidate (if you can't name the concrete friction a rule fixes, it gets demoted to a note instead of a behavioral rule), then:

- Writes memory entries to your project's memory directory (e.g. `./memory/`)
- Appends decisions to your project's `changelog.md` with the load-bearing `**Why:**` field
- Adds a one-line entry to your top-level `CHANGELOG.md` when the change affects your workspace itself (a new or updated skill, new behavior, root instructions, persistent memory)
- Suggests updates to `context.md` or your root instruction file (CLAUDE.md / AGENTS.md) when state or system-wide learning changed

Memory entries follow a simple format — topic, type (pattern / decision / learning), date, context, a summary, and when to apply it next time.

---

Part of [hurleywgly/skills](https://github.com/hurleywgly/skills). MIT licensed.
