# research

> Send agents to dig up insights across the web

Most AI research sends a single agent off to do a few searches and hands back a composite that blends signal and noise. This approaches a question from multiple directions at once, scores what it finds, and gives agents the tools to actually research usefully — within a budget you set.

Built for AI coding agents (Claude Code, Codex, and more).

## Install

```bash
npx skills add hurleywgly/skills --skill research
```

Or add it for a specific agent, e.g. Claude Code:

```bash
npx skills add hurleywgly/skills --skill research -a claude-code
```

Manual: copy this folder into your agent's skills directory (e.g. `~/.claude/skills/research/` or `.agents/skills/research/`).

## What it does

- **Hunt down real user voice.** Send agents searching the web through simulated personas that pull verbatim quotes, pain points, and product insights from numerous angles — real evidence of what people are saying.
- **Start a knowledge base.** Run a research loop to build a foundational set of expertise on a topic. The self-grading, multi-persona approach gives you confidence you're learning from grounded sources, even for subjects that are foreign to you.

## Why it matters

Most AI chatbots that research send a single agent off to do a few searches and come back with a composite of related information. There's no standard way to verify what's signal versus noise, or whether the report came from an exhaustive search. This approaches tasks simultaneously from multiple directions and gives agents all the tools to succeed. Set budgets and actually research usefully.

## How it fits your workflow

When you're shaping the launch of a new product feature, you research the things you don't know or understand that could help you move from concept to launch. It's an easy way to add high-quality context to your agentic systems.

## Pairs well with

`pitch-me` • `capsule` • `ink` • `design`

## Usage

```bash
# Create a research brief interactively
/research new

# Run it (checkpoints every 5 cycles)
/research run research/briefs/my-question.md

# Single-cycle test
/research run research/briefs/my-question.md --once

# Overnight autonomous run (skips checkpoints)
/research run research/briefs/my-question.md --autonomous

# Synthesize findings with multi-perspective review
/research synthesize my-question
```

## How it works

1. **Write a brief** — defines the research question, personas, sources, and stop conditions.
2. **Run `/research`** — the system loops: pick persona → search the web → extract findings → score → keep/discard → adapt → repeat.
3. **Review at checkpoints** — every 5 cycles, it pauses to show findings and ask continue/adjust/stop.
4. **Synthesize** — multi-perspective review clusters findings into themes with analytical annotations.

### The research cycle

```
┌─────────────────────────────────┐
│         Select Persona          │
│    (rotate through brief's      │
│     persona list each cycle)    │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│       Generate 2-3 Queries      │
│   (persona seeds + adaptation   │
│    from previous cycles)        │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│     WebSearch → WebFetch        │
│   (forums, reviews, social,    │
│    communities)                 │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│       Extract Findings          │
│  (quotes, pain points,         │
│   switching triggers,           │
│   workarounds)                  │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│     Score: A + E + N (0-3)      │
│  Actionable · Evidenced · Novel │
│                                 │
│   >= 2 → KEEP                   │
│   < 2  → DISCARD (with reason) │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│    Deduplicate → Log → Adapt    │
│                                 │
│  Stop if: max cycles reached,   │
│  3 consecutive low-yield cycles,│
│  or all sources exhausted       │
└─────────────────────────────────┘
```

Each cycle launches one sub-agent per persona in parallel, searching through different lenses simultaneously. The orchestrator collects results, deduplicates, logs, and checks the stop condition before the next cycle.

## Directory structure

The skill creates this structure in your workspace:

```
research/
├── personas/           # Who we research through
│   ├── [domain]/       # Grouped by research domain
│   │   └── [persona].md
│   └── ...
├── briefs/             # What we research
│   └── [brief].md
└── runs/               # Research output
    └── [brief-slug]/
        ├── run-log.md
        └── synthesis.md
```

## Synthesis & multi-perspective review

After a run completes, `/research synthesize` clusters findings into themes and reviews them through multiple analytical perspectives. Three modes:

1. **Custom lenses** — point the skill at your own perspective files (markdown describing analytical frameworks); one agent per lens reviews in parallel.
2. **Built-in perspectives** (default) — four generic angles:
   - **Pattern Recognition** — recurring themes, convergence points, underlying structure
   - **Technical Feasibility** — what's buildable, system implications, the smallest useful thing
   - **User Experience** — emotional patterns, narrative threads, user journey
   - **Risk Assessment** — echo-chamber effects, missing data, blind spots
3. **Skip** — generate a direct synthesis without multi-perspective review.

## Key concepts

| Concept | What it is |
|---|---|
| **Persona** | Simulated user whose perspective drives the search |
| **Brief** | Research question plus config |
| **Cycle** | One persona's search + extract + score |
| **Quality rubric** | Actionable + Evidenced + Novel (0-3) |
| **Keep/Discard** | Score >= 2 kept, < 2 discarded with a reason |
| **Run log** | All findings, kept and discarded |
| **Synthesis** | Multi-perspective themes |

## Acknowledgment

Inspired by Andrej Karpathy's [autoresearch](https://github.com/karpathy/autoresearch) — the loop discipline of fixed-budget cycles, objective keep/discard gates, and relentless iteration, adapted from ML training loops to web research. The difference: an open system searching the live web, a qualitative 3-point rubric instead of a single objective metric, multiple parallel personas instead of one agent, and a multi-perspective synthesis layer on top.

---

Part of [hurleywgly/skills](https://github.com/hurleywgly/skills). MIT licensed.
