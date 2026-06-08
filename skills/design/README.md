# design

> Turn a one-line brief into polished Figma screens

Most AI design output is a one-shot guess you have to clean up by hand. `design` runs the loop a real designer would: build it, step back, fix what's weak, repeat — so you end up with clean, consistent screens instead of a first draft that needs babysitting.

Built for AI coding agents (Claude Code, Codex, and more).

## Install

```bash
npx skills add hurleywgly/skills --skill design
```

Or add it for a specific agent, e.g. Claude Code:

```bash
npx skills add hurleywgly/skills --skill design -a claude-code
```

Manual: copy this folder into your agent's skills directory (e.g. `~/.claude/skills/design/` or `.agents/skills/design/`).

## What it does

- **Product idea to screens.** Describe what you want — a landing page, a multi-step flow — and the agent builds it in Figma section by section.
- **Designer critiquing its own work.** The agent screenshots each section, scores it on hierarchy, spacing, color, and type, then fixes what's weak and re-checks. You get clean, consistent layouts, not a draft you have to babysit.

## Why it matters

Most AI design output is a one-shot guess you have to clean up by hand. This still runs a loop like a real designer: design it, take a step back, make some changes, repeat. Incredibly powerful with a thorough style guide.

## How it fits your workflow

Take a nice HTML or React prototype you've worked on and use `design` to create a Figma replica. From there, iterations can be as hands-on (collaborative) or hands-off (autonomous) as the project calls for.

## Pairs well with

`build` • `ink` • `research`

## Usage

Just say what you want:

```
/design a landing page for a telehealth app
```

It turns your description into a brief and runs the loop. Point it at an existing brief instead:

```
/design run path/to/brief.md
```

Add `--stretch` to **any** run to go wide in one longer turn — more sections/screens, fewer checkpoints:

```
/design a 5-page marketing site for a telehealth app --stretch
```

### How the loop works

1. **Brief** — intent, feel, constraints, and an ordered list of sections.
2. **Section loop** — create → screenshot → score (6-point rubric) → fix → repeat (max 2 refinement cycles per section).
3. **Composition pass** — full-page screenshot, cross-section coherence check, spacing fixes.
4. **Motion spec** — precise animation direction (durations, easing, per-element timing).
5. **Finishing pass** — frame sizing, alignment, layer naming, token + text checks.
6. **Output** — a shareable HTML/PDF doc with the hero shot, design intent, screens, and motion spec.

It's honest about its ceiling: it produces B+ layouts a human designer can take to A in one focused session — not agency-level art direction. Driving Figma requires a Figma MCP connection. See [`SKILL.md`](./SKILL.md) for the full loop, rubric, budget model, and safety rules.

---

Part of [hurleywgly/skills](https://github.com/hurleywgly/skills). MIT licensed.
