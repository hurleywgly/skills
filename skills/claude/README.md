# claude

> A Claude gut-check when another model is the one driving

When a different model runs your session, it's too easy to trust its read of its own work. This pulls in Claude as an independent second opinion — a model from a different lineage that catches what the first one rationalized past.

Built for AI coding agents (Claude Code, Codex, and more).

## Install

```bash
npx skills add hurleywgly/skills --skill claude
```

Or add it for a specific agent, e.g. Claude Code:

```bash
npx skills add hurleywgly/skills --skill claude -a claude-code
```

Manual: copy this folder into your agent's skills directory (e.g. `~/.claude/skills/claude/` or `.agents/skills/claude/`).

## What it does

- **Let a second model try to break it.** Consult Claude for a second opinion, play devil's advocate, or hand it a slice of the workflow — then relay the result back into the model running the session.

## Why it matters

When another model is driving your session, it's too easy to trust its own read of its own work. A model from a different lineage catches what the first one rationalized past. Model strengths and weaknesses shift over time, and this skill lets you play to Claude's strengths even when you're outside Claude or Claude Code.

## How it fits your workflow

When a different model is running the session, fire off the Claude skill to consult or piece together a part of the plan. It almost always brings a different perspective.

## Pairs well with

`codex` • `design` • `research` • `think`

## Usage

Three modes, parsed from how you invoke it:

```text
claude review                 # review the branch diff, with a PASS/FAIL gate
claude review <instructions>  # same, but focus the review
claude challenge              # adversarial — try to break the code or plan
claude challenge <focus>      # adversarial, scoped to a specific concern
ask claude <question>         # consult — ask anything about the code or plan
```

In review mode it inspects the current branch diff against your base branch and returns findings ordered by severity. Critical findings (`[P0]`, `[P1]`, `critical`, `high`) fail the gate so you catch the risk before shipping. All Claude output is shown verbatim, never summarized.

---

Part of [hurleywgly/skills](https://github.com/hurleywgly/skills). MIT licensed.
