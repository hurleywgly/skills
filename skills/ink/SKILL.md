---
name: ink
description: "Render a composed, self-contained HTML artifact instead of markdown: explorations, side-by-side comparisons, research explainers, annotated code review, specs, throwaway editors, briefs, reports, infographics. Use whenever layout, diagrams, or visual encoding would carry the content better than markdown (multi-pane comparisons, SVG diagrams, annotated diffs, variant grids, custom controls). Supplies a curated design system and five editorial moods. PDF and image generation are optional downstream steps. Not for production frontend code, slide files, or state files an agent reads."
argument-hint: "<what to render> [mood] [layout pattern]"
---

# /ink

HTML is Claude's most expressive medium. Markdown stops carrying you somewhere around 100 lines — tables thin out, diagrams become ASCII, diffs become text. HTML keeps going: SVG diagrams, side-by-side grids, color-coded annotations, sliders that export back to a prompt, custom editors purpose-built for one piece of data.

`/ink` is a design system + taste guide for those HTML artifacts. It doesn't lock you into rigid templates — you describe what you want, `/ink` picks a layout pattern and a mood (5 editorial styles), and renders self-contained HTML. Open in a browser. If you eventually need to share it somewhere that won't render HTML (Discord, email, S3-as-PDF), generate a PDF as a downstream step.

## When to use this skill

**Trigger when the artifact would benefit from layout, structure, or visual encoding markdown can't carry well:**

- **Explorations** — *"Generate 6 distinctly different approaches to X — vary layout, tone, density — lay them out in a single HTML file in a grid so I can compare."*
- **Comparisons** — side-by-side matrices for variants, vendors, design options, API surfaces, prompt versions.
- **Research / explainers** — long-form HTML with SVG diagrams, code snippets, callouts, sidenotes.
- **Code review / understanding** — render diffs with margin annotations, color-coded findings by severity, flowcharts of control flow.
- **Specs and planning** — decision context, options with tradeoffs, recommendation, open questions.
- **Throwaway editors** — single-file HTML tools purpose-built for one piece of data, with controls + live preview + a *copy as prompt / copy as JSON* button.
- **Briefs, reports, presentations, infographics** — finished artifacts when you need them. Five editorial moods.
- **Visual assets** — hero graphics, illustrations, banners (optional Gemini image generation).

**Do NOT trigger for:**

- Frontend components or production web pages (use `frontend-design`)
- Slide decks for Google Slides / PowerPoint (Ink outputs HTML, not `.pptx`)
- Social media posts (use platform-specific skills)
- State / transfer files: `context.md`, worklogs, changelogs, kanban / task files (`*-tasks.md`), `memory/*`, capsules, project packages, agent state manifests, plan files read mechanically by an agent, research briefs / personas. These are workspace source-of-truth; HTML diffs are noisy and the next reader is usually an agent, not a human.

## Step 0: HTML or plain text?

By default, render HTML. The exceptions are narrow:

- **Render HTML when** there's a layout pattern that helps (grid, comparison, annotated code, diagram-heavy explanation, custom editor), the artifact will be re-read or shared, or you'd otherwise reach for a table / ASCII diagram / multi-section structure to convey it.
- **Stay in plain chat / markdown** when the answer is a few sentences, a single number, or an update to a state file (worklog, kanban, memory, plan file).
- **When unclear, default HTML.** The cost is 2–4× longer to generate; the upside is the user actually reads it.

If the host workspace has its own output/delivery conventions (e.g. a `## Output & Delivery Conventions` section in its own CLAUDE.md), defer to that.

## Step 1: Pick the layout pattern

Read the user's intent. Most requests map to one of these patterns. The pattern is a starting structure — adapt freely. Templates live in `templates/[type]-template.html`.

| Pattern | Best for | Visual signature |
|---|---|---|
| **Exploration** | "Show me N distinct approaches" / "lay variants out in a grid" | 4–9 cards in a responsive grid, each with a label, a render or sketch, and a one-line tradeoff caption |
| **Comparison** | "Compare X vs Y vs Z" / "which is better at..." | Side-by-side columns or a matrix; rows are dimensions, columns are options |
| **Explainer** | "Explain how X works" / "research file on X" / "in-depth read" | Long-form layout with SVG diagrams, code blocks, sidenotes, pull quotes; chapter openers if 5+ sections |
| **Code review** | "Review this PR" / "annotate this diff" / "explain this module" | Diff layout with margin annotations, severity color-coding, flowcharts for control flow |
| **Editor** | "Build me a tool to [reorder / tag / configure] this" / "throwaway editor" | Controls (drag, sliders, dropdowns) + live preview + a *copy as prompt / copy as JSON* button |
| **Planning** | "Decision doc for X" / "options + recommendation" | Decision context → option cards (recommended one highlighted) → recommendation → open questions → next actions |
| **Brief** | "One-pager on X" / "executive summary" | Single-page, key-metric strip, recommendation seal |
| **Report** | "PRD" / "deep dive" / "multi-page write-up" | Cover, TOC, section numbering, named-page chapter openers, page numbers |
| **Presentation** | "Deck on X" / "slides for Y" | Slide-per-page HTML, viewport-locked composition |
| **Infographic** | "Dashboard of X" / "data presentation" | Stat callouts, metric cards, timeline elements |

**Image path** (keywords: image, illustration, hero, banner, icon): route to Gemini image generation (Step 5).

If the user just says "make a HTML file about X," skip the routing — pick the pattern that best fits the content and ship. Don't make them choose a type.

## Step 2: Gather metadata (documents)

Collect what's needed for the chosen pattern:

- **Title** (required)
- **Subtitle** (optional)
- **Author** (ask — no default)
- **Date** (default: today)
- **Mood** — choose the visual style:
  - `crisp` (default) — system fonts, blue accent, business-ready
  - `monograph` — luxury monograph: Cormorant Garamond, warm cream palette, generous white space
  - `folio` — encyclopedic reference: Playfair Display, crimson accent, two-column density
  - `modernist` — modernist/architectural: DM Serif Display italic, monochrome, disciplined grid
  - `arcade` — Pac-Man manual / 80s game journal: Press Start 2P + VT323, cream paper, arcade yellow + ghost colors

  Auto-select if context is clear: research / explainers → monograph or folio; executive briefs and exploration grids → crisp; architectural / design docs → modernist; playful / retro content → arcade. Otherwise default to crisp.

  **Project-derived moods (pattern):** Any project with its own `DESIGN.md` (Google [design.md spec](https://github.com/google/design.md)) can spawn a `mood-<project>` block — source the YAML frontmatter for tokens, write a single CSS block under the existing mood section in `base-styles.css`. Keep project moods scoped to the project repo, not in the public skill set.

- **Image strategy** (ask before generating):
  - `none` — text + color blocks only. Lean on typography, accent color, CSS-drawn rules. Default if unclear.
  - `placeholders` — SVG data-URI placeholders sized to layout slots. Free, anchors hero/figure spots.
  - `generated` — real generated imagery via Gemini Nano Banana (~$0.04) or OpenAI gpt-image-2 (~$0.006–$0.21 depending on quality). Use when the doc actually benefits from photographic or illustrated heroes (monograph plate spreads, folio plate figures, infographics). Routes to Step 5; user can name the provider or Ink picks based on which API key is configured.
  When in doubt: "Should I generate hero images (Gemini ~$0.04 or OpenAI gpt-image-2 ~$0.04–$0.21), use SVG placeholders, or skip imagery?"

- **Pattern-specific options:**
  - Exploration: How many variants? (default: 6); what dimensions vary? (layout / tone / density / etc.)
  - Comparison: What dimensions are rows? What options are columns?
  - Explainer: Diagram-heavy or text-heavy? Include code snippets?
  - Code review: Just the diff, or diff + annotated control flow?
  - Editor: What's the data shape? What does *copy* output (prompt text? JSON? markdown table?)
  - Planning: Number of options? Recommendation section? (default: 2–4 options, yes)
  - Report: Include table of contents? (default: yes)
  - Brief: Recommendation section? (default: yes)
  - Infographic: Number of metric highlights? (default: auto-detect)
  - Presentation: Slide count? (default: auto from content)

If the user provides content (file path, pasted text, description, codebase ref), gather it now.

## Step 3: Generate HTML

Paths such as `templates/`, `references/`, and `bin/` are relative to this skill's own folder (the directory holding this SKILL.md), not the user's working directory.

1. Read `templates/base-styles.css` for the Ink design system
2. Read `templates/[type]-template.html` for the HTML structure pattern (or the mood template if non-crisp)
3. **3a. Resolve mood → font pair:**
   - `monograph` → display: Cormorant Garamond, body: EB Garamond
   - `folio` → display: Playfair Display, body: Libre Baskerville
   - `modernist` → display: DM Serif Display, body: Lora
   - `arcade` → display: Press Start 2P, body: VT323
   - `crisp` → system fonts (no Google Fonts needed)
4. **3b. For non-crisp moods, add Google Fonts `<link>` tag** (CDN default) in `<head>` before the `<style>` block:
   - monograph: `https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=EB+Garamond:ital,wght@0,400;0,500;1,400&display=swap`
   - folio: `https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap`
   - modernist: `https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Lora:ital,wght@0,400;0,600;1,400&display=swap`
   - arcade: `https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap`
   Add `<link rel="preconnect" href="https://fonts.googleapis.com">` and `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>` first.
5. **3c. Apply mood class:** Add the mood class (e.g. `class="mood-monograph"`) to `<body>` or the outer wrapper.
6. Transform content into HTML matching the pattern. For *editor* pattern only, JS is allowed and expected (controls, drag, copy-to-clipboard).
7. Embed all CSS in a `<style>` block (self-contained, no external dependencies other than optional Google Fonts).
8. Replace template placeholders with actual content.
9. Resolve output dir: `mkdir -p ./output/`
10. Save to `./output/[slug].html` (kebab-case title; append date if file exists). **Never save inside the skill folder itself** — that's the recipe, not the meal. The `./output/` path is relative to the directory you invoked `/ink` from; if your workspace has a fixed output convention, override at invocation time.

## Step 4: Open in browser

```bash
# Cross-platform open
case "$(uname -s)" in
  Darwin*) open "./output/[slug].html" ;;
  Linux*)  xdg-open "./output/[slug].html" ;;
  MINGW*|MSYS*|CYGWIN*) start "./output/[slug].html" ;;
esac
```

Confirm:

```
Created ./output/[slug].html — opening in browser.
Pattern: [exploration / comparison / explainer / code-review / editor / planning / brief / report / presentation / infographic]
Mood:    [crisp / monograph / folio / modernist / arcade]

To iterate: tell me what to change.
To share: I can generate a PDF (printable) or you can upload the HTML file (e.g. to S3 / Vercel) for a shareable link.
```

## Step 4b: PDF (optional — only when the user needs to share through HTML-hostile surfaces)

HTML is the primary surface. Generate a PDF only when:
- The user explicitly asks
- The destination is Discord, Slack, email body, or anywhere HTML files don't preview inline
- The artifact will be archived/printed

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="./output/[slug].pdf" \
  "./output/[slug].html"
```

(On Linux, swap for `chromium --headless ...` or `google-chrome-stable --headless ...`.) Don't auto-PDF every doc — it's not the default.

## Step 5: Generate Image (optional)

Only when the user asks for a generated image (hero graphic, illustration, banner). Two providers are supported, Gemini (`gemini-2.5-flash-image`) and OpenAI (`gpt-image-2`); both are bring-your-own-key, cost money per image, and write a PNG to `./output/[slug].png`.

Before generating, read [references/image-generation.md](references/image-generation.md) for provider routing, first-run key setup, the exact commands, prompt enhancement, and the confirmation format. Do not generate images from memory of that file.

## Design Principles

These guide every artifact, regardless of pattern:

1. **Generous whitespace.** More spacing than feels necessary. Let content breathe.
2. **Accent bar as punctuation.** The solid accent bar appears in 1–2 places: title accent, section divider. Never as background fill.
3. **Typography hierarchy with intent.** Title 0 (display-size) only on covers. Title 2 for section headers. Body for running text. The scale should feel like a well-set book.
4. **Dark-on-light with mood accents.** Near-black text on white (or warm-white for editorial moods). Accent color for links, callout borders, key metric numbers.
5. **Card-based data layouts.** Stats, metrics, takeaways use radius-card with subtle shadows (crisp) or flat rule-bounded panels (editorial moods).
6. **Subtle details.** 1px light borders. Surface-color table headers. Left-border pull quotes.
7. **Editorial typography over default web type.** For non-crisp moods, load Google Fonts via CDN `<link>`. Apply `.body-editorial` OpenType features (ligatures, oldstyle numerals, kerning, hanging punctuation) to body text. Use `.drop-cap` on chapter openers. Use `.section-label` (small caps) instead of `.annotation` for section labels.
8. **Rhythm through section alternation.** Vary layout across sections: full-bleed image → text block → stat cards → pull quote. Uniform single-column feels assembled; alternation feels composed.
9. **Sidenotes over footnotes.** For research-heavy or annotated documents (especially monograph/folio moods), use `.body-with-margin` + `.sidenote` rather than inline parenthetical text.

## Print rules (when a user wants a clean PDF)

- **Never force page breaks between sections** unless content is clearly a full page. Use `margin-top` for separation.
- **Only force breaks on:** cover pages, major part dividers (10+ page reports), slides in presentations.
- **Prevent orphaned headings:** Add `page-break-after: avoid` to section labels, titles, intro text, accent bars.
- **Anchor footers** inside last content container — standalone footers orphan.
- **Let large tables break across pages:** `page-break-inside: avoid` on `tr`, not `table`. Repeat headers with `display: table-header-group` on `thead`.

## Configuration

The design system is fully customizable via CSS variables in `templates/base-styles.css`:

| Variable | What it does | Default |
|----------|-------------|---------|
| `--ink-accent` | Theme color (one change re-themes everything) | `#2563EB` |
| `--brand-name` | Text in footers/headers | `"Document"` |
| `--brand-show` | Show/hide brand text (`block` / `none`) | `block` |
| `--font-primary` | Main font stack | System fonts |
| `--font-mono` | Code font stack | System mono fonts |

## Design System Quick Reference

### Colors
| Token | Hex | Usage |
|-------|-----|-------|
| Accent | `#2563EB` | CTAs, accents, metric numbers |
| Text | `#1A1A1A` | Primary text |
| Text Secondary | `#4A5568` | Secondary text |
| Surface | `#F7F8FA` | Card/table backgrounds |
| Border | `#E2E8F0` | Primary borders |
| Success | `#38A169` | Positive metrics |
| Error | `#E53E3E` | Alerts, negative metrics |
| Warning | `#D69E2E` | Cautions |

### Typography
**Moods:** `crisp` (system fonts, default) | `monograph` (Cormorant Garamond + EB Garamond) | `folio` (Playfair Display + Libre Baskerville) | `modernist` (DM Serif Display + Lora) | `arcade` (Press Start 2P + VT323)
**Image strategy:** `none` (text + color blocks, default) | `placeholders` (SVG data-URI blocks) | `generated` via Gemini Nano Banana (~$0.04) OR OpenAI gpt-image-2 (~$0.006–$0.21 by quality tier) — Step 5
**Fluid scale (clamp):** display / title-0 / title-1 / title-2 / title-3 / title-4 / headline / body / callout / subhead / caption / annotation — all scale with viewport, floor at print-safe pt sizes.

### Spacing (8px grid)
4 / 8 / 12 / 16 / 24 / 32 / 36 / 48 / 56

### Radius
Cards: 20px | Buttons: 12px | Controls: 8px | Small: 6px

## Template Architecture

- **`templates/base-styles.css`** — Shared CSS: color palette, typography, spacing, components, print rules
- **`templates/[type]-template.html`** — HTML skeleton with `{{PLACEHOLDERS}}`. Follow the structure; don't use literally.

## Output

Documents: `./output/[filename].html`
PDFs (optional, when explicitly needed): `./output/[filename].pdf`
Images: `./output/[filename].png`

**Convention:** All `/ink` artifacts live in `./output/` — relative to the directory you invoked the skill from. Never write outputs inside the skill folder itself; that's the skill code, not its products. If your workspace prefers a fixed location, override the output path at invocation time.

## Contracts (locked)

Properties of `/ink` that are not negotiable per-doc. They constrain what the skill is and isn't.

1. **No JS dependencies for static patterns.** Reports, briefs, planning, exploration grids, comparisons, explainers, code reviews, presentations, and infographics output HTML + CSS + optional Google Fonts only. No animation libraries (GSAP, Anime.js, Motion One, Three.js). Motion is CSS-only (`@keyframes`, `view-timeline`, scroll-driven animations).
2. **The *editor* pattern is the exception.** Throwaway editor outputs may include vanilla JS (no frameworks) for controls, drag/drop, and copy-to-clipboard. They live and die in the browser; print isn't a concern for editors.
3. **Mood library is curated, not catalog.** Adding a 6th general-purpose mood requires: (a) a content category not served by the existing 5, (b) all selectors scoped under `.mood-<name>`, (c) a single CSS block in `base-styles.css`, (d) at least one live test doc. Project-derived moods (`mood-<project>` from a project's own `DESIGN.md`) sit alongside but don't count against the cap.
4. **HTML is the primary surface.** PDF is downstream — generate it when the user needs to share through an HTML-hostile channel, not by default.

## Limitations

- Two-way interactivity is editor-pattern only. Static patterns stay static.
- Very long explainers (30+ pages of equivalent print) may have minor pagination inconsistencies if printed.
- Images must be base64-encoded to stay self-contained.
- Image generation requires an API key for one of the supported providers (Google Gemini ~$0.04/image, or OpenAI gpt-image-2 ~$0.006–$0.21/image depending on quality tier).
- Either provider may refuse certain prompts per its own content policy.

### When to skip /ink

Markdown is the right format — `/ink` is the wrong tool — when:

- The doc is a state file, append target, or kanban (e.g. `context.md`, worklog files, `*-tasks.md`, `memory/*`, `CHANGELOG.md`)
- The doc is agent-to-agent transfer (capsules, project packages, agent state manifests)
- The doc is a plan file read mechanically by an agent — HTML diff noise hurts
- Edits will be small/textual and reviewed in git (HTML diffs are noisy)
- The answer is a few sentences or a single number — chat is fine
- The next reader is an agent, not a human
