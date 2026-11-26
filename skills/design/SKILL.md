---
name: design
description: "Run a visual design loop from a written brief or a plain description: explore several directions, narrow to one, then build section by section, get each round critiqued by an outside reviewer, fix, and repeat until it converges or the budget runs out, ending in a shareable document. Prefers Figma; works without it by drawing on an HTML/SVG canvas or an open-source design tool. Use for brief-driven screen designs or style boards; --stretch runs a longer, breadth-scaled turn."
argument-hint: "<description> | new [--type style-board|screen-design] | run <brief-path> [--canvas figma|html|<tool>] [--budget N] [--autonomous] [--stretch]"
disable-model-invocation: true
---

# /design

A design loop that explores before it commits, then builds, gets critiqued from outside, and refines, staying on the original request the whole way.

## How it works

The shape is the double diamond from product design: go wide, narrow, then build and narrow again.

1. **Frame** the request.
2. **Diverge:** produce several genuinely different directions.
3. **Converge:** pick a smaller subset or one, with a stated reason. This is the diverge checkpoint.
4. **Build and refine:** create a section, capture it, have an outside reviewer critique it against the rubric, fix, repeat.
5. **Compose, finish, and hand off** a shareable document.

Two things hold across every step. The original request is the reference point: before each round, reread the brief's Intent and drop any change that does not serve it, because long loops drift toward polishing whatever is on screen. And the agent never approves its own direction or its own work as final; a human or an outside reviewer does.

## Invocation

The simplest form is a plain description, `/design a landing page for a telehealth app`, which becomes a brief and runs the loop.

- `/design new` asks only for what is missing from the brief, then runs. `--type style-board|screen-design` skips the type question.
- `/design run [brief-path]` executes or resumes a run from a brief.
- `--canvas figma|html|<tool>` picks where the design is drawn (see Canvas). Default: Figma when it is connected, otherwise HTML.
- `--budget N` overrides the run's call budget (Figma canvas only).
- `--autonomous` skips the human checkpoints after the diverge checkpoint. Outside critique still runs.
- `--stretch` runs a longer, wider turn; see Gears.

## Canvas

Prefer Figma, because the result is editable by a designer and feeds the build flow. It is not required.

| Canvas | Use when | How a round is captured |
|---|---|---|
| **Figma** | The Figma MCP server is connected | Screenshot of the frame. Read `references/figma.md` before the first call: it holds the page-isolation, frame, budget and rate-limit rules. |
| **HTML/SVG** | No Figma, or the user wants a file they can open anywhere | One self-contained HTML file per run, rendered in the host's browser and screenshotted |
| **Open-source design tool** | The user names one the host can drive (a whiteboard or vector tool with an API, CLI or MCP server) | That tool's export or a screenshot |

Say which canvas you chose and why in one line. The loop, rubric and critique are the same on every canvas; only the drawing and capture calls differ. If the preferred canvas fails mid-run, say so and ask before switching, since the two results are not interchangeable.

## The brief

Briefs and all run state live in `output/design/runs/[slug]/`, relative to the workspace root. A brief is YAML frontmatter plus a short markdown body:

```markdown
---
slug: example-landing
type: screen-design              # style-board | screen-design
status: draft                    # draft | active | iterating | complete
canvas: figma                    # figma | html | <tool name>
directions: 3                    # how many directions to explore before converging
max_iterations: 3                # refinement rounds per section
review_rounds: 2                 # outside-critique rounds on the composed whole
quality_floor: 4                 # minimum rubric score to advance (out of 6)
checkpoint_every: 3              # human checkpoint interval (sections completed)
motion_spec: true                # write animation/motion annotations
---

# [Design name]

## Intent
[1-2 sentences: what this design needs to accomplish. Every round is checked against this.]

## Feel
[Evocative phrases.]

## Inspiration
- [image path, URL, or design link]

## Anti-References
[What to avoid]

## Constraints
[Brand rules, viewport targets, tech stack]

## Tokens
[Colors, type sizes and spacing scale this design must use. The rubric's color and spacing checks compare against these; if none are given, declare them here before building.]

## Sections
[Ordered list. Each gets its own refinement loop.]

## Existing Work
[Files, style guides, token pages to reference]
```

Figma runs add `figma_file_key`, `figma_page_name` and `max_calls`; see `references/figma.md`.

## The loop

### 1. Frame

Read the brief (or turn the description into one). Restate the Intent in one sentence and list what is out of scope. If something material is missing, ask once.

### 2. Diverge

Produce `directions` (default three) genuinely different takes on the whole design: different layout idea, different visual attitude, different emphasis. Three colorways of one layout do not count. Keep them cheap: a rough frame, a small HTML sketch, or a thumbnail each, enough to react to. On the HTML canvas put all of them side by side in one `directions.html` and capture it as `screenshots/00-directions`. The point is to see the range before committing, because the first idea is usually the most expected one.

### 3. Converge (the diverge checkpoint)

Show the directions side by side with one line each on what it bets on and where it is weak. Recommend a subset or one, and say why. Then stop for the human's choice. This checkpoint always happens at least once per run, including under `--autonomous` and `--stretch`; the agent does not pick its own direction. If the human combines two, restate the combined direction before building.

### 4. Build and refine, per section

For each section in the brief, in order:

1. **Create** the section on the canvas.
2. **Capture** it (screenshot or export).
3. **Critique from outside.** Send the capture, the brief's Intent, Constraints and Tokens, and the rubric to a reviewer that did not build it (see Outside critique). A screenshot alone cannot show exact gaps or color values, so also send the measured ones (computed spacing and colors from the browser, or the values from the canvas) or the reviewer will fail those criteria for lack of evidence. Ask for a score per criterion and, for each problem, the specific fix.
4. **Decide.** Score at or above `quality_floor`: advance. Below it with rounds left: apply the fixes and repeat from step 2. Out of rounds: advance and flag the section. Score fell since the last round of the same section: stop and flag the regression.
5. **Log** the round: score, issues, fixes, and a one-line request check ("still serving: [Intent]").

Check in with the human every `checkpoint_every` sections: scores, captures, remaining budget, and one specific question.

### 5. Compose

Once all sections exist, capture the whole design and run `review_rounds` outside-critique rounds on it: vertical rhythm, color balance, consistency of repeated elements, and whether the whole still answers the Intent. Keep going past `review_rounds` only while the reviewer is still finding problems that matter and budget remains. Changes made after the final review round have not been reviewed: either spend one more round on them or say plainly in the hand-off that they are unreviewed.

### 6. Motion spec (if `motion_spec: true`)

Static canvases cannot show motion, so write it down: a small motion system (enter, exit, micro, emphasis, each with duration and easing) and per-section notes on what moves, in what order. Put it on the canvas where that is possible and in `motion-spec.md` in the run folder.

### 7. Finish

Before presenting: consistent spacing, meaningful layer or element names, colors that match the declared tokens, no placeholder text. On Figma, also run the frame checks in `references/figma.md`.

### 8. Hand off and close

Make a shareable HTML document with a skill that renders composed HTML pages (such as `ink`, if installed), saved as `output.html` in the run folder (this name wins over that skill's default) with the captures embedded so the file stands alone; if none is installed, write a plain self-contained HTML page. It holds: a hero capture, the three or four decisions that shaped the design (including which direction won and why), the screens, the motion summary, and what is next.

Then update the brief's `status`, write the pickup note (below), and report: where the design lives, scores, flagged items. If the run belongs to a project, add an entry to that project's own log with the design's location so its build work can find it.

## Outside critique

The builder is a poor judge of its own layout, so every critique round goes to a reviewer with no stake in the work.

- First choice: a different model. Use the installed second-opinion skill for the other vendor (`codex` when Claude is driving, `claude` when Codex is driving). Save the capture inside the folder the reviewer runs in and name it by path in the request; a second-opinion skill takes a text prompt and reads files itself. Give it the rendered HTML/SVG source instead if it cannot read images.
- Otherwise: a fresh sub-agent that gets only the capture, the Intent and Constraints, and the rubric, with none of the build conversation.
- If neither exists: critique it yourself, and say in the run log and the hand-off that the critique was not independent.

Ask the reviewer for problems and fixes, not approval. Record who reviewed each round.

## Rubric

Each capture is scored on six criteria, 0 or 1 each.

| # | Criterion | 0 (fail) | 1 (pass) | How to check |
|---|-----------|----------|----------|-------------|
| 1 | **Hierarchy** | Elements compete, no focal point | Clear primary > secondary > tertiary | Squint test at 50% zoom |
| 2 | **Spacing** | Irregular gaps, elements feel random | Consistent rhythm, gaps are multiples of 4px | Visual measurement |
| 3 | **Color system** | Off-brand colors, rogue values | All colors match declared token set | Compare to brief's color tokens |
| 4 | **Typography** | Mixed sizes without purpose | Clear type scale, mono on data, readable | Count distinct sizes (max 3-4 per section) |
| 5 | **Density** | Too sparse (wireframe) or too cramped | Professional density — information-rich, not cluttered | Does it look like a shipped product? |
| 6 | **Completeness** | Missing elements, placeholder text, dead ends | All scoped elements present with realistic content | Compare to section spec in brief |

- **5-6:** converged; stop iterating on this section.
- **3-4:** targeted fixes; run another round.
- **0-2:** structural rework; flag for the human before spending more.

The rubric does not judge whether it feels on-brand, whether a user would trust it, or animation timing. Flag those for the human.

Five habits account for most of the polish: one spacing scale (4/8/12/16/24/32/48/64), layered shadows over flat borders, at most three type sizes per section, at most two accent colors per screen, and generous vertical padding between sections.

## Gears

`--stretch` runs the same loop as one longer, wider turn : more sections or screens, fewer check-ins, and a hand-back at a fixed stop (all sections converged, or the budget ceiling). It goes wider, not lower: the diverge checkpoint, outside critique, and every budget floor still apply. It composes with `--autonomous`.

## Session handoff

Design runs are long, so the run folder is the state. Before ending a session with work in progress, add a pickup note at the bottom of `run-log.md`:

```markdown
## Pickup Note (YYYY-MM-DD)
**Last worked:** [section], round [N], score [N/6]
**Next:** [specific next action]
**Feedback from this session:** [direction, preferences, corrections]
**Open questions:** [anything unresolved]
**Canvas state:** [where the design lives; N screens complete]
```

To resume: read the brief, read the last pickup note, check the canvas matches it, continue.

## Design to build

`/design` does not hand off straight to code. Its artifacts (screens, tokens, motion spec) are referenced from project tasks; the build work pulls those tasks and consults the design as context. Design owns the visual lens; build owns requirements, architecture and testing.

## Safety

- Write only to a page or file this run created, and never delete objects it did not create, so a run cannot damage existing design work.
- Respect the run budget; on Figma that includes the daily call floor in `references/figma.md`.
- The diverge checkpoint and human checkpoints present a position and a specific question; `--autonomous` skips only the later checkpoints.

## Outputs

| Artifact | Path | Shape | Consumed by |
|----------|------|-------|-------------|
| Brief | `output/design/runs/[slug]/brief.md` | Frontmatter + Intent, Feel, Sections | `/design run` |
| Run log | `output/design/runs/[slug]/run-log.md` | Directions considered, round history, reviewer, scores, pickup note | `/design run` resume, human review |
| Captures | `output/design/runs/[slug]/screenshots/` | The directions, one image per section per round, and the final | Outside reviewer, hand-off doc |
| Design | Figma file and page, or `output/design/runs/[slug]/design.html` (plus `directions.html` for the diverge step) | Frames or sections per the brief | Human review, design-to-code work |
| Hand-off doc | `output/design/runs/[slug]/output.html` | Hero, decisions, screens, motion, next | Human, sharing |
| Figma call tracker | `output/design/rate-tracker.json` | `{ "date", "calls" }` | Figma runs only |

If these paths or shapes change, update this table.

## What to expect

The loop reliably produces clean, consistent, well-spaced layouts, and catches spacing errors, color drift, hierarchy problems and missing elements. It does not replace custom illustration, micro-typography, or the art direction of choosing what to show. Treat the result as a strong base a designer can finish in one focused session.
