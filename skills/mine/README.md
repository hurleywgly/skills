# mine

> Have agents sift information and find gems on your behalf.

We hang onto notes, reports, and old code longer than we probably should. `/mine` digs through everything you've kept but never had time to distill, and hands back the handful of ideas still worth acting on.

Built for AI coding agents (Claude Code, Codex, and more).

## Install

```bash
npx skills add hurleywgly/skills --skill mine
```

Or add it for a specific agent, e.g. Claude Code:

```bash
npx skills add hurleywgly/skills --skill mine -a claude-code
```

Manual: copy this folder into your agent's skills directory (e.g. `~/.claude/skills/mine/` or `.agents/skills/mine/`).

## What it does

- **Pan through messy or old notes.** Drop in years of scattered notes, exports, or abandoned folders and have agents surface the handful of ideas still worth acting on.
- **Learn from any dataset.** Find the nuggets you care about amidst a sea of noise — great with analogous systems or abandoned codebases when you have a specific problem you're trying to solve.

## Why it matters

We hang onto notes, reports, and old code longer than we probably should. This skill helps you turn the information you've kept but haven't had time to distill into insights you can use to drive strategy or win an argument.

## How it fits your workflow

Point `/mine` at anything you've been hoarding — old notes, a dead repo, a folder of exports — and let agents dig while you do something else. The gems come back as a capsule you can actually use.

## Pairs well with

`pitch-me` • `projector` • `research`

## Usage

Just describe what you want and where to look. The agent figures out the source type, scope, and strategy, then hands back one capsule with scored, themed findings.

```
/mine landing page tips from my Education notes
```

```
/mine everything useful in ~/Downloads/notion-export.zip
```

```
/mine what does this repo do ~/projects/some-codebase
```

```
/mine summarize https://docs.example.com
```

Run `/mine resume` to pick up a multi-session run, or `/mine status` to check progress.

### What it mines

| Source | How to reference it | Platform |
|--------|---------------------|----------|
| iCloud Notes | "my notes", "Notes app", a folder name | macOS only |
| Local files | Any directory path | CLI / Desktop |
| Git repos | Path to a repo, or "this codebase" | CLI / Desktop |
| ZIP archives | Path to a `.zip` file | CLI / Desktop |
| Websites | Any URL | All environments |

### How findings are scored

Every finding is scored on three criteria — keep if it scores 2 or 3 of 3, discard below:

| Criterion | What it measures |
|-----------|------------------|
| **Transferable** | Useful beyond its original context? |
| **Specific** | Concrete details, not just vibes? |
| **Buried** | Actually hard to find right now? |

The output is a single markdown capsule: findings grouped by theme, each scored and categorized (insight, framework, decision, idea, pattern, quote, action, contact), with source attribution and a confidence rating.

---

Part of [hurleywgly/skills](https://github.com/hurleywgly/skills). MIT licensed.
