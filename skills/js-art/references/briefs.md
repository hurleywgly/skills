# Briefs: what the picture is about

The brief is the fourth dial. It decides how the user tells you what they want, and how indirectly you translate it.

## Why the indirect brief works

The prompt this skill grew from gave the model two long, rambling personal stories and said: capture these feelings, draw nothing from them, no people. The model had no stock image to fall back on, so it had to turn feeling into composition, color and texture.

Reasons to trust the method, strongest first. Be honest with the user that most of this is practitioner theory, not measurement.

1. **Models drift to a familiar center.** Anthropic's design write-up describes generic output as sampling the "high-probability center", and notes that after you ban one default the model finds the next. A literal subject list sits in that center. A personal story with its subject forbidden does not. (The last step is inference.)
2. **Paired constraints.** Stokes's model and the Haught-Tromp experiments found that constraints work in pairs: one rule precludes the obvious, one promotes a search elsewhere. "Nothing from the story" precludes; "capture the emotion" promotes. These are human studies.
3. **Objective correlative.** T.S. Eliot: emotion is conveyed by a set of objects and events that act as its formula, not by naming it. The vignette is the formula.
4. **Synectics and Oblique Strategies.** Both use metaphor or an oblique prompt to break habitual framing.

What is measured elsewhere: render-and-revise loops beat one-pass generation for SVG (trained systems, not plain prompting); asking for several options first raises diversity in text. Both are built into this skill's flow.

What is folk wisdom: "masterpiece", "heart and soul", "use every pixel". Harmless, cheap, unproven. Keep one line of it in the final prompt because the original used it, and don't lean on it.

## The seven brief styles

Offer the two or three that suit what the user has said. A user who already described a subject has chosen their own; don't make them pick.

| Style | What the user gives | What you must not draw | Suits |
|---|---|---|---|
| **1. Memory vignette** | A long, specific personal story with sensory detail | Anything in the story; no people | Any lineage. The default for a feeling. |
| **2. Place and weather** | A location at an exact hour and condition | Landmarks, figures | Shin-hanga, WPA, Adnan, anime backgrounds |
| **3. Music** | A piece of music, real or invented, by tempo, texture and dynamics | Instruments, notation | Orphism, Bauhaus, Matisse |
| **4. Object meditation** | One humble object the user has owned for years | Nothing; this is the one literal style | Cyanotype, katazome, Scandinavian textile |
| **5. Color first** | 3–4 colors with rough proportions | A palette outside the one given | Adnan, Concrete, Martin, quilts |
| **6. Constraint game** | Rules in place of a subject: a mark budget, one tool, no curves | Whatever the rules forbid | Concrete, Martin, any print lineage |
| **7. Homage with a twist** | A named lineage plus one deliberate break from it | Any specific existing composition | Any |

Tiny examples:

1. "The night I got the console: carpet, pizza grease, staying up too late. Draw none of it."
2. "A ferry dock at 5:40am in November fog, just before the lights go off."
3. "A slow record at the wrong speed; brushes on a snare; one bright horn late."
4. "My grandfather's tape measure, in graphite and one red pencil."
5. "70% unbleached paper, 20% oxide green, 8% soot, 2% signal orange."
6. "Exactly 400 strokes, conté crayon only, nothing closer than 40px to the edge."
7. "90s anime background painting, but with no sky and no horizon."

## Writing vignettes for the user

Many users would sooner react than write. Offer to draft vignettes.

- Write in the user's register, lowercase and run-on if that is how the source prompt read. Specific beats pretty: a brand, a temperature, a sound, what the hands were doing.
- 50–90 words each. One scene, one feeling.
- Make them differ in mood, not just setting: one giddy, one tender, one wry, one still.
- Never invent facts about the user's real life and present them as theirs. Write them as scenes anyone could have had, or build from what the user told you.
- Add one line under each saying what it would pull the picture toward (palette tilt, density, one compositional idea).

## Translating a brief into a picture

Do this in writing before any code. Five lines is enough.

1. **Feeling in three words.** For example: giddy, safe, late.
2. **One compositional idea.** Not a subject. "A field of small things with one that is too big." "Everything leans left except one vertical."
3. **Value plan.** Where the lightest and darkest areas sit, and roughly how much of the frame each takes.
4. **The spark.** The one small warm or odd element, and where it goes off-center.
5. **Out of bounds.** What from the brief must not appear, and which of the lineage's "kills it" items you are most at risk of.

## The prompt template

Save this, filled in, as `prompt.md` beside the art. Keep it in sync with the code as the piece changes.

```
Draw one artwork in JavaScript only, on a 2D canvas. 16:9, 3840×2160. One self-contained HTML file.

It must look made by hand with physical media, not digital and not like an SVG.
Medium: <medium and its tells, from media.md>.
Lineage: <lineage> — borrow its grammar, <one line of composition rules>, but make something original. Copy no existing composition.
Palette: <5–8 inks with hex> on <paper>. <One small warm spark, or the palette's own rule.>

Capture this, and draw nothing from it. No people.
===
<the vignette, place, music, object, colors, or rules>
===

One compositional idea: <idea>. A few very large shapes; at least one cropped by the frame. Readable from across a room.
Never: <the lineage's "kills it" list, plus the user's own out-of-bounds>.

Plan the composition in five lines before coding. Render, look at the screenshot, critique it as a working printmaker would, and revise at least once.
Put real care into it and use the whole canvas.
```

## Sources

- Anthropic on default aesthetics: https://claude.com/blog/improving-frontend-design-through-skills
- Constraints and creativity: https://www.rider.edu/sites/default/files/docs/tromp_haught-tromp_PACA_2016.pdf
- Objective correlative: https://www.poetryfoundation.org/learn/glossary-terms/objective-correlative
- Synectics: https://en.wikipedia.org/wiki/Synectics
- Oblique Strategies: https://en.wikipedia.org/wiki/Oblique_Strategies
- Verbalized Sampling: https://arxiv.org/abs/2510.01171
- Render-in-the-loop SVG: https://arxiv.org/abs/2603.09312 and https://arxiv.org/abs/2604.20730
- Naming a medium (watercolor pelican): https://simonwillison.net/2026/Aug/25/pelican-watercolor/
- Anthropic algorithmic-art skill: https://github.com/anthropics/skills
