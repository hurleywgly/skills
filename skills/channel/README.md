# channel

> Load any package's persona and become it on demand

You build up rich worlds of context for your agents — personas, reference docs, project state — but every new session starts cold. `channel` keeps a session focused on one package, figures out what's worth loading, and pulls that context in so the agent shows up already knowing who it is and where the work stands.

Built for AI coding agents (Claude Code, Codex, and more).

## Install

```bash
npx skills add hurleywgly/skills --skill channel
```

Or add it for a specific agent, e.g. Claude Code:

```bash
npx skills add hurleywgly/skills --skill channel -a claude-code
```

Manual: copy this folder into your agent's skills directory (e.g. `~/.claude/skills/channel/` or `.agents/skills/channel/`).

## What it does

- **Become any package instantly.** Name a package and the agent loads its prompt, context, and knowledge files, then stays in character for the rest of the chat. One command turns a fresh session into your essay copilot, your interview coach, or your operational sidekick.
- **Resume a project mid-stride.** Pull the live state and instructions of a project-specific package into a new conversation. The agent reads the dashboard and instruction files so you skip the re-briefing and pick up exactly where you left off.

## Why it matters

You build up rich worlds of context for agents — personas, a stack of reference docs, company context — but every new session starts cold. Re-explaining or dropping the same context in every time is tiresome. `channel` keeps your session focused on a specific package, figures out what's useful, and loads that context for you.

## How it fits your workflow

When you've got a package built for a specific project, channel it into whatever session you're in and the agent shows up already knowing the persona you want it to operate as and the state of the project.

## Pairs well with

`projector` • `capsule` • `build`

## Usage

```bash
# Fuzzy-match a package by name and load its context + persona
/channel essay

# See everything available, with type and a one-line summary
/channel list

# Load all readable knowledge files, past the default budget
/channel essay --deep
```

`channel` resolves the package (shorthand or fuzzy name match), detects its type, loads the right files within a context budget, and adopts the persona. Say "exit channel" to drop the persona and return to default behavior. It's read-only — it never modifies package files.

---

Part of [hurleywgly/skills](https://github.com/hurleywgly/skills). MIT licensed.
