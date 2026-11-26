---
name: pitch-me
description: "Pitch N distinct concepts before committing to one. Use when the user says \"pitch me\", \"give me N ideas\", \"N ways to\", \"throw spaghetti\", or when the open question is what to build rather than how. Each concept gets research backing and an independent outside take, is shown in whatever medium sells it best (diagram, wireframe, designed graphic, short video), and the set comes back as a ranked list with the reason for each rank, in one browsable HTML page. Not for convergent questions or when the direction is already locked."
argument-hint: "<brief> [--count=9] [--medium=auto|diagram|wireframe|graphic|video] [--screenshots] [--converge] [--no-outside-take]"
---

# /pitch-me

When the choice space is wide, get pitched before you commit. `/pitch-me` produces N distinct concept pitches against a brief, each shown in the medium that sells it, ranked with reasons, in a single browsable artifact.

## When to use

- "Give me 9 ways to..." / "Throw some spaghetti..."
- Pre-PMF concept exploration (game mechanics, content angles, product hooks)
- Cultural-moment response with a closing take-window
- Marketing or content angle ideation
- Any time you'd jump to "the obvious answer" — fan out first
- **Before** any planning pass when the question is "what should we build" rather than "how should we build X"

## When NOT to use

- Direction is already locked → go straight to planning
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
| Multi-perspective analysis pass | Convergence on the top picks |
| Planning pass | Turn the winning concept into a ship plan |
| `ink` (optional) | Renders the output page. If it is not installed, write a plain self-contained HTML page with the same sections |

## Invocation

```
/pitch-me <brief>
  [--count=9]                # 3–20, default 9
  [--medium=auto|diagram|wireframe|graphic|video]   # default auto: choose per pitch
  [--screenshots]            # browse + embed real-world parallels per concept
  [--converge]               # run a multi-perspective pass on the top 3 after the pitch
  [--no-outside-take]        # skip the outside-take step (not recommended)
```

## Flow

### 1. Frame
Extract from `<brief>`: goal, audience, constraints (tech / licensing / budget / timeline), and what a win looks like. If anything material is missing, ASK ONCE before fanning out — wrong constraints poison every concept downstream. If nobody is there to answer, state the assumption you are making at the top of the page and proceed.

### 2. Research fanout (3 parallel agents)
Run three research sub-agents in parallel (in Claude Code, three `general-purpose` Agents in a single message). If the host has no sub-agents, run the three passes yourself, one after another:

- **Agent A — Facts:** what's actually true about the topic. Sources, data, primary references. URLs cited inline.
- **Agent B — Conversation state:** what's already been said, what's the discourse temperature, what's been beaten to death, where's the white space.
Save what each pass returns as a short dossier in the run's `research/` folder (`a-facts.md`, `b-conversation-state.md`, `c-asker-posture.md`).

- **Agent C — Asker posture:** what tools/voice/aesthetic does the asker have available, what would feel "obviously them," what would feel off-brand. Reads from the project's root instruction file (AGENTS.md / CLAUDE.md), any notes, and recent work logs.

### 3. Independent outside take
Get a second opinion from a different AI system (through the `codex` or `claude` second-opinion skill in consult mode, if one is installed) with the brief + a synthesis of A/B/C, and save its output to `research/outside-take.txt`. Its job: sharpen the framing, name the failure mode of the obvious angle, propose 1–2 high-leverage moves that the in-house thinking will under-weight. This take is intentionally adversarial.

Skip with `--no-outside-take` only if you've already done this manually. If no second system is reachable, say so in the artifact rather than presenting an in-house take as independent.

### 4. Diverge
Generate N concepts. Each one must:

- Be playable / actionable / shippable within the brief
- Honor the constraints from Step 1
- Carry a thesis (or a different thesis from its siblings)
- Be genuinely different — no near-duplicates ("Version with X" + "Version with Y" doesn't count)

Write each pitch the way you would actually pitch it: a name, the hook in a sentence, how it works, what it would take to make, and the risk if there is a real one. Let the concept decide how much each of those needs; there is no fixed card to fill in.

### 5. Show each pitch in the medium that sells it
Pick the medium per pitch, and say in a line why it fits. The right one depends on what the idea is:

- **Diagram** — when the idea is a system, a flow, or a relationship between parts.
- **Wireframe** — when the idea is a screen or an interaction; show the moment that matters.
- **Designed graphic** — when the idea lives or dies on feel: a brand, a poster, a hero image.
- **Short video or animation** — when the idea is about motion, timing, or a sequence, and a still would undersell it.

These are starting points, not a menu. Mix them across the set, and use something else if it pitches the idea better. Make them with whatever the host has: inline SVG and HTML/CSS for diagrams, wireframes and simple animation; the host's image tool or an installed image skill for raster graphics; a video tool if one exists, otherwise a short coded animation. `--medium` forces one medium for the whole set.

Generated images and video usually cost money per render. Sketch every pitch with free, coded visuals first, and confirm with the user before paying for renders on more than the top few.

### 6. (Optional) Real-world screenshots
If `--screenshots`, for each concept use whatever browser tool the host provides (Claude Code's built-in browser pane or Codex's in-app browser; not the user's personal Chrome) to find the closest real-world parallel and embed an actual screenshot. Example: a Tinder-style concept → screenshot of an existing card-swipe interface. Helps the reader calibrate "I know what this looks like."

### 7. (Optional) Convergence pass
If `--converge`, after the pitch, run a multi-perspective analysis pass on the top 3 concepts in the ranking. This produces divergence → convergence in a single invocation. Output it as a second section in the artifact.

### 8. Rank, with reasons
Order the concepts from the one you would pursue first to the one you would drop, and give each a short rationale for its place: what it has over the one below it, and what holds it back from the one above.

Do this by comparison, not by scoring. Models are unreliable at absolute numbers: a guessed 7/10 or 82/100 looks precise, but it is not repeatable and carries no reasoning. They are much better at putting two options side by side and saying why one wins against what the brief is trying to achieve. So no stars, points, or percentages anywhere in the output. Where two concepts are genuinely close, say so and name what would break the tie.

End with where you would start and what would change your mind.

### 9. Render
Output one HTML page (with the `ink` skill if installed), saved at the path in Outputs below (that path wins over any default file name). Use a plain default style unless the user gave brand guidance. The page holds:

- Brief recap + constraints (safe / not-safe)
- Thesis strip (if a unifying argument emerged from research + the outside take)
- The outside take, verbatim, in a collapsed block
- The pitches in rank order, each with its visual and its rationale
- Where to start, and what would change that
- Next-move block

Let the page's layout follow the pitches: a set of videos and a set of diagrams should not look the same. A ranked stack usually reads better than a uniform card grid, because position carries the ranking.

## Outputs

| Artifact | Path | Consumer |
|---|---|---|
| Pitch page | `output/pitch-me/<slug>/concepts.html` | Human reader, share surface |
| Markdown manifest | `output/pitch-me/<slug>/manifest.md` | Planning pass, source of truth |
| Per-concept assets | `output/pitch-me/<slug>/assets/` | Downstream visual development |
| Research dossiers | `output/pitch-me/<slug>/research/` | Reference; cited inline in concepts |

Slug derived from brief topic (kebab-case, suffixed with date if collision).

## Anti-patterns

- **N concepts that are M minor variations** — diversity beats count. Better to ship 6 truly different concepts than 12 with palette swaps.
- **Skipping the outside take "to save time"** — losing the independent take is losing the value. Use `--no-outside-take` only if you've done the equivalent manually.
- **Paying to render every concept** — sketch all of them for free first; spend on the few that earned it.
- **A number where a reason should be** — a score invites false precision and hides the thinking. Rank and explain.
- **One medium for everything by habit** — nine identical cards flatten nine different ideas.
- **Posting the exploration as the deliverable** — `/pitch-me`'s output is divergent thinking, not finished work. It's the menu, not the meal. Always pair with a planning pass or direct execution.
- **Letting the recommendation tail wag the dog** — if the ranking is foregone before research, you've skipped the divergent step. Re-run with truly open framing.

## Pattern

Diverge before you converge. A multi-perspective analysis pass is the convergence move; `/pitch-me` is the divergence move. The pair is the creative engine.

## Reference invocations

```
# Spaghetti-throw on a cultural moment
/pitch-me "How should we respond to this week's big cultural moment?" --count=9

# Pre-PMF feature ideation with real-world parallels
/pitch-me "What's the killer first feature for the free tier?" \
  --count=12 --screenshots

# Launch exploration where feel matters, with a convergence pass
/pitch-me "Landing-page hero treatments for the new site" \
  --count=6 --medium=graphic --converge

# Quick brainstorm, no outside take, just divergence
/pitch-me "Names for the new feature" --count=15 --no-outside-take
```
