# primer

> Turn any tech announcement into a simple breakdown

Big software announcements drop faster than you can make use of them. Primer does the legwork — point it at the links and get back a cited explanation of what something actually is and why it matters to you.

Built for AI coding agents (Claude Code, Codex, and more).

## Install

```bash
npx skills add hurleywgly/skills --skill primer
```

Or add it for a specific agent, e.g. Claude Code:

```bash
npx skills add hurleywgly/skills --skill primer -a claude-code
```

Manual: copy this folder into your agent's skills directory (e.g. `~/.claude/skills/primer/` or `.agents/skills/primer/`).

## What it does

- **Decode a viral tech trend.** Drop in an announcement, thread, or piece of terminology and get back a cited breakdown of what it actually is, how it works, and why it matters to you.
- **Ship a shareable explainer.** It builds a designed, interactive single-page site explaining the concept in plain terms — then optionally deploys it to a live URL you can send to anyone.

## Why it matters

Big software announcements drop faster than you can make use of the news. When a new concept or breakthrough trends in your feed over a couple of days, it gets hard to tell whether it's valuable to you or just noise. Primer does the legwork to keep you informed without getting distracted or overwhelmed by new terminology.

## How it fits your workflow

When something lands on your feed that you know matters but don't fully get, point primer at a few relevant links — articles, posts, repos — and let it explain the thing to you on your own time.

## Pairs well with

`research` • `ink` • `channel`

## Usage

Point it at source material and let it run the full research-to-site pipeline:

```
make a primer on this thread: <url>
```

```
break this down: <url1> <url2>   # mix articles, posts, GitHub READMEs
```

It fetches and analyzes the sources from multiple angles (what it is, who made it, how it changes existing systems, where the hype outruns reality), builds a research doc plus a mobile-responsive single-file HTML primer, then can deploy it to a live shareable URL.

Best for significant announcements worth a real deep-dive — for a quick TL;DR, just ask for a summary instead.

---

Part of [hurleywgly/skills](https://github.com/hurleywgly/skills). MIT licensed.
