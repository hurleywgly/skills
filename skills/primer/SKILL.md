---
name: primer
description: "Turn a significant technical announcement, release, or viral thread into a shareable primer: a research doc plus a single-file interactive HTML explainer built from parallel research and four analysis perspectives, optionally deployed to a public URL. Use when the user says \"make a primer\" or \"break this down\" about a launch. Not for quick summaries, social posts, or research with no artifact."
argument-hint: "<url(s) or pasted source> [angle or tone]"
---

# /primer

Take a significant technical announcement, thread, or release and turn it into a comprehensive, shareable educational artifact.

## When to Use This Skill

**Triggers when:**
- User shares a viral tech thread and wants to understand the implications
- User says "make a primer" or "break this down"
- A significant technical announcement drops that warrants deep analysis
- User wants to create a shareable educational artifact from a complex topic

**Do NOT trigger for:**
- Quick summaries (just summarize directly)
- Content creation for social
- Research without artifact creation

## Inputs

The user provides:
- **Source material** — URL(s) to the announcement, thread, repo, demos, articles
- **Screenshots** — optional, for visual context from tweets/threads
- **Tone/angle** — what aspect matters most to them

## Workflow

### Phase 1: Parallel Research (3 agents)

Launch 3 research agents simultaneously in a single message (if the host has no sub-agents, run the three passes yourself in sequence):

**Agent 1 — Source Material:**
- Fetch all URLs (project pages, demos, GitHub READMEs, shortened links)
- Extract: what it is, how it works, technical claims, API surface, demos
- Resolve t.co and other shortened URLs

**Agent 2 — Format Reference:**
- Read existing primers in `output/` for format and style patterns
- Extract: structure, design system, tone, how technical concepts are explained
- Note what worked well in previous primers

**Agent 3 — Person/Context:**
- Research the creator's background, credibility, track record
- Search for community reactions, notable developer responses
- Establish why this person's voice carries weight

### Phase 2: Multi-Perspective Analysis (4 agents)

Launch all 4 perspective agents in parallel in a single message:

**Synthesis** — Patterns, convergence, strategic signal:
- What broader trends does this sit at the intersection of?
- Why now? What made this possible/necessary?
- Second-order effects — if this succeeds, what else changes?
- Who should care beyond the obvious audience?

**Narrative** — Story, resonance, framing:
- What story is the creator telling? What's the emotional arc?
- Why is this resonating? (engagement signals, bookmark ratios)
- How should we frame this for a builder audience?
- Hook → tension → resolution structure for the primer

**Systems** — Architecture, integration, tradeoffs:
- How does this change the architecture of existing systems?
- Integration patterns with current tools/frameworks
- Scalability characteristics — where it excels vs breaks
- Tradeoffs table (You gain / You give up)

**Risk** — Risks, caveats, hype vs reality:
- Accuracy and reliability risks
- Adoption barriers and maintenance concerns
- Accessibility implications
- Gap between demo magic and production reality
- What caveats should the primer include so readers aren't misled?

### Phase 3: Design Direction

Before building, decide the visual approach based on the subject matter.

**The artifact IS the argument** — let the subject inform the design:

| Subject Matter | Design Direction |
|---------------|-----------------|
| Infrastructure / systems / agents | Dark-mode tech dashboard, expandable cards, pipeline visualizations |
| Typography / design / craft | Editorial, serif fonts, drop caps, pull quotes, warm palette |
| Data / analytics / research | Clean, data-forward, tables, charts, comparison grids |
| Developer tools / DX | Code-heavy, terminal aesthetic, copy-paste examples |
| Creative / generative / art | Bold, visual-first, large images, minimal text |

Ask the user if they have a preference, or choose based on subject.

### Phase 4: Artifact Creation (2 agents, parallel)

Launch 2 agents simultaneously:

**Agent 1 — Research Doc** (`output/[topic]-research.md`):
- Executive summary
- Creator background
- Technical deep-dive (architecture, API, demos)
- Full multi-perspective analysis (all 4 perspectives, unabridged)
- Sources table with URLs

**Agent 2 — Interactive Primer** (`output/[topic]-primer.html`):
- Single-file HTML, zero external dependencies
- Mobile responsive
- Design direction from Phase 3
- Sections structured around the narrative arc
- Tradeoffs table included
- Caveats included prominently (not buried)
- Patterns as structural backbone
- Subtle interactivity: scroll progress, fade-ins, hover states
- All external links open in new tab

### Phase 5: Deploy

Deploying publishes the primer at a public URL. Deploy when the user asked for a shareable link; otherwise finish Phase 4, show the local HTML, and ask before publishing. If the `vercel` CLI is missing or not logged in, skip this phase and hand over the HTML file with a note on how to deploy it.

```bash
mkdir -p /tmp/[topic]-primer
cp output/[topic]-primer.html /tmp/[topic]-primer/index.html
cd /tmp/[topic]-primer && vercel --yes --name [topic]-primer
cd /tmp/[topic]-primer && vercel --prod
```

Confirm the URL works: `curl -sI https://[topic]-primer.vercel.app`

### Phase 6: Share Artifacts (optional)

If requested:
- Create a portable knowledge summary: `output/[topic]-primer-summary.md`
- Draft X post: casual, builder-to-builder, link to deployed URL
- Draft as quote-tweet if the source was a tweet/thread

## Output Checklist

| Deliverable | Location |
|-------------|----------|
| Research doc | `output/[topic]-research.md` |
| HTML primer | `output/[topic]-primer.html` |
| Deployed URL | `https://[topic]-primer.vercel.app` |
| Knowledge summary (optional) | `output/[topic]-primer-summary.md` |
| Social draft (optional) | Presented in conversation |

## Quality Bar

- [ ] Research doc has all 4 perspectives
- [ ] Primer HTML opens cleanly in browser
- [ ] Mobile responsive (test at 375px width)
- [ ] All external links work and open in new tab
- [ ] Deployed URL returns 200
- [ ] Design direction matches subject matter
- [ ] Caveats are visible, not buried
- [ ] Narrative follows recognition → understanding → implication arc

Primer output is HTML-default for human review. When delivering via a chat or email channel that won't render raw HTML, also produce a PDF via Chrome `--print-to-pdf`.

