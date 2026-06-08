---
name: channel
description: Load a package's context and persona into the current conversation — fuzzy match by name, auto-detect type, budget-aware
disable-model-invocation: true
---

# /channel

Load a package's persona and context into the current conversation. One command to become any package.

## Invocation

| Form | What It Does |
|------|-------------|
| `/channel [name]` | Fuzzy-match a package and load its context |
| `/channel list` | Show all available packages with type and one-liner |
| `/channel [name] --deep` | Override the default budget and load all readable knowledge files |

## Phase 1: Resolve Package

**Package root**: Always your workspace `packages/` directory (e.g. `./packages/`).

1. List all directories in `packages/` (ignore loose `.md` files — those are capsules, not packages. If user targets one, suggest `/capsule load` instead).
2. **Shorthand match first**: Scan `manifest.md` files in each package directory for a `shorthand` field that exactly matches the user's input.
3. **Fuzzy match fallback** (if no shorthand match):
   - Exact directory name match (e.g., "essay-copilot")
   - Substring match (e.g., "essay" matches "essay-copilot")
4. If multiple matches, present them and ask the user to pick.
5. If zero matches, show available packages and bail.

## Phase 2: Detect Package Type

Scan the resolved directory to classify the package.

**Detection priority** (a package may have overlapping signals):

| Priority | Signal | Type | Label |
|----------|--------|------|-------|
| 1 | `manifest.md` with `type` field | Use declared type | — |
| 2 | `.global-state.json` or `*AGENT*.md` exists | **Type C** | Operational Package |
| 3 | `system_prompt.md` exists | **Type A** | Claude Project Package |
| 4 | Otherwise | **Type B** | Study/Reference Package |

## Phase 3: Load Context (Type-Specific)

### Type A: Claude Project Package

1. **`system_prompt.md`** — Read in full. This is the persona. Treat it as the active behavioral guide.
2. **`README.md`** — Read in full. Provides overview and usage context.
3. **`knowledge/` files** — Budget-aware loading (see Phase 4).

### Type B: Study/Reference Package

1. **`README.md`** — Read in full.
2. **Structural maps** — Read `PROJECT_MANIFEST.md`, `EXPORT_SUMMARY.md`, or `QUICK_REFERENCE.md` (whichever exist).
3. **Other top-level `.md` files** — Read remaining top-level markdown files.
4. **Subdirectory contents** — List subdirectories and their files. Do NOT auto-read. Report what is available.

### Type C: Operational System Package

1. **Agent instruction file** — Find `*AGENT*.md` or the largest top-level `.md` that is not README/DASHBOARD. Read in full.
2. **`GLOBAL_DASHBOARD.md`** — Read in full (current state overview).
3. **`.global-state.json`** — Read in full (machine-readable state).
4. **`README.md`** — Read in full.
5. **Subdirectory listing** — List all subdirectories and their contents. Do NOT auto-read. Report what is available.

## Phase 4: Context Budget

Default budget rules for knowledge files (primarily Type A `knowledge/` folders):

| Content | Default | `--deep` |
|---------|---------|----------|
| `.md` files (≤8 total) | Read all in full | Read all in full |
| `.md` files (>8 total) | Read first 5 by filename order, list rest | Read all in full |
| `.pdf` files | First 3 pages each, report full list | First 5 pages each |
| Single file >500 lines | Read first 200 lines, note total | Read in full |
| Binaries (images, zips) | Skip, note existence | Skip, note existence |

## Phase 5: Present & Activate

After loading, present:

```
## Channeling: [Package Name]
**Type:** [Claude Project Package | Study Package | Operational Package]
**Loaded:**
- [file] — [line count or "full"]
- [file] — [first N pages]
...

**Available but not loaded:**
- [file] — [reason: budget, binary, etc.]

**Persona active.** [1-sentence summary from system_prompt.md or README]

Ready. How can I help?
```

Then: adopt the persona and behavior defined in the loaded `system_prompt.md` or agent instruction file. The package's instructions become the active behavioral guide for the remainder of the conversation (or until the user invokes `/channel` again or says "exit channel").

## `/channel list` Behavior

Scan `packages/`, classify each directory, and present:

```
## Available Packages

| Package | Shorthand | Type | Summary |
|---------|-----------|------|---------|
| essay-copilot | essay | Claude Project | [first non-heading line from primary file] |
| networking-sidekick | networking | Operational | ... |
| pm-interview-prep-copilot | pm-prep | Study | ... |
...

Usage: `/channel [name]` — e.g., `/channel essay`
```

For shorthand: read from `manifest.md` if it exists, otherwise show "—".
For summary: read the first non-blank, non-heading line from the primary file (`system_prompt.md`, `*AGENT*.md`, or `README.md`).

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| Package has `.claude/` subfolder | Ignore — project-level Claude config, not content |
| Loose `.md` file in packages/ (capsule) | Skip in `/channel list`. If targeted, suggest `/capsule load` |
| User says "exit" or "stop channeling" | Drop persona, return to default agent behavior |
| Knowledge folder contains zip/binary | Note existence, do not read |
| No recognizable entry point | Report "Package found but has no entry point. List contents?" |
| `manifest.md` exists | Use `shorthand` for matching, `type` for classification |
| No `manifest.md` | Fall back to fuzzy name matching and file-signal detection |

## What /channel Does NOT Do

- Modify any package files (read-only operation)
- Create new packages (use `/projector` for that)
- Execute capsule integration plans (use `/capsule load` for that)
- Persist the channel across sessions (conversational context only)
