# auto-mine

> Mine your sources overnight, wake up to the gems

The best research dies because nobody has a free evening to grind through it. `auto-mine` puts an agent on the job while you sleep, then deliberately hands judgment back to you in the morning — authorized, read-only, parked for review by design.

Built for AI coding agents (Claude Code, Codex, and more).

## Install

```bash
npx skills add hurleywgly/skills --skill auto-mine
```

Or add it for a specific agent, e.g. Claude Code:

```bash
npx skills add hurleywgly/skills --skill auto-mine -a claude-code
```

Manual: copy this folder into your agent's skills directory (e.g. `~/.claude/skills/auto-mine/` or `.agents/skills/auto-mine/`).

## What it does

- **Mine while you sleep.** Point it at a messy source before bed and it works the whole mining loop unattended, until it runs out of new gems or hits its limit. By morning there's a tidy digest of the best finds waiting for you to judge over coffee.
- **Read-only and honest.** It never touches your sources and never decides anything for you. You wake up to ranked keepers, a keep-vs-toss ratio, and parked cards that wait for your call.

## Why it matters

The best research dies because nobody has a free evening to grind through it. We want agents working while we're away, but handing one the keys overnight is scary if it might change things or quietly make choices for you. This runs the digging unattended, then deliberately stops and hands judgment back. Authorized, read-only, parked for review by design.

## How it fits your workflow

Queue up a selection of notes or source files at the end of the day, approve the run, and let it grind overnight. In the morning you skim the ranked keepers and decide what's worth pulling into your projects.

## Pairs well with

`mine` • `capsule` • `ink`

## Usage

`auto-mine` takes the same arguments as `mine` — a source plus an optional mission — and runs that mining loop unattended to a budget.

```
/auto-mine ~/notes/research-dump
```

```
/auto-mine ~/notes/research-dump "find pricing patterns worth testing"
```

An unattended run needs your authorization first — either a card in the `⚡ Autonomous` lane of your task board (you drag to approve; the agent pulls from there and never self-approves), or a direct "get going on this autonomously." Without it, the run parks immediately and tells you why.

When the loop finishes — it stops on convergence (three quiet cycles in a row), an exhausted source, an answered mission, or a spent budget — you get a morning bundle: an append-only run log plus an HTML digest with the top keepers ranked by theme, the keep/discard ratio, budget cap vs. actual, and any parked-for-decision cards. Nothing auto-resolves; the calls are yours.

---

Part of [hurleywgly/skills](https://github.com/hurleywgly/skills). MIT licensed.
