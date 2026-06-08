# events

> Surface the local events worth your time, scored to you.

Local event discovery is a chore nobody keeps up with — listings are scattered, event boards are noisy, and the good stuff gets lost. This turns that chore into a quick shortlist of 2–5 events you'll actually read, in time to go.

Built for AI coding agents (Claude Code, Codex, and more).

## Install

```bash
npx skills add hurleywgly/skills --skill events
```

Or add it for a specific agent, e.g. Claude Code:

```bash
npx skills add hurleywgly/skills --skill events -a claude-code
```

Manual: copy this folder into your agent's skills directory (e.g. `~/.claude/skills/events/` or `.agents/skills/events/`).

## What it does

- **Get a timely shortlist.** The agent scans the web for upcoming events and hands back 2–5 actually worth attending — while there's still time to grab a spot.

## Why it matters

Local event discovery is a chore nobody keeps up with. Listings are scattered, event boards are noisy, and the good stuff gets lost too often. This turns that chore into a quick shortlist you actually read.

## How it fits your workflow

Run it at the start of every week to stay aware of cool tech events nearby you might have missed and want to attend. Works great when you're traveling, too.

## Pairs well with

`pull-feed` • `daily-brief`

## Usage

No API keys — just WebSearch and WebFetch. Point it at your metro and interests via `config.json`, then ask:

```
/events
```
Full scan — all tiers, networking overlay, and conference radar.

```
/events quick
```
Known sources only — a fast check that skips the conference radar.

```
/events conferences
```
Conference radar only — a 2–6 month lookahead for larger events.

It scores every candidate against your profile (topic relevance, community quality, networking value, convenience), drops anything below the bar, and renders a clean shortlist with a one-line "why" for each — plus a separate conference radar for what's further out.

---

Part of [hurleywgly/skills](https://github.com/hurleywgly/skills). MIT licensed.
