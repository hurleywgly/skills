---
name: design
description: "Run an autonomous Figma design loop from a written brief: build section by section, screenshot, self-critique against a rubric, fix, and repeat until quality converges or the call budget runs out, then hand off a shareable document. Use for brief-driven screen designs or style boards in Figma. Requires the Figma MCP server and its figma-use skill."
argument-hint: "<description> | new [--type style-board|screen-design] | run <brief-path> [--budget N] [--autonomous] [--stretch]"
disable-model-invocation: true
---

# /design

Autonomous visual design loop — create, critique, refine, and document visual designs in Figma.

## Purpose

Run structured design work through Figma's MCP tools. The core innovation: a **recursive self-critique loop** where the agent creates, screenshots, evaluates its own work via vision analysis, makes targeted fixes, and repeats until quality converges or budget exhausts.

Same loop DNA as a brief-driven research or build loop (scored, gated, structured logging), adapted for visual design where iteration means **section-level refinement with objective scoring**.

## Subcommands

The simplest invocation is a plain description — `/design a landing page for a telehealth app` — which turns what you said into a brief and runs the loop. Add `--stretch` to any invocation to go wider in one longer turn. The explicit subcommands below give finer control.

### `/design new`

Guided brief creation + execution. Asks targeted questions based on what's missing, then runs.

**Flags:**
- `--type style-board|screen-design` — skip type selection (default: ask)
- `--autonomous` — skip human checkpoints (still respects call budget and self-critique loop)
- `--stretch` — longer breadth-scaled turn (more sections/screens), fewer checkpoints, deterministic stop, hands back (see **Gear: `--stretch`** below)

### `/design run [brief-path]`

Execute or resume a design run from an existing brief file.

**Flags:**
- `--budget N` — override max Figma API calls for this run (default: 60)
- `--autonomous` — skip human checkpoints
- `--stretch` — longer breadth-scaled design turn (more sections/screens), fewer checkpoints, deterministic stop, hands back (see **Gear: `--stretch`** below)

---

## Gear: `--stretch`

`--stretch` runs `/design` as a **longer, breadth-scaled gated turn** — the design loop running long, NOT an unattended overnight run.

**What it changes:** raises the run's `max_calls` ceiling to cover more sections/screens in one turn (e.g. a full multi-page site rather than a single landing page), checks in less often, and hands back the assembled artifact + scores at a deterministic stop (all sections converged · stretch call-ceiling · daily floor · two-429 abort).

**What it never changes** (stretch goes wider, not lower-quality):
- The **self-critique loop is NOT skipped** — every section still creates → screenshots → scores → fixes. stretch covers more sections, not sloppier ones.
- The **daily rate-tracker floor stays** — still refuse to start under 20 remaining; stretch raises the *run* budget, never the daily safety floor.
- Figma isolation (new page), per-section budget fairness, and the two-429 abort all still apply.
- The diverge checkpoint stays mandatory at least once — never self-approve a direction.

Composes with `--autonomous` (skip interactive checkpoints; self-critique still runs): `/design run [brief] --stretch --autonomous` = a long, multi-section turn with no mid-run pauses that still hands back at the deterministic stop. Triggers on **breadth** (section/screen count, scope), not risk.

---

## Brief Schema

Briefs live in `skills/design/runs/[slug]/brief.md`. YAML frontmatter + markdown body.

```markdown
---
slug: homepage-redesign
type: screen-design              # style-board | screen-design
status: draft                    # draft | active | iterating | complete
figma_file_key: null             # null = create new file; or existing file key
figma_page_name: null            # null = create new page
max_iterations: 2                # refinement cycles per section (recommended: 2)
max_calls: 60                    # hard cap on Figma API calls this run
quality_floor: 4                 # minimum rubric score to advance (out of 6)
checkpoint_every: 3              # human checkpoint interval (sections completed)
motion_spec: true                # generate animation/motion annotations
created: 2026-04-05
---

# [Design Name]

## Intent
[1-2 sentences: what this design needs to accomplish.]

## Feel
[Evocative phrases. "Poolsuite warmth meets Linear precision"]

## Inspiration
- [image path, URL, or Figma link]

## Anti-References
[What to avoid]

## Constraints
[Brand rules, viewport targets, tech stack]

## Sections
[Ordered list of sections to design. Each gets its own iteration cycle.]
1. Navigation
2. Hero
3. Value props
4. Templates
5. Final CTA
6. Footer

## Existing Work
[Figma files, style guides, token pages to reference]
```

---

## The Self-Critique Rubric

Every screenshot is scored against 6 objective criteria. Each scores 0 (fail) or 1 (pass).

| # | Criterion | 0 (fail) | 1 (pass) | How to check |
|---|-----------|----------|----------|-------------|
| 1 | **Hierarchy** | Elements compete, no focal point | Clear primary > secondary > tertiary | Squint test at 50% zoom |
| 2 | **Spacing** | Irregular gaps, elements feel random | Consistent rhythm, gaps are multiples of 4px | Visual measurement |
| 3 | **Color system** | Off-brand colors, rogue values | All colors match declared token set | Compare to brief's color tokens |
| 4 | **Typography** | Mixed sizes without purpose | Clear type scale, mono on data, readable | Count distinct sizes (max 3-4 per section) |
| 5 | **Density** | Too sparse (wireframe) or too cramped | Professional density — information-rich, not cluttered | Does it look like a shipped product? |
| 6 | **Completeness** | Missing elements, placeholder text, dead ends | All scoped elements present with realistic content | Compare to section spec in brief |

**Scoring thresholds:**
- **Score 5-6:** Converged. Stop iterating on this section.
- **Score 3-4:** Targeted fixes needed. Run one more refinement cycle.
- **Score 0-2:** Structural rework needed. Flag for human review before burning more calls.

**What the rubric does NOT evaluate (flag for human, don't score):**
- "Does it feel on-brand?" — too subjective for self-critique
- "Would a user trust this?" — needs human judgment
- Animation timing and easing — can't evaluate from static screenshot

---

## Behavior: `/design run`

### Phase 1: Load Brief + Budget Check

1. Read brief file, validate required fields (intent, scope, sections)
2. **Check daily budget.** Read `skills/design/rate-tracker.json`
   - If remaining < `max_calls`: warn user, suggest reducing scope
   - If remaining < 20: refuse to start
3. **Calculate per-section budget:** `max_calls / (sections × 3)` — ensures fair distribution
4. Create run directory, initialize `run-log.md`

### Phase 2: Figma Setup

1. **File resolution:** create new or verify existing
2. **Page isolation:** create a new dedicated page for the run and write only there. Existing pages hold the user's own work, and a run that writes into them cannot be cleanly undone.
3. **Token page (for multi-screen runs):**
   - Create a "Design Tokens" frame with color swatches, type scale, spacing scale, button variants
   - This is the ground truth for cross-screen consistency
   - Cost: 2-3 calls. Pays back across all screens.
4. **Context scan** if existing work referenced

**Increment call counter after every Figma MCP tool call.**

### Phase 3: Section Loop (The Recursive Core)

For each section in the brief's section list, in order:

```
SECTION LOOP:
  Step 1: CREATE section in Figma (1-3 use_figma calls)
  Step 2: SCREENSHOT the section (1 get_screenshot call)
  Step 3: SCORE against 6-point rubric (free — vision analysis, no API call)
  Step 4: DECISION
    if score >= quality_floor → ADVANCE to next section
    if score < quality_floor AND iterations < max_iterations → FIX and re-score
    if iterations >= max_iterations → ADVANCE with flag
    if score decreased from previous iteration → STOP, flag regression
  Step 5: LOG iteration (score, issues, fixes applied, call count)
```

**Refinement cycle (Step 4 → FIX):**
1. The critique output must include **specific fix instructions**, not just problems
   ```
   ISSUE: Feature cards have uneven spacing — left gap ~40px, right ~20px
   FIX: Set uniform gap in auto-layout to 24px on node [ID]
   ```
2. Apply targeted fixes via `use_figma` (1-2 calls)
3. Re-screenshot and re-score
4. Max 2 refinement cycles per section (the sweet spot — cycle 1 catches 70% of issues, cycle 2 catches 20%, cycle 3 is almost always wasted)

**Budget per section:** ~7 calls (create 3 + screenshot 1 + fix 2 + screenshot 1)

**Checkpoint** every `checkpoint_every` sections:
Present scores, screenshots, and remaining budget. Let human redirect before burning more calls.

### Phase 4: Full-Page Composition Pass

After all sections are built:

1. **Screenshot the full page** (1 call)
2. **Evaluate cross-section coherence** (free vision analysis):
   - Vertical rhythm between sections
   - Color balance across the whole composition
   - Consistent header/CTA/footer sizing
3. **Fix section spacing** if needed (1-2 calls)
4. **Final screenshot** (1 call)

### Phase 5: Motion Spec (if `motion_spec: true`)

Generate animation/motion direction. Figma is static, but the agent specifies motion precisely.

**Create a "Motion Spec" frame** on the same page with:

```
MOTION SYSTEM
| Pattern    | Duration | Easing              | Use                          |
|------------|----------|---------------------|------------------------------|
| enter      | 400ms    | ease-out-expo       | Elements entering viewport   |
| exit       | 200ms    | ease-in             | Elements leaving             |
| micro      | 150ms    | ease-in-out         | Hover, toggle, button press  |
| emphasis   | 600ms    | spring(1, 80, 10)   | Celebration, completion      |
```

**Per-section motion annotations:**
```
HERO
  1. Headline — fade-in + translateY(20px→0), 600ms ease-out, delay 0ms
  2. Subhead — fade-in, 400ms ease-out, delay 200ms
  3. CTA — fade-in + scale(0.95→1), 400ms spring, delay 400ms
  4. Hero visual — bars stagger-in left→right, 30ms stagger, 300ms each
```

Cost: 1-2 `use_figma` calls for the spec frame.

### Phase 6: Finishing Pass

Before presenting, run invisible craft checks:

1. **Frame sizing:** Set `clipsContent = false` and `layoutSizingVertical = "HUG"` on all container frames (prevents collapsed/clipped content)
2. **Alignment audit:** Verify consistent spacing
3. **Layer naming:** Rename auto-generated names ("Rectangle 47" → meaningful)
4. **Color check:** Verify all colors match token set
5. **Text check:** No placeholder text remaining

### Phase 7: Output Document

Generate a shareable HTML/PDF document:
1. Hero shot of final design
2. Design intent (3-4 key decisions)
3. Screens grouped by flow
4. Motion spec summary
5. What's next

### Phase 8: Close Run

1. Update brief frontmatter: `status: complete` (or `iterating` if pausing mid-run)
2. Update rate tracker with final call count
3. **Write pickup note** at bottom of run-log (see Session Handoff below)
4. **Project logging:** If the run is tied to a project, log the design work into that project's files:
   - Add an entry to the project's worklog/changelog
   - Update project state with the Figma file key + page name so downstream build work can reference the designs
   - Follow a dual-logging pattern: design work belongs to the project, not just the skill
   - For standalone one-off designs (not tied to a project), no external logging needed
5. Report: Figma link, call count, scores, flagged items

---

## Session Handoff

Design sessions consume large context windows. The system must support clean session boundaries.

### Closing a Session

Before ending a conversation with active design work, write a **pickup note** at the bottom of the run-log:

```markdown
## Pickup Note (YYYY-MM-DD)
**Last worked:** [section/screen name], iteration [N], score [N/6]
**Next:** [specific next action — what to build or fix]
**Reviewer feedback:** [any direction, preferences, or corrections from this session]
**Remaining budget:** [N] calls today
**Open questions:** [anything unresolved]
**Figma state:** file [key], page "[name]", [N] screens complete
```

### Starting a New Session

When resuming a `/design run`:
1. Read the brief (frontmatter has status + current state)
2. Read the run-log's last pickup note
3. Read Figma file metadata (`get_metadata`) to verify current state
4. Continue from where the pickup note says

No capsule needed for same-project continuation — the run directory IS the state.

### Design → Build Handoff

`/design` does NOT hand off directly to code. The flow is:

```
/design → Figma artifacts (screens, components, tokens, motion spec)
    ↓
Project requirements/tasks reference the Figma designs
    ↓
a build loop pulls tasks → consults Figma designs as context → implements
    ↓
implementation may use a Figma-to-code tool (e.g. /figma-implement-design)
```

Design is an input to the build loop. The build loop owns the technical lens — requirements, architecture, testing. `/design` owns the visual lens — layout, tokens, motion, brand fidelity. They reference each other but don't call each other directly.

---

## Figma Frame Rules

These prevent the "collapsed container" problem where you have to manually expand frames.

1. **`clipsContent = false`** on every container and section frame
2. **`layoutSizingVertical = "HUG"`** on page-level and section-level frames — let content determine height
3. **Only use fixed `resize()`** for elements with known dimensions (buttons, icons, specific cards)
4. **Top-level screen frames:** width fixed (1440), height HUG
5. **Never hardcode height** on auto-layout parents — they should grow with content

---

## Rate Limit Management

### Call Budget

Track in `skills/design/rate-tracker.json`:
```json
{ "date": "2026-04-05", "calls": 0 }
```

- **Before each call:** check run budget AND daily budget (reserve 20 for manual use)
- **At 75% of run budget:** switch to finalize mode (polish only)
- **On 429 response:** wait 60 seconds. Two 429s = abort with summary.

### Call Cost Estimates

| Operation | Typical calls |
|-----------|--------------|
| File + page + token page setup | 3-5 |
| One section (create + screenshot) | 4-5 |
| One refinement cycle (fix + screenshot) | 2-3 |
| Full-page composition pass | 3-4 |
| Motion spec | 1-2 |
| Finishing pass | 2-3 |

**Budget models:**

| Scope | Sections | Iterations | Total calls |
|-------|----------|-----------|------------|
| Style board | 6 | 1 each | ~35-45 |
| Landing page (6 sections) | 6 | 2 each | ~55-70 |
| 5-page site | 25+ | 2 each | ~120-150 |

---

## The 80/20 of Visual Polish

Five things that make the biggest difference. These should be explicit sub-checks in the rubric:

1. **Consistent spacing scale** — Use 4/8/12/16/24/32/48/64. Nothing else. Eliminates 50% of "it feels off."
2. **Layered shadows, not flat borders** — Two-layer shadows (subtle ambient + directional) make surfaces real.
3. **Type scale discipline** — Max 3 sizes per section: heading, body, caption.
4. **Color restraint** — Max 2 accent colors per screen. Everything else is surfaces.
5. **Whitespace as a feature** — 48-80px vertical section padding. Content needs breathing room.

---

## Safety Rules

### Figma Isolation
1. Create a new page for every design run (see Page isolation in Phase 2)
2. Never delete objects the skill didn't create
3. Pre-flight scan before writes
4. Set `clipsContent = false` on all containers

### /figma-use Loading
Load the `/figma-use` skill before every `use_figma` call. The Figma MCP server requires it, and calls made without it fail or write malformed nodes.

### Human Gates
- Never self-approve a design direction (diverge checkpoint is mandatory)
- Checkpoints present a position + specific question
- `--autonomous` skips human checkpoints but still runs self-critique loop

### Budget Protection
- Hard cap per run. Log every call.
- Daily awareness: warn < 50 remaining; refuse < 20
- Per-section budget prevents one section from starving others

---

## Outputs

| Artifact | Path | Shape | Consumed by |
|----------|------|-------|-------------|
| Figma file | Figma (file key + page name) | Frames per brief sections | Human review, `/figma-implement-design` |
| Run log | `design/runs/[slug]/run-log.md` | Cycle history, scores, pickup note, budget tracking | `/design run` resume, human review |
| Output doc | Generated as shareable HTML/PDF | Hero shot + intent + screens + motion + next | Human, sharing |
| Project log | The project's worklog/changelog | Design entry with Figma key + page name | A build loop (indirectly, via project tasks) |

**Handoff rule:** `/design` artifacts feed a build loop via project tasks, NOT directly to code. If output paths change, update this table.

## Multi-Page Coherence

For runs with multiple screens:

1. **Token page first** — build before any screens. Color swatches, type scale, button variants. Cost: 2-3 calls.
2. **JS constants in every script** — define colors/sizes at top of each `use_figma` call
3. **Coherence verification pass** — after all screens built, screenshot each, run one vision comparison checking: header heights, CTA consistency, font sizes, footer match
4. **Fix drift** before closing

---

## Run Directory Structure

```
skills/design/
├── SKILL.md
├── rate-tracker.json
└── runs/
    └── [slug]/
        ├── brief.md
        ├── run-log.md
        ├── screenshots/
        │   ├── section-hero-v0.png
        │   ├── section-hero-v1.png
        │   ├── full-page-final.png
        │   └── ...
        ├── motion-spec.md        # if motion_spec: true
        └── output.html           # shareable HTML/PDF document
```

---

## Integration

| Skill | Relationship |
|-------|-------------|
| `/figma-use` | **Mandatory prerequisite** — loaded before every `use_figma` call |
| HTML/PDF export | Output document generation |
| Research findings | Inform brief requirements |
| A build loop | Project tasks may trigger design briefs; consumes design artifacts |
| `/figma-generate-design` | May use for initial bulk screen generation |
| `/figma-implement-design` | Downstream — turns designs into code |

---

## Quality Ceiling (Honest Assessment)

The recursive loop produces **B+ quality** — clean, consistent, well-spaced, design-system-correct layouts. It raises the floor significantly (C+ → B+) by catching spacing errors, color drift, hierarchy problems, and missing elements.

It does NOT produce agency-level (A+) work. That requires:
- Custom illustration and iconography
- Micro-typographic decisions (kerning, optical alignment)
- Intentional rule-breaking by someone who knows which rules to break
- Art direction — choosing *what* to show, not just *how*

**The honest framing:** This system produces layouts that a human designer could take from B+ to A in one focused session. That is genuinely valuable compared to starting from a blank file.
