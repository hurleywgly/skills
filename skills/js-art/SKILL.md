---
name: js-art
description: Draw an original still artwork entirely in JavaScript on a canvas, made to look hand-made with physical media (riso, gouache, woodblock, watercolor, pencil and more), sized for a wall TV or print. Workshops a direction from a researched library of art lineages, pitches several concepts as a gallery, then renders the pick at 4K. Use when the user says "/js-art", "draw me art in JavaScript", "make art for my Frame TV", "prompt art", or pastes a code-art prompt they want to try.
argument-hint: "[look, mood, or pasted prompt] [where it will hang]"
---

# /js-art

Make one piece of wall art with code. No image models: the picture is drawn by a script, on a canvas, and has to look like a person made it with real materials.

The method comes from a prompt style that gives the model a feeling and forbids drawing anything literal from it. This skill adds three things: a library of directions to choose from, a pitch-then-pick flow so the user reacts to pictures and not descriptions, and a print engine that already knows how to look hand-made.

## What you have

| File | Use |
|---|---|
| `references/directions.md` | 16 art lineages with composition rules, palettes and "what kills it", plus presets and mixing rules |
| `references/media.md` | The print engine's profiles and rules, 14 recipes for other media, universal hand-made rules, 4K performance |
| `references/briefs.md` | Seven ways to brief a piece, how to write vignettes, the translation step, and the prompt template |
| `assets/engine.js` | Layered-ink print engine (1600×900 design space, any render scale) |
| `assets/gallery-template.html` | Pitch gallery: N concepts side by side with notes and recommendations |
| `assets/final-template.html` | One piece, full bleed, 3840×2160, with Save PNG |
| `scripts/build.py` | Inlines engine and pieces into one self-contained HTML file |
| `examples/` | A complete gallery (eight prints; a normal round is six) and a single final piece to copy from |

Read `directions.md` and `briefs.md` before the first question. Read `media.md` and one example before writing code.

## Flow

Keep it playful and fast. Ask one or two questions at a time. Skip any question the user has already answered.

### 1. Find the direction

A direction is four dials: **lineage**, **medium**, **palette**, **brief**. Settle them in conversation.

- **If the user pasted a prompt or post:** first say plainly what makes it work (its constraints, aesthetic, technique and output format). Then ask what they want to change.
- **If they described a look:** map it to the nearest lineage or two, say which grammar you are borrowing, and confirm.
- **If they are open:** offer three or four presets from `directions.md` that suit the room or mood, plus "describe your own" and "surprise me".

Then ask what you still need:

- Where it will hang and at what size. Default is a 16:9 still at 3840×2160.
- Subject or mood, via a brief style from `briefs.md`. Offer to draft vignettes for them to react to.
- Palette: the lineage's, their own, or a color-first brief.
- Anything they want kept or banned.

Say the four dials back in a few lines before drawing.

### 2. Pitch a gallery

Users react to pictures far better than to descriptions. Draw the options.

1. Write the five-line translation from `briefs.md` for the brief.
2. Design **six concepts, each built on a different compositional idea**. Six palette swaps of one layout is a failed round. Name each idea in a few words (strata, nested fields, cropped circles, pattern over a landform).
3. Write one pieces file defining `INKS`, `META` and `PIECES`. Copy the shape from `examples/winter-big-shapes.pieces.js`.
4. Build and open it:
   ```
   python3 <skill>/scripts/build.py gallery <slug>.pieces.js <out>/<slug>/gallery.html
   ```
5. Open the file in the host's browser. Wait for `document.body.dataset.done`, check the console for errors, and look at every print. A print that failed shows "misprint" with the error.
6. **Critique before showing.** Run the checklist below on each print and fix what fails. The first render is a draft; the user should see the second.
7. Show the gallery. Give your honest ranking: which to pursue, which are weaker and why.

### 3. Iterate

Take the reaction and draw again. A new round is a new file (`round-2.html`) so earlier rounds stay viewable.

- "Too literal" or "too on the nose": remove objects, keep the weather and light, go bigger and more abstract.
- "More like that one": keep its compositional idea and vary scale, cropping and palette weight.
- If they like parts of two, combine them and say which part came from where.

### 4. Render the final

1. Move the chosen piece into its own file defining `INKS` and `PIECE`. Push the detail further than the sketch: more interior texture, a tighter value plan, a second look at every edge.
2. Build it:
   ```
   python3 <skill>/scripts/build.py final <name>.piece.js <out>/<slug>/<name>.html
   ```
3. Open it in the host's browser. It renders at 3840×2160; add `?scale=1` for a quick preview. Check the console, then look at the whole image and at a 100% crop of the busiest area.
4. Save the filled-in prompt template as `prompt.md` beside the art. Keep prompt and code in sync through every later change.
5. Tell the user how to get the PNG (the Save PNG button) and how to put it on the display.

### 5. Share, only if asked

Offer once to share the final the way the host supports (for example as a private artifact). Share only on an explicit yes. The user controls sharing.

## Critique checklist

Look at the rendered picture, not the code. Fix anything that fails before the user sees it.

1. **Three-second read.** From across a room, is there one clear idea? If it needs explaining, simplify.
2. **Big shapes.** 3–9 large shapes carry the picture, and at least one is cropped by the frame. Many small elements means start over.
3. **Off-center.** The focal point and the warm spark sit off the middle. Symmetry needs a reason.
4. **Value plan.** There is a clear lightest area, a clear darkest area, and a middle. Squint at the screenshot.
5. **Clean color.** No muddy brown where warm ink crossed cool. Warm shapes need a knockout beneath them.
6. **No bare flats.** Every large area carries some interior work: grain, hatching, halftone, brush drag.
7. **Nothing reads as a default.** No centered gradient, no purple-to-blue, no stock noise swirl, no perfect circles or ruler lines.
8. **Honors the brief.** Nothing forbidden appears. Watch for accidents: two dots and a line become a face; drips under a circle become a figure.
9. **Honors the lineage.** Check its "kills it" list.
10. **One medium.** A single substrate and a single ink behavior. Mixed tells look fake.

## Engine quick reference

Design space is 1600×900. Print order is first-use order, so start with light inks.

```js
const INKS={navy:'#22305c',sky:'#9cc3d6',coral:'#e36a50'};
function piece(p){
  let x=p.ink('sky');                 // get a layer's 2D context, ready to fill or stroke
  x.globalAlpha=.6; x.fillRect(0,0,W,H);
  x=p.ink('navy'); p.wcirc(x,500,450,300); x.fill();   // wobbled circle path, then fill
  p.all(x=>{p.wcirc(x,900,300,120); x.fill()});        // knock a hole through every layer so far
  x=p.ink('coral'); p.wcirc(x,900,300,112); x.fill();  // warm ink on clean paper
  p.hatch('navy',[200,150,600,600],Math.PI/4,10,.3);   // knocked-out cross-hatching
}
const PIECE={fn:piece,seed:7,name:'Example',media:MEDIA.riso};
```

| Call | Does |
|---|---|
| `p.ink(name)` / `p.knock(name)` | Layer context for adding ink / for cutting it away |
| `p.all(fn)` | Run a knockout on every layer created so far |
| `p.wpath(x,pts,jitter,closed)` `p.wcirc` `p.lob` `p.star` `p.boomer` | Hand-wobbled paths. Caller fills or strokes. |
| `p.strokes(x,clip,opts)` | Brush strokes; on a knock context this is dry-brush |
| `p.dots(x,box,step,fn)` | Halftone field; `fn(x,y)` returns dot size 0–1 |
| `p.hatch(ink,box,angle,gap,alpha)` | Parallel knocked-out lines |
| `p.contours(ink,f,n,gap)` | Lines echoing the curve `y=f(x)` |
| `p.r(a,b)` | Seeded random. Never use `Math.random`. |
| `curve(f,x0,x1)` `rot(pt,center,angle)` `makeNoise(seed)` | Helpers |
| `MEDIA.riso` `.screen` `.gouache` `.cutpaper` `.woodblock` | Print profiles |

For a medium outside the print family (watercolor, pencil, pastel, ink), follow its recipe in `media.md`. You can still draw onto the engine's layers and let `finish()` supply paper and grain, or write a standalone file that keeps the same contract: one self-contained HTML file, a Save PNG button, and `document.body.dataset.done` set when rendering ends.

## Rules

- **Code only.** No image models, no traced or embedded images.
- **One self-contained HTML file per deliverable.** Vanilla JS and Canvas 2D by default. If a library is truly needed, load a pinned version from cdnjs or jsdelivr, and say so.
- **Seeded randomness**, so a piece re-renders identically.
- **Original work.** Borrow a lineage's grammar; never reproduce a specific artwork. Don't offer the lineages listed under "Left out on purpose" in `directions.md`.
- **No people** unless the user asks for figures.
- **Animated pieces must respect `prefers-reduced-motion`.** The default is a still.
- **Output goes to the workspace's output directory** (default `./output/js-art/<slug>/`), never inside this skill's folder.
- **Never publish or post without an explicit yes.**
- **Render and check in whatever browser the host provides** (in the Claude desktop app, the browser pane). Start a headless browser only when there is no other, since a visible one lets the user watch the piece appear.

## After a good run

If the user liked a direction that is not in `directions.md`, offer to add it as a lineage block or a preset. If a [D] recipe in `media.md` worked or needed changes, update it and mark what was tested. The library should get better each time it is used.
