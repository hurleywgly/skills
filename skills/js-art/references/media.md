# Media: how the surface is made

The medium dial decides how ink or paint behaves. Two kinds of medium are covered here.

- **Print family.** Handled by the bundled engine (`assets/engine.js`). Pick a profile and draw.
- **Everything else.** No bundled code. Each block below is a recipe to implement for the piece.

**Trust levels.** The riso profile is proven on real pieces. The other four engine profiles are parameter variations of it: check the first render and tune. In the recipes, **[S]** means the step comes from the linked source and **[D]** means it was derived in canvas terms during research and has not been run. Treat every [D] step as a starting point to test.

## Universal hand-made rules

1. Paper first. Texture and tint exist before any mark, and every mark interacts with them.
2. No perfect line, circle or closed loop. Overshoot, restate, leave gaps.
3. Alpha varies inside every stroke and fill.
4. Texture gates where pigment lands. It is not a filter laid on top.
5. Edges carry information: pooled in wet media, ragged in dry, lit and shadowed in paper.
6. Build areas from strokes or layers, not single fills.
7. 3–8 pigments. Other colors come from overlap.
8. Imperfect registration between layers, 1–3 px at 1600 wide.
9. Vary edge character within one shape: sharp on one side, soft on the other.
10. Hand error is Gaussian, not uniform. Damp jitter on long strokes.
11. Tool physics: the load runs out, pressure ramps in and out, starts and ends blob.
12. One light direction and one grain direction per piece.
13. Leave unpainted paper.
14. Seeded PRNG everywhere, never `Math.random`.
15. Noise perturbs; it does not compose. Stock Perlin swirls as visible structure look generic.
16. Finish with one unifying pass (grain, slight vignette).

## Print family (bundled engine)

Each ink is its own layer. White is paper left alone: `knock()` cuts ink away. `finish()` warps each layer's edges, grains it, and multiplies it onto paper with a small offset.

| Profile | Look | Notes |
|---|---|---|
| `MEDIA.riso` | Ragged edges, heavy grain, speckle, visible misregistration | Proven. The house look. |
| `MEDIA.screen` | Cleaner edges, flatter ink, small registration gaps | For WPA posters, Scandinavian textile, Concrete art |
| `MEDIA.gouache` | Blotchy coverage, soft wobble, almost no misregistration | Add `strokes()` on a `knock()` layer for brush drag |
| `MEDIA.cutpaper` | Crisp faceted edges, flat color, strong paper fibre | Engine has no drop shadows; see recipe 11 to add them |
| `MEDIA.woodblock` | Grainy flats, mottled baren pressure | Add grain with `hatch()` and bokashi per recipe 9 |

Print-family rules learned the hard way:

- **Warm over cool turns brown.** Multiply darkens. Knock the cool layers out under any gold, coral or blush shape first (`p.all(...)`), then print the warm ink.
- **Tonal steps from one ink.** Draw the same ink again at a different alpha on its own layer to get two or three values without a new color.
- **Knock through everything for unifying marks.** Cracks, a horizon line or reflection bars cut through all layers at once tie a picture together.
- **Interior texture is what separates a print from a vector.** Every large flat should carry something: halftone `dots()`, `hatch()`, `contours()`, or dry-brush `strokes()` on a knock layer.
- **Order matters.** Layers print in first-use order. Start light, end dark.

## Recipes for other media

### 1. Watercolor
- **Tells:** feathered edges beside crisp ones; darker pigment ring at the edge; granulation; overlaps glaze.
- **How [S, Hobbs and Sighack]:** deform a polygon recursively (move each edge midpoint by a Gaussian offset, split, reduce variance each level). About 7 rounds makes a base shape. For each of 30–100 layers, deform the base 4–5 more rounds and fill at about 4% alpha. Mask each layer with around 1000 small random circles so opacity varies.
- **Edges:** give each edge its own variance. Low is sharp, high fades.
- **Layering:** interleave colors in blocks of 5 layers per blob, not blob by blob [S]. Multiply so glazes darken [D]. One extra pass stroking the base outline at 6–10% gives the pigment ring [D].
- **Looks digital when:** fuzz is uniform all round. Keep some hard edges.
- **Sources:** https://tylerxhobbs.com/essays/2017/a-generative-approach-to-simulating-watercolor-paints · https://sighack.com/post/generative-watercolor-in-processing

### 2. Ink wash
- **Tells:** stroke starts loaded and runs dry; split-bristle streaks; wet halo; few values of one black.
- **How [D]:** 20–60 bristles offset across the stroke width, each a polyline at alpha 0.05–0.3 with width from a pressure curve. Give each bristle an ink reserve; when low, gate it with 1-D noise so gaps appear. Washes are recipe 1 in grey, 20–40 layers.
- **Layering:** light washes first, darkest dry strokes last, multiply. Three dilutions only.
- **Looks digital when:** width and alpha are constant.
- **Sources:** https://ileivoivm.github.io/inkField/tech/en/index.html · https://inconvergent.net/generative/

### 3. Graphite and hatching
- **Tells:** lines overshoot and are restated; tone from density; paper tooth breaks each line.
- **How [S, Rough.js]:** offset each endpoint randomly, bow the line with two control points near 50% and 75%, and draw it twice. Hachure fill: rotate the shape by the hatch angle, scanline at the gap, rotate back. Probabilistic hatching [S, Wilke]: scatter short segments with normally distributed length inside the shape, angle held to a band.
- **Tooth [D]:** after drawing, `destination-out` a tiled paper-grain pattern at 20–40%.
- **Layering:** 2–4 hatch passes at different angles, alpha 0.15–0.35, multiply. Let hatches overrun the outline by 2–6 px.
- **Looks digital when:** lines are evenly spaced. Jitter gap ±20%, angle ±3°, and alpha per line.
- **Sources:** https://shihn.ca/posts/2020/roughjs-algorithms/ · https://clauswilke.com/art/post/probabilistic-hatching

### 4. Colored pencil [D]
- As recipe 3 with 3–5 hue layers per region, each a hatch field at its own angle, alpha 0.12–0.25, multiply. Offset the tooth pattern per layer so later colors land in different valleys. A low-alpha flat fill only in the darkest areas acts as a burnish.
- **Looks digital when:** a pre-mixed flat color sits under the hatching. Let color come only from overlap.

### 5. Wax crayon and oil pastel
- **Tells:** wax sits on paper peaks and skips valleys; thick build-up; visible stroke direction.
- **How [D, after Rudolf, Mould and Neufeld]:** precompute a paper height map as tiled noise. Draw fat (20–60 px) scribble strokes at alpha 0.5–0.9, then mask the layer with a contrast-stretched grain pattern (`destination-in`). A second, heavier pass fills more valleys.
- **Layering:** `source-over`, since wax is semi-opaque.
- **Looks digital when:** grain is an overlay on a flat fill. Grain must gate the deposit.
- **Sources:** https://people.scs.carleton.ca/~mould/papers/crayon-cgf.pdf · https://github.com/acamposuribe/p5.brush

### 6. Charcoal, and chalk on a dark board
- **Tells:** dusty broken stroke; smudge haze; erased ghosts.
- **How [D]:** stamp a noisy disc sprite along the path every 0.3 × width at alpha 0.05–0.2 with random rotation. For smudge, draw the layer onto itself at 1/8 scale and back at alpha 0.15–0.3, then redraw the crisp marks. A blackboard gets large low-alpha eraser swipes before any chalk.
- **Looks digital when:** chalk is pure white at full alpha. Use off-white at 0.6–0.85 with streak noise.
- **Sources:** https://gist.github.com/saltcod/1299777

### 7. Marker [D]
- Build every area from parallel wide strokes (30–80 px, alpha 0.55–0.75, multiply) overlapping 10–20% so bands show. Add a dab at each stroke end. Never one polygon fill.
- **Source for the model:** https://github.com/acamposuribe/p5.brush

### 8. Pen and ink
- **Tells:** uniform line width; tone only from density; pen-down blobs; curves that never cross.
- **How [S, Hobbs]:** a flow field on a grid about 0.5% of width, extended past the canvas; step 0.1–0.5% of width; stop a curve when it nears another. Quantized angles give a faceted look. Add a 1.5× dot at each pen-down and a rare short gap [D].
- **Looks generic when:** the field is plain Perlin. Design it with obstacles or stepped angles.
- **Source:** https://tylerxhobbs.com/words/flow-fields

### 9. Woodblock additions (on the print engine)
- **Grain:** value = sin(r·f + noise·k) with a stretched high-frequency term, used as a 5–15% knockout on each color layer. `hatch()` with a small gap and low alpha is the quick version.
- **Bokashi [D]:** a linear alpha gradient on the layer over a short band only, with the fade line perturbed by 1-D noise so it wobbles. Grain still applies inside the gradient.
- **Key block:** a dark line layer printed last.
- **Looks digital when:** the gradient is smooth and full height.
- **Sources:** https://en.wikipedia.org/wiki/Bokashi_(printing) · https://barenforum.org/encyclopedia/entries/012_03/012_03.html

### 10. Linocut
- **Tells:** two tones; tone from carved line width; stray uncut ridges in cleared areas; salty ink solid.
- **How [D]:** fill the ink layer solid, then knock out tapered gouge strokes (3–12 px) following a direction field, denser in light areas. Leave random short ridges in cleared zones. Speckle the solid 1–3%.
- **Looks digital when:** white areas are clean.
- **Sources:** https://www.clicktorelease.com/code/codevember-2016/22 · https://www.scitepress.org/Papers/2019/73859/73859.pdf

### 11. Cut paper with depth [D]
- Per sheet, back to front: draw a soft offset shadow first (blur 8–30 px, offset 4–14 px, alpha 0.25–0.35, one light direction), fill the shape, add a 1 px lighter stroke on the lit edge, and lay a per-sheet grain at a random offset. Polygonize curves into 6–20 px chords with small angle jitter.
- At 4K, render shadows at quarter scale and upscale.
- **Looks digital when:** every sheet has the same shadow and texture phase.

### 12. Cyanotype [D]
- Brush the emulsion area in deep blue onto cream with dry-brush strokes (ragged border). Knock out the subjects. Blur some subject edges by downscaling and upscaling the mask, to mimic poor contact. Drift blue density ±15% with low-frequency noise. One layer, multiply.
- **Looks digital when:** the blue is a flat rectangle.
- **Source (process):** https://en.wikipedia.org/wiki/Cyanotype

### 13. Stitch and weave
- **How [D]:** each stitch is 2–3 parallel strokes (dark, mid, highlight) with round caps and endpoint jitter of 3–8% of the cell. For plain weave, alternate short horizontal and vertical segments with a gradient across each. Pre-render one stitch sprite per color at 4K.
- **Looks digital when:** stitches are identical.
- **Sources:** https://codepen.io/bajuba/pen/OJKdMeo · https://github.com/ArtPoon/pixelcraft

### 14. Mosaic
- **How [S, Hausner; D for canvas]:** seed tile centers along offset curves of the main shapes, relax with 5–15 Lloyd iterations, inset each cell 2–4 px for uniform grout, jitter vertices, vary tile lightness ±6%.
- **Looks digital when:** it is a random Voronoi with no flow.
- **Sources:** https://www.dgp.toronto.edu/~rinat/papers/mosaicSBIM2014.pdf · https://observablehq.com/@esperanc/simple-adaptive-mosaic-effects

## Which medium suits which composition

| Composition | Best media | Avoid |
|---|---|---|
| Flat shapes, bold silhouettes | Print family, linocut, marker | Watercolor |
| Atmospheric landscape | Woodblock with bokashi, watercolor, ink wash | Mosaic, stitch |
| Botanical or specimen | Cyanotype, linocut, colored pencil | Marker |
| Abstract line work | Pen and ink, graphite | Cut paper |
| Naive and playful | Crayon, marker, chalkboard | Linocut |
| Pattern and repeat | Stitch, mosaic, linocut, woodblock | Charcoal |
| Night and drama | Linocut, ink wash, chalk on dark | Colored pencil |
| Layered depth | Cut paper with shadows, woodblock | Cyanotype |

Hybrids worth trying [D]: woodblock key-line over watercolor washes; crayon marks on cut-paper sheets; ink wash with pen line; riso layers with linocut gouge knockouts.

## Performance at 3840×2160

- The frame is 8.3 million pixels, about 33 MB per full-frame buffer. The bundled engine does one per-pixel pass per ink layer plus one for paper; a seven-ink piece renders in a few seconds on a recent laptop.
- For hand-written media, budget one or two full-frame `getImageData` passes in total, at the end. Never call it in a loop.
- Generate noise once on a 512–1024 px tile and apply it with `createPattern` at a random offset and rotation.
- Render low-frequency effects (vignette, density drift) at 1/8 scale and upscale.
- Batch strokes into one path per style. Pre-render stamps and stitches as sprites.
- Use the browser pane to render. Do not launch headless browsers for this; they are heavy and unnecessary.

## Research gaps

No published technique write-up was found for bokashi, cyanotype, cut paper or colored pencil in creative-coding sources; those recipes are derived from the physical process. p5.brush is the richest reference for dry media, but its standalone build needs WebGL2, so read it for ideas and don't depend on it.
