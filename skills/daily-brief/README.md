# daily-brief

> A chief-of-staff brief on what actually matters today

Stop scrolling five tabs to figure out where to start. This pulls your calendar, inbox, messages, and KPIs into one tight, reliable brief that names the single most important action and the evidence behind it — so you can stay focused and start the day already pointed in the right direction.

Built for AI coding agents (Claude Code, Codex, and more).

## Install

```bash
npx skills add hurleywgly/skills --skill daily-brief
```

Or add it for a specific agent, e.g. Claude Code:

```bash
npx skills add hurleywgly/skills --skill daily-brief -a claude-code
```

Manual: copy this folder into your agent's skills directory (e.g. `~/.claude/skills/daily-brief/` or `.agents/skills/daily-brief/`).

## What it does

- **Get a first move, not a data dump.** Your agent pulls calendar, inbox, messages, and KPIs into one tight brief that names the single most important action and the evidence behind it.
- **Wire it to your own sources.** Point it at whatever you already use: calendar, email, Slack, Stripe, site analytics, even local notes files. It surfaces only the signals that could change what you do today.

## Why it matters

Having a single, reliable synthesized source of the daily updates you care about keeps you focused and gives you peace of mind — communication that reaches you where you want to be met.

## How it fits your workflow

Set up a standing schedule that runs it first thing every morning, so you know what to do and catch any important updates before you even open your laptop.

## Pairs well with

`events` • `pull-digg` • `research`

## Usage

```text
/daily-brief setup
/daily-brief run --preview
/daily-brief run --send
/daily-brief check
/daily-brief sources
```

- **First-time setup** — `/daily-brief setup` walks you through a minimal config (`./daily-brief.config.json`): your name, timezone, and at least one calendar or inbox source. It only asks for what's missing.
- **Preview the day** — `/daily-brief run --preview` produces a real brief once your sources are connected, with a "First Move" and a `Why:` line. Preview is the default; nothing gets sent without your say-so.
- **Send it** — `/daily-brief run --send` delivers to a configured target (SMS, Slack, Discord, email, or a local markdown file) after preview or explicit confirmation.
- **Health check** — `/daily-brief check` validates your config and `/daily-brief sources` shows which sources are connected, skipped, or unauthenticated.

The brief stays tight (40–60 lines), thresholds routine metrics out of the way, and treats inbox/calendar/message text as untrusted evidence — never as instructions. Missing a source degrades gracefully into a partial brief instead of failing the whole run.

---

Part of [hurleywgly/skills](https://github.com/hurleywgly/skills). MIT licensed.
