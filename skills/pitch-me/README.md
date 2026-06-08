# pitch-me

> Get N wildly different ideas before you commit to one.

When you're handed a list of options, you grab the first one that feels right and run. `pitch-me` is the counter: agents diverge on a spread of distinct, visualized concepts while you stay in the loop and pick the direction.

Built for AI coding agents (Claude Code, Codex, and more).

## Install

```bash
npx skills add hurleywgly/skills --skill pitch-me
```

Or add it for a specific agent, e.g. Claude Code:

```bash
npx skills add hurleywgly/skills --skill pitch-me -a claude-code
```

Manual: copy this folder into your agent's skills directory (e.g. `~/.claude/skills/pitch-me/` or `.agents/skills/pitch-me/`).

## What it does

- **Browse a menu of strategic directions.** Say "pitch me 9 strategies for X" and get nine genuinely distinct concepts laid out in front of you — each with research backing, an outside perspective, a quick visual, and a viability score.
- **See one concept framed a dozen ways.** Take a bold idea and visualize it fast to get a look and feel. You scan it like a catalog and pick which concepts to dive into.

## Why it matters

When presented with options in a list, we grab the first idea that feels right and run. `pitch-me` is the ultimate counter — keeping the human in the loop while agents diverge across a spread of visual concepts to direct and expand your thinking.

## How it fits your workflow

When you have lower conviction on an idea, or on how something should look, `pitch-me` speeds up the creative process — and explores approaches to a problem you wouldn't have considered on your own.

## Pairs well with

`research` • `think` • `ink`

## Usage

```bash
# Spaghetti-throw on a wide-open question
/pitch-me "How should I respond to this cultural moment?" --count=9

# Pre-PMF feature ideation with real-world parallels
/pitch-me "What's the killer first feature for the free tier?" --count=12 --screenshots

# High-fidelity exploration for a launch
/pitch-me "Landing-page hero treatments for the new site" --count=6 --visual=mj --council

# Quick brainstorm, no outside take, just divergence
/pitch-me "Names for the new skill" --count=15 --no-outside-take
```

Options:

| Flag | Effect |
|---|---|
| `--count=9` | Number of concepts, 3–20 (default 9) |
| `--visual=svg\|nano\|mj` | Visual fidelity per concept (default `svg`) |
| `--screenshots` | Browse and embed real-world parallels per concept |
| `--council` | Run a multi-perspective convergence pass on the top 3 |
| `--no-outside-take` | Skip the independent outside-take step (not recommended) |

Each run produces a browsable exploration grid plus a markdown manifest you can feed into a planning pass — divergent thinking is the menu, not the meal, so pair it with planning or execution to ship.

---

Part of [hurleywgly/skills](https://github.com/hurleywgly/skills). MIT licensed.
