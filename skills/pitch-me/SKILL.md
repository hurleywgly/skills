---
name: pitch-me
description: "Pitch N distinct concepts before committing to one. Use when the user says \"pitch me\", \"give me N ideas\", \"N ways to\", \"throw spaghetti\", or when the open question is what to build rather than how. Each concept gets research backing, an independent outside take, a visual, and a viability score, rendered as one browsable HTML grid. Not for convergent questions or when the direction is already locked."
argument-hint: "<brief> [--count=9] [--visual=svg|nano|mj] [--screenshots] [--council] [--no-outside-take]"
---

# /pitch-me

When the choice space is wide, get pitched before you commit. `/pitch-me` produces N distinct concept pitches against a brief, each visualized and viability-scored, in a single browsable artifact.

## When to use

- "Give me 9 ways to..." / "Throw some spaghetti..."
- Pre-PMF concept exploration (game mechanics, content angles, product hooks)
- Cultural-moment response with a closing take-window
- Marketing or content angle ideation
- Any time you'd jump to "the obvious answer" — fan out first
- **Before** any planning pass when the question is "what should we build" rather than "how should we build X"

## When NOT to use

- Direction is already locked → use a planning pass
- Question is binary → just decide
- You need execution, not exploration → build it directly
- Question is convergent (single best answer exists) → use a multi-perspective analysis pass

## Composes with

```
/pitch-me (diverge)  →  multi-perspective analysis (converge)  →  planning pass (plan)  →  build (ship)
```

| Skill | Role |
|---|---|
| `/pitch-me` | Spread N concepts wide |
| Multi-perspective analysis pass | Multi-perspective convergence on top picks |
| Planning pass | Turn the winning concept into a ship plan |
| An image-prompt skill (optional) | Develop the visual hero for the chosen direction |
| `/ink` | The output format. If `ink` is not installed, write a plain self-contained HTML grid with the same sections |
| Multi-phase workflow | Wrap the whole pipeline across multiple sessions |

## Invocation

```
/pitch-me <brief>
  [--count=9]                # 3–20, default 9
  [--visual=svg|nano|mj]     # default svg
  [--screenshots]            # browse + embed real-world parallels per concept
  [--council]                # auto-run a multi-perspective analysis pass on top 3 after the pitch
  [--no-outside-take]        # skip the independent outside-take step (not recommended)
```

## Flow

### 1. Frame
Extract from `<brief>`: goal, audience, constraints (tech / licensing / budget / timeline), success metric. If anything material is missing, ASK ONCE before fanning out — wrong constraints poison every concept downstream.

### 2. Research fanout (3 parallel agents)
Run three research sub-agents in parallel (in Claude Code, three `general-purpose` Agents in a single message). If the host has no sub-agents, run the three passes yourself, one after another:

- **Agent A — Facts:** what's actually true about the topic. Sources, data, primary references. URLs cited inline.
- **Agent B — Conversation state:** what's already been said, what's the discourse temperature, what's been beaten to death, where's the white space.
- **Agent C — Asker posture:** what tools/voice/aesthetic does the asker have available, what would feel "obviously them," what would feel off-brand. Reads from the project's root instruction file (CLAUDE.md / AGENTS.md), any memory/ notes, and recent work logs.

### 3. Independent outside take
Get an independent second opinion from another AI system (via the `codex` or `claude` skill in consult mode, if one is installed) with the brief + a synthesis of A/B/C. Its job: sharpen the framing, name the failure mode of the obvious angle, propose 1–2 high-leverage moves that the in-house thinking will under-weight. This take is intentionally adversarial.

Skip with `--no-outside-take` only if you've already done this manually. If no second system is reachable, say so in the artifact rather than presenting an in-house take as independent.

### 4. Diverge
Generate N concepts. Each one must:

- Be playable / actionable / shippable within the brief
- Honor the constraints from Step 1
- Carry a thesis (or a different thesis from its siblings)
- Be genuinely different — no near-duplicates ("Version with X" + "Version with Y" doesn't count)

Per concept, capture:

| Field | Notes |
|---|---|
| Name | 1–4 words, evocative |
| Tagline | One sentence — the hook |
| Mechanic | 1–2 sentences — how it actually works |
| Tech path | Specific stack / API / library |
| Viral / value score | ★ 1–5 |
| Build cost | S / M / L / XL |
| Risk callout | Only if non-trivial — keep most cards risk-free |

### 5. Visualize
Per concept, render a visual at the chosen fidelity:

- **`svg`** *(default)* — coded iconic sketch, instant, free, illustrative. Best for spaghetti-throw mode where speed matters.
- **`nano`** — Nano Banana 2 illustration (~$0.04 per concept). Better hero shots when text overlays in HTML afterward.
- **`mj`** — Full Midjourney render (~$0.10 per concept, slower). Reserved for serious / shippable explorations.

Default to `svg`. Upgrade to `nano`/`mj` only for the picked concept(s) downstream. Both cost money per image, so confirm before rendering more than a handful.

### 6. (Optional) Real-world screenshots
If `--screenshots`, for each concept use whatever browser tool the host provides (for example Claude in Chrome) to find the closest real-world parallel and embed an actual screenshot. Example: a Tinder-style concept → screenshot of an existing card-swipe interface. Helps the reader calibrate "I know what this looks like."

### 7. (Optional) Convergence pass
If `--council`, after the pitch, run a multi-perspective analysis pass on the top 3 concepts (by viral × build-cost-inverse score). This produces divergence → convergence in a single invocation. Output the convergence pass as a second section in the artifact.

### 8. Recommend
Synthesize into three buckets:

- **Ship now** — 1–2 concepts that fit the brief immediately
- **Follow-up** — concepts worth developing in week 2+ if the first ship lands
- **Skip / pivot** — concepts that don't fit the brief but might compose into adjacent work (e.g., a feature on a different product, a separate skill)

### 9. Render
Output a `/ink` exploration grid with:

- Brief recap + constraints block (safe / not-safe two-column)
- Thesis strip (if a unifying argument emerged from research + the outside take)
- N concept cards (3-up grid, responsive)
- Recommendation strip (3 buckets, color-coded)
- 2–3 visual direction prompts for the next step
- Next-move block

## Outputs

| Artifact | Path | Consumer |
|---|---|---|
| Exploration HTML | `./output/pitch-me/<slug>/concepts.html` | Human reader, share surface |
| Markdown manifest | `./output/pitch-me/<slug>/manifest.md` | Planning pass, multi-phase workflow, source of truth |
| Per-concept assets | `./output/pitch-me/<slug>/assets/` | Downstream visual development |
| Research dossiers | `./output/pitch-me/<slug>/research/` | Reference; cited inline in concepts |

Slug derived from brief topic (kebab-case, suffixed with date if collision).

## Anti-patterns

- **N concepts that are M minor variations** — diversity beats count. Better to ship 6 truly different concepts than 12 with palette swaps.
- **Skipping the outside take "to save time"** — losing the independent take is losing the value. Use `--no-outside-take` only if you've done the equivalent manually.
- **Auto-rendering hero MJ images for all N concepts** — start with SVG sketches; render the chosen direction later. Don't burn $0.10 × 9 on unpicked work.
- **Posting the exploration as the deliverable** — `/pitch-me`'s output is divergent thinking, not finished work. It's the menu, not the meal. Always pair with a planning pass or direct execution.
- **Letting the recommendation tail wag the dog** — if the recommendation is foregone before research, you've skipped the divergent step. Re-run with truly open framing.

## Pattern

Diverge before you converge. A multi-perspective analysis pass is the convergence move; `/pitch-me` is the divergence move. The pair is the creative engine.

## Reference invocations

```
# Spaghetti-throw on a cultural moment
/pitch-me "How should I respond to Drake's three-album drop?" --count=9

# Pre-PMF feature ideation with real-world parallels
/pitch-me "What's the killer first feature for the product's free tier?" \
  --count=12 --screenshots

# High-fidelity exploration for a launch
/pitch-me "Landing-page hero treatments for the v6 portfolio" \
  --count=6 --visual=mj --council

# Quick brainstorm, no outside take, just divergence
/pitch-me "Names for the new skill" --count=15 --no-outside-take
```

