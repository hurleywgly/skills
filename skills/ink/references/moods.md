# Reference moods

Five more moods beyond the core five (`crisp`, `monograph`, `folio`, `modernist`, `arcade`). Read this when the user names one of these, or when none of the core five suits the content.

Each is a token set, not a template: paste its block as the last thing in the page's `<style>`, after the contents of `templates/base-styles.css` and after the pattern template's own styles, put the class on `<body>`, and follow its rules. The core five have full mood templates. These five were each rendered once on a one-pager (2026-11-26) and the blocks below include what that run had to add, but they are still young: look at the first render and tune contrast and spacing before delivering. If a rule here fights the content, the content wins.

Three things hold for all five:

- Pattern templates were built for `crisp` and put the accent color on several elements. Where a mood says to use the accent sparingly, recolor the rest to the text color yourself (stat values, markers, accent bars, badges).
- Dark moods (`terminal`, `blueprint`, `keynote`) need light tokens for print: in `@media print`, reset the color tokens to the `:root` values from `base-styles.css` and set `background: #fff`, keeping the mood's fonts. Write that rule on `body.mood-<name>` so it outranks the mood block.
- Small text at 4.5:1 contrast or better. The blocks are tuned for that in page content; re-check anything you change. Two template parts sit outside the tokens and need a look in every mood: text inside an accent-tinted badge (use the text color, not the accent), and the screen-only preview bar's hint text.
- Pattern templates do not all use `--font-display`. If a mood's display face is not showing, set it on the page's main heading yourself.

Font links are optional, as everywhere in Ink: each stack ends in system fonts.

## swiss

International Typographic Style: the mid-century Swiss poster and corporate-identity tradition (Müller-Brockmann, Helvetica-era signage). Objective, gridded, flush-left.

```css
.mood-swiss {
  --ink-accent: #E2001A;
  --ink-accent-light: rgba(226, 0, 26, 0.06);
  --ink-accent-medium: rgba(226, 0, 26, 0.14);
  --ink-dark: #111111;
  --ink-text: #111111;
  --ink-text-secondary: #333333;
  --ink-text-muted: #6B6B6B;
  --ink-surface: #F2F2F2;
  --ink-border: #111111;
  --ink-border-light: #D9D9D9;
  --font-primary: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  --font-display: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  --radius-card: 0px;
  --radius-button: 0px;
  --radius-control: 0px;
  --radius-small: 0px;
  --radius-pill: 0px;
  background: #FFFFFF;
}
```

- Everything flush left on a strict column grid; ragged right; no centered text.
- Hierarchy from size and weight only. One red element per view, used like a signal; red is for shapes, rules and headings, kept off body copy so it stays a signal. Badges are black outlines. Left-align anything the template centers.
- Large numerals and tight, bold headlines; generous white space as structure.
- Kills it: rounded cards, drop shadows, gradients, more than one accent, decorative icons.
- Suits: one-pagers, comparisons, infographics, pitch decks that want authority.

## terminal

Developer documentation and terminal interfaces: man pages, CLI output, code editors in a dark theme.

```css
.mood-terminal {
  --ink-accent: #7EE787;
  --ink-accent-light: rgba(126, 231, 135, 0.10);
  --ink-accent-medium: rgba(126, 231, 135, 0.20);
  --ink-text: #E6EDF3;
  --ink-text-secondary: #B1BAC4;
  --ink-text-muted: #8B949E;
  --ink-surface: #161B22;
  --ink-border: #30363D;
  --ink-border-light: #21262D;
  --ink-dark: #010409;
  --font-primary: 'JetBrains Mono', 'IBM Plex Mono', 'SF Mono', ui-monospace, Menlo, monospace;
  --font-display: 'JetBrains Mono', 'IBM Plex Mono', 'SF Mono', ui-monospace, Menlo, monospace;
  --radius-card: 4px;
  --radius-button: 4px;
  --radius-control: 4px;
  --radius-small: 3px;
  --radius-pill: 4px;
  --lh-body: 1.6;
  background: #0D1117;
  color: #E6EDF3;
}
```

- Monospace throughout; headings marked by weight and a prefix (`#`, `$`, `>`), not by a second typeface.
- Code blocks and tables carry the page. Keep prose lines to about 80 characters.
- One accent for commands and success states; use the semantic colors for warnings and errors only.
- Check every component for contrast on the dark background before delivering.
- Kills it: serif type, photos, soft pastel cards, long centered paragraphs.
- Suits: developer explainers, annotated code reviews, API and CLI one-pagers.

## blueprint

Architectural and engineering drawings: white line work on blueprint blue, labelled in capitals.

```css
.mood-blueprint {
  --ink-accent: #FFD166;
  --ink-accent-light: rgba(255, 209, 102, 0.10);
  --ink-accent-medium: rgba(255, 209, 102, 0.22);
  --ink-text: #EAF2FF;
  --ink-text-secondary: #C3D6F5;
  --ink-text-muted: #A9C1E6;
  --ink-surface: #17407A;
  --ink-border: #EAF2FF;
  --ink-border-light: #4A72AE;
  --ink-dark: #0B2A57;
  --font-primary: 'IBM Plex Sans', 'Helvetica Neue', Arial, sans-serif;
  --font-display: 'IBM Plex Mono', 'SF Mono', ui-monospace, Menlo, monospace;
  --radius-card: 0px;
  --radius-button: 0px;
  --radius-control: 0px;
  --radius-small: 0px;
  --radius-pill: 0px;
  background: #123466;
  color: #EAF2FF;
}
```

- Diagrams first: inline SVG with thin white strokes, dimension lines, and numbered callouts keyed to a legend.
- Labels in small capitals with wide letter-spacing; a title block in one corner (title, plus date and revision only when the source gives them; do not invent either).
- A faint grid behind the content (a CSS background of 1px lines) is the one texture allowed.
- Yellow is for the single thing the reader must not miss.
- Kills it: filled colorful cards, photos, thick strokes, more than one highlight color.
- Suits: architecture explainers, system diagrams, process infographics.

## keynote

The dark stage-presentation look: very large type on near-black, one idea per view, one bright accent.

```css
.mood-keynote {
  --ink-accent: #2997FF;
  --ink-accent-light: rgba(41, 151, 255, 0.12);
  --ink-accent-medium: rgba(41, 151, 255, 0.24);
  --ink-text: #F5F5F7;
  --ink-text-secondary: #C7C7CC;
  --ink-text-muted: #8E8E93;
  --ink-surface: #1C1C1E;
  --ink-border: #3A3A3C;
  --ink-border-light: #2C2C2E;
  --ink-dark: #000000;
  --font-primary: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Inter', 'Helvetica Neue', Arial, sans-serif;
  --font-display: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', 'Helvetica Neue', Arial, sans-serif;
  --radius-card: 18px;
  --radius-button: 999px;
  --radius-control: 12px;
  --radius-small: 10px;
  --text-body: clamp(12pt, 1.3vw + 0.2rem, 15pt);
  --text-callout: clamp(11pt, 1.2vw + 0.2rem, 13pt);
  --text-caption: clamp(10pt, 1vw + 0.1rem, 11.5pt);
  --text-annotation: clamp(9.5pt, 0.9vw + 0.1rem, 11pt);
  background: #000000;
  color: #F5F5F7;
}
```

- One idea per slide or section. A headline of a few words at display scale, at most one supporting line.
- Numbers shown huge, with a short label beneath. Charts reduced to the one comparison that matters.
- Lots of empty black. Center alignment is acceptable here and only here.
- Kills it: bullet lists longer than three items, dense tables, small text, several accent colors.
- Suits: pitch decks, launch one-pagers, headline-metric infographics.

## riso

Two-color risograph printing: zines, gig posters, small-press pamphlets. Fluorescent ink on warm paper, slightly imperfect.

```css
.mood-riso {
  --ink-accent: #FF48B0;
  --ink-accent-alt-1: #0078BF;
  --ink-accent-light: rgba(255, 72, 176, 0.14);
  --ink-accent-medium: rgba(255, 72, 176, 0.28);
  --ink-dark: #1D1D1B;
  --ink-text: #1D1D1B;
  --ink-text-secondary: #1D1D1B;
  --ink-text-muted: #5E5A4F;
  --ink-surface: #EFE6D2;
  --ink-border: #0078BF;
  --ink-border-light: #D9CDB2;
  --font-primary: 'Space Grotesk', 'Helvetica Neue', Arial, sans-serif;
  --font-display: 'Archivo Black', 'Arial Black', Impact, sans-serif;
  --radius-card: 0px;
  --radius-button: 0px;
  --radius-control: 0px;
  --radius-small: 0px;
  --radius-pill: 0px;
  background: #F6EEDC;
}
```

- Pink and blue are inks for shapes, fills, rules and large display type. Neither is dark enough for small text on this paper (pink is under 3:1, blue about 4:1), so running text and labels are black.
- Two inks only, pink and blue, plus the paper. A third color appears only where the two overlap (use `mix-blend-mode: multiply` on overlapping shapes).
- Big, blunt headlines; flat shapes; halftone dots or stripes as the only shading (CSS gradients repeated as patterns).
- Offset one layer by a pixel or two for misregistration; keep it subtle.
- Kills it: gradients, drop shadows, photos in full color, thin elegant type.
- Suits: playful infographics, event or launch one-pagers, explorations where energy matters more than polish.

## Choosing among all ten

| Content | Reach for |
|---|---|
| Business one-pager, decision brief | `crisp`, `swiss` |
| Long-form report or essay | `monograph`, `folio` |
| Pitch deck | `keynote`, `swiss`, `modernist` |
| Infographic | `swiss`, `riso`, `blueprint` |
| Technical or developer explainer | `terminal`, `blueprint`, `crisp` |
| Playful or retro piece | `arcade`, `riso` |

A user-named mood always wins over this table.
