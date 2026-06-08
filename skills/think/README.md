# think

> Harden any idea before it becomes a plan.

Most people underrate how good language models are as thought partners. `think` gives you a fast, multi-angle gut-check on a rough idea before you commit it to a plan or feature.

Built for AI coding agents (Claude Code, Codex, and more).

## Install

```bash
npx skills add hurleywgly/skills --skill think
```

Or add it for a specific agent, e.g. Claude Code:

```bash
npx skills add hurleywgly/skills --skill think -a claude-code
```

Manual: copy this folder into your agent's skills directory (e.g. `~/.claude/skills/think/` or `.agents/skills/think/`).

## What it does

- **Pressure-test before you commit.** Throw a half-formed idea, plan, or message at it and get a fast multi-angle read. It's like sharing your idea in front of peers, except you walk away with a tighter iteration instead of notes.
- **Poke holes one question at a time.** Let the agent interrogate you and challenge your best ideas, forcing you to think outside the box before you write another line of code.

## Why it matters

Most people underrate how effective language models are for thought partnership. `think` gives you a quick, multi-angle gut-check — the kind of pressure an idea needs before it turns into work.

## How it fits your workflow

Reach for `think` the moment you have a rough idea, before you've committed it to a plan or a feature. Paste in the rough idea, take the hardened read, answer a couple of its sharpest questions, then hand the sharpened version straight into planning or build.

## Pairs well with

`pitch-me` • `build` • `ink`

## Usage

```text
/think <idea|plan|file|brief>
  [--depth=quick|normal|deep]   # default: normal
  [--questions=N]               # quick 0-2, normal 3-5, deep 6-10
  [--manifest]                  # write a cwd-relative markdown record
```

A few ways to invoke it:

- `/think this onboarding flow — what am I missing?` — drop in a rough idea and get the four-pass hardening read, plus the strongest assumption and counterargument.
- `/think docs/strategy.md --depth=deep` — point it at a file or brief; it inspects the source first, then interrogates one sharp question at a time.
- `harden this before I build it` / `poke holes in this` — natural-language triggers work too; no flags required.

With no flags, it gives the hardening pass first and asks whether to keep going into interrogation when the next question would materially improve the idea.

---

Part of [hurleywgly/skills](https://github.com/hurleywgly/skills). MIT licensed.
