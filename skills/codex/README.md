# codex

> A Codex gut-check when Claude is the one driving.

Your current session is also its own biggest cheerleader. Pull in an independent model from a different lineage and you break the echo chamber — Codex catches what the model in the chair already rationalized past.

Built for AI coding agents (Claude Code, Codex, and more).

## Install

```bash
npx skills add hurleywgly/skills --skill codex
```

Or add it for a specific agent, e.g. Claude Code:

```bash
npx skills add hurleywgly/skills --skill codex -a claude-code
```

Manual: copy this folder into your agent's skills directory (e.g. `~/.claude/skills/codex/` or `.agents/skills/codex/`).

## What it does

- **Let a second model try to break it.** Consult Codex for a second opinion, play devil's advocate, or have it tackle a portion of the workflow and relay that back into the model calling the skill.

## Why it matters

Your current session is also your biggest cheerleader. Bringing in an independent model breaks the echo chamber and gives you a genuinely adversarial perspective.

## How it fits your workflow

Right before you push a new UI the driving model built, have Codex review the diff and tell you if anything's at-risk. When it flags enough of a risk, jump on the fix before getting the new feature out.

## Pairs well with

`claude` • `design` • `research` • `think`

## Usage

Three modes, auto-detected or named directly:

- **Review a diff with a pass/fail gate** — `/codex review` runs a Codex code review against your current branch versus its base, parses severity markers, and returns a PASS / FAIL / UNKNOWN gate. Add focus: `/codex review focus on security`.
- **Adversarial challenge** — `/codex challenge` turns Codex loose to find edge cases, race conditions, security holes, and failure modes. No compliments, just the problems. Add a focus area: `/codex challenge security`.
- **Consult on anything** — `/codex <your question>` asks Codex about the codebase in read-only mode and returns its answer verbatim.
- **Just `/codex`** — auto-detects: if there's a diff, it offers review / challenge / something else; otherwise it asks what to consult about.

Codex output is shown verbatim, and any disagreement from the driving model lands after the full response — never instead of it.

---

Part of [hurleywgly/skills](https://github.com/hurleywgly/skills). MIT licensed.
