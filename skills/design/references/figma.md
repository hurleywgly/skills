# Figma canvas

Read this before the first Figma call of a run. It applies only when the canvas is Figma.

## Before any write

Load the Figma plugin's own skill for the write tool (`figma-use`) before each write call, as the Figma tools require. For bulk first-pass screens the plugin's screen-generation skill can help; for turning the finished design into code, its design-to-code skill is the downstream step.

## Brief fields

```yaml
figma_file_key: null             # null = create a new file; or an existing file key
figma_page_name: null            # null = create a new page
max_calls: 60                    # cap on Figma calls for this run
```

## Setup

1. **File:** create a new one or verify the existing key.
2. **Page isolation:** create a new dedicated page for every run and write only there, so a run can never damage existing design work. Scan the file first if existing work is referenced.
3. **Token page** (multi-screen runs): a "Design Tokens" frame with color swatches, type scale, spacing scale and button variants. It is the ground truth for consistency across screens and costs two or three calls.
4. Define colors and sizes as constants at the top of each write script, so screens cannot drift.

## Frame rules

These prevent collapsed containers that have to be expanded by hand.

1. `clipsContent = false` on all container and section frames.
2. `layoutSizingVertical = "HUG"` on page-level and section-level frames, so content sets the height.
3. Fixed `resize()` only for elements with known dimensions (buttons, icons, specific cards).
4. Top-level screen frames: fixed width (1440), height HUG.
5. No hardcoded height on auto-layout parents.

Run these as a check in the finishing pass, along with renaming auto-generated layers.

## Call budget

Count every Figma tool call against the run's `max_calls`, and track the day's total in `output/design/rate-tracker.json`:

```json
{ "date": "YYYY-MM-DD", "calls": 0 }
```

- Before starting: if the day's remaining calls are below the run's `max_calls`, warn and suggest a smaller scope; below 20, do not start. The floor leaves room for manual use.
- Split the run budget across sections so one section cannot starve the rest.
- At 75% of the run budget, switch to finishing only.
- On a rate-limit (429) response, wait 60 seconds. A second one ends the run with a summary.

`--stretch` raises the run budget, not the daily floor. `--budget N` overrides `max_calls`.

Rough costs, for planning:

| Operation | Typical calls |
|-----------|--------------|
| File, page and token page setup | 3-5 |
| One section (create + screenshot) | 4-5 |
| One refinement round (fix + screenshot) | 2-3 |
| Whole-design composition round | 3-4 |
| Motion spec frame | 1-2 |
| Finishing pass | 2-3 |

The diverge step costs roughly one section per direction; keep each direction to a single rough frame.

## Multi-page coherence

Build the token page first. After all screens exist, screenshot each and compare header heights, CTA treatment, font sizes and footers in one pass, then fix drift before closing.
