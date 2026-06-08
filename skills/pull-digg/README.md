# pull-digg

> Staying on top of the AI-news firehose

Staying current on AI is a part-time job, and most feeds reward whatever's loudest instead of whatever matters. This runs a scout pass over a curated AI-news graph, scores candidates against a real bar, and hands back only the handful that survive.

Built for AI coding agents (Claude Code, Codex, and more).

## Install

```bash
npx skills add hurleywgly/skills --skill pull-digg
```

Or add it for a specific agent, e.g. Claude Code:

```bash
npx skills add hurleywgly/skills --skill pull-digg -a claude-code
```

Manual: copy this folder into your agent's skills directory (e.g. `~/.claude/skills/pull-digg/` or `.agents/skills/pull-digg/`).

## What it does

- **Straight-to-the-point AI news.** Get a tight briefing of the most influential stories in AI, ranked by social and credibility signals.
- **Find repos and accounts worth your time.** Have your agent check Digg and surface the GitHub projects and credible accounts quietly starring and posting them.

## Why it matters

Staying current on AI is a part-time job, and most feeds reward whatever's loudest rather than whatever matters. This runs a scout pass over a curated AI-news graph, scores candidates against a real bar, and hands back only the handful that survive. It's honest about its own limits, too: rankings are one signal, not objective truth.

## How it fits your workflow

Fire this when you want a fast read on what's moving in AI without opening fifteen tabs. Pull the briefing in the morning, dig into a story's source posts when something looks real, and pull the GitHub feed when you're hunting for tools to build or write about.

## Pairs well with

`daily-brief` • `research` • `ink`

## Usage

```bash
# Curated briefing: top signals across stories, movers, replacements, and repos
/pull-digg

# Search Digg stories for a topic, with source-post citations
/pull-digg topic "agent evals" --since 30d

# Digg GitHub feeds: starred AI repos and recent activity
/pull-digg github

# Credibility lookup for one X handle
/pull-digg author <handle>

# Story detail: evidence, sentiment, crossrefs, top source posts
/pull-digg story <clusterUrlId>
```

Read-only by design — it pulls from public Digg surfaces via `digg-pp-cli`, requires no authentication, and never posts, votes, or changes anything.

---

Part of [hurleywgly/skills](https://github.com/hurleywgly/skills). MIT licensed.
