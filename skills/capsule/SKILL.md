---
name: capsule
description: "Create or load a Capsule: a self-contained markdown file that transfers knowledge, patterns, skills, or a whole system from one agent or session to another. Sizes itself automatically (quick, standard, deep), sanitizes sensitive data, and always ends in a concrete integration plan. Use for handoffs between agents, sessions, tools, or people."
argument-hint: "[what to capture] | load <path>"
disable-model-invocation: true
---

# /capsule

Create or load Capsules for system-to-system knowledge transfer. Capsules are self-contained markdown artifacts that package knowledge, patterns, skills, and integration plans into a portable format any receiving agent can act on.

## Purpose

Formalize the capsule pattern with:
- **Automatic complexity detection** — Quick, Standard, or Deep tier based on content signals
- **Mandatory actionability** — Every Standard/Deep capsule includes a concrete integration plan
- **Skill portability** — Deep capsules include complete skill artifacts inline so receiving systems can replicate without follow-up questions
- **Sanitization** — Strip sensitive data before cross-system transfer

## Modes

| Mode | Invocation | What It Does |
|------|-----------|--------------|
| **Create** | `/capsule` or `/capsule "description"` | Build a new capsule from session context or referenced files |
| **Load** | `/capsule load [path]` | Read an existing capsule and execute its integration plan |

---

## Create Mode: 6-Phase Workflow

### Phase 1: Intake

Determine what to transfer and where it's going.

- If invoked with a description or file references, use those as source material
- If bare invocation, scan the current session context and ask:
  - "What should we transfer?"
  - "Where is it going?" (which system/context will receive this)
- Identify all source material: session context, files, URLs, patterns from conversation

### Phase 2: Complexity Detection (Auto-Triage)

Assess source material and auto-select tier:

| Signal | Quick | Standard | Deep |
|--------|-------|----------|------|
| Topic count | 1-2 focused | 3-5 related | 6+ or cross-domain |
| Artifact types | No skills/code | Patterns, learnings | Skills, schemas, infrastructure |
| Transfer type | Knowledge/context dump | Session handoff, meeting prep | Skill replication, infrastructure |
| Action needed | "Read and understand" | "Integrate these ideas" | "Replicate and build" |

**Decision tree:**
1. Includes skill definitions, schemas, or infrastructure changes that need to be **installed** in the receiving system? -> **Deep**
1b. Includes code or configs that **illustrate a point** but don't need installation? -> **Standard** with code inline
2. Includes 3+ distinct learnings, patterns, or strategic shifts? -> **Standard**
2b. Is a session handoff, meeting prep, or context fork? -> **Standard** (needs Integration Plan for receiver to pick up where sender left off). The size rule in Phase 3 can still drop a short handoff to Quick; when it does, keep the next step as one line in Core Content
3. Otherwise -> **Quick**

Announce the detected tier and rationale. Let the user override if they disagree.

**Category and archetype**: Alongside tier, classify the capsule's category (what the receiver needs to do: Full System, Knowledge Pillar, Conversation Thread, or Living Reference) and its archetype (how the knowledge behaves after delivery: Perishable, Handoff, Seed, Steroid, Delta, Trainer, or Dormant). The heuristics and the compression strategy for each are in `references/taxonomy.md`; read it now. Announce both. They shape compression in Phase 3 and do not change the tier.

### Phase 3: Extraction & Assembly

**Artifact classification** — Before compressing, classify each artifact in the source material:
- **NARRATIVE**: Context, explanations, rationale, learnings → compress normally per tier
- **STRUCTURED**: Skill definitions, schemas, configs, API contracts, code interfaces → copy to Verbatim Payloads section exactly as-is

Classification heuristic: **"If changing a single character could change the behavior of a system that consumes this artifact, route to Verbatim Payloads. Everything else gets LLM-compressed."**

Behavior varies by tier. Load lenses from the workspace's `lenses/` directory as specified.

**Size.** The line counts below are ceilings, not targets. A capsule is read in full by an agent with a limited context window, so every line it does not need costs the receiver attention. Write the smallest capsule that still lets the receiver act without a follow-up question, and stop there. A capsule longer than the material it carries has failed: when the source is short and the receiver can open it, send the pointer plus the decisions, open questions and next step, and drop to the Quick tier even if the content would otherwise read as Standard.

**Quick (up to about 60 lines)**
- Direct extraction, structured sections
- Lens: Synthesizer only
- Focus on clarity and conciseness
- No Integration Plan required

**Standard (up to about 200 lines)**
- Multi-topic extraction with pattern identification
- Generate numbered action items and integration steps
- Lens: Synthesizer -> Guardian
- Include the Integration Plan. Include Patterns & Learnings and Signals only when there is something real to put in them; an empty or padded section costs the receiver more than its absence

**Deep (as long as the payloads require, with the narrative around them held to Standard length)**
- Full extraction with skill artifacts inline
- JSON schemas if relevant
- Concrete integration plan with install/setup commands
- For each skill artifact, include ONE of:
  - Complete SKILL.md inline (if <200 lines)
  - Public URL + install instructions
  - Full specification sufficient to recreate from scratch
- Lens: Synthesizer -> Architect -> Guardian -> Sculptor
- Apply `/projector` principles: discovery, fidelity assessment, knowledge file curation

**Lens activation**: For each lens in the sequence, read the lens file from `lenses/[name].md` (relative to the workspace root) and apply its perspective to the assembled content. Each lens reviews the output of the previous one and may correct it, cut from it, or add something the receiver would be blocked without. A lens pass that only adds commentary has made the capsule worse.

**Missing lenses**: If `lenses/[name].md` doesn't exist (e.g., receiving system lacks lens files), skip that lens activation, proceed with default perspective, and name the unavailable lenses in one line in section 7 of the capsule.

**Source compression**: When source material is verbose relative to the target tier, compress before assembling:
- Strip ceremony (headers, boilerplate, repeated context the receiver won't need)
- Preserve specifics (exact commands, file paths, config values, code snippets)
- Preserve relational structures (composition patterns, dependency chains, workflow sequences, portable-vs-specific distinctions) as named, addressable elements — not scattered within component descriptions
- Convert narrative into structured form (paragraphs become bullet points or tables)
- Keep the ratio: if a 500-line source doc feeds a Quick capsule, extract the 10 lines that matter, not a 150-line summary of 500 lines
- Point instead of copying when the receiver can open the source: give the path or URL and say exactly what to read there. A pointer is smaller than a summary and loses nothing. Copy content in only when the receiver cannot reach it (a different machine, a different owner, a session that is ending)
- Before compressing, list the source's distinct items (decisions, facts, open questions, artifacts). Each one ends up in the capsule, behind a pointer, or in a one-line "Left out" note saying what was dropped and why. Loss should be a choice the receiver can see, not something that happens during summarizing

### Phase 4: Sanitization

Scan all assembled content before writing:

| Category | Action |
|----------|--------|
| Company data | Replace with generic descriptions or `[REDACTED]` |
| Credentials/tokens | Remove entirely, note in Sanitization Notes that they're needed |
| Personal names (non-sender/receiver) | Generalize to roles (e.g., "the engineering lead") |
| Internal URLs | Remove or describe what was linked |
| Proprietary metrics | Strip specific values, keep directional insight |

**Same-owner exception**: If both sending and receiving systems belong to the same owner:
- Skip personal sanitization (preserve teammate names, relationship context)
- Session handoff capsules default sanitization to off entirely
- Company/proprietary data is still stripped regardless

**Capsule-in-capsule rule**: If source material includes a previously created capsule whose Sanitization Notes say "Skipped (same-owner)," re-run full sanitization on that material. Prevents an unsanitized capsule from being pulled into a future capsule shared externally.

### Phase 5: Verification

Self-check before writing to disk. Evaluate each criterion and report results:

1. **Actionability**: Does every section inform or instruct? Flag any purely descriptive sections at Standard/Deep tiers.
2. **Completeness**: For skills, is there enough to replicate without follow-up questions? Flag gaps.
3. **Assumptions**: Are implicit assumptions made explicit? (e.g., "receiving system has Claude Code", "requires curl + jq")
4. **Proportionality**: Does depth match tier? Flag bloated Quick capsules or thin Deep capsules.
5. **Receivability**: Does this capsule work if the receiver has never seen the source system? Flag any section that assumes intimate knowledge of the sender's setup.
6. **Fidelity**: For each Verbatim Payload, verify content exactly matches source. Compute hash. Flag any payload that appears modified.
7. **Coverage**: Walk the item list from Phase 3. Every item is present, pointed to, or named in "Left out". Flag anything that disappeared without a trace.
8. **Economy**: Could any section be cut, turned into a table, or replaced by a pointer without the receiver losing the ability to act? If so, do it before writing.

Present verification results to the user. User approves, requests adjustments, or overrides.

### Phase 6: Output

**Output directory resolution** (in order):
1. If the workspace's CLAUDE.md or project config specifies a packages/output directory, use that
2. If a `packages/` directory exists at the workspace root, use it (create if missing)
3. Otherwise, write to the current working directory

Write the capsule to `{output_dir}/[slug]-capsule.md`.

Report:
```
Capsule written to {output_dir}/[slug]-capsule.md

Tier: [Quick | Standard | Deep]
Category: [Full System | Knowledge Pillar | Conversation Thread | Living Reference]
Archetype: [Perishable | Handoff | Seed | Steroid | Delta | Trainer | Dormant]
Lines: [N]
Sections: [list]
Sanitization: [Applied / Skipped (same-owner)]
Verification: [All passed / N issues flagged]

Ready for dispatch.
```

---

## Load Mode: `/capsule load [path]`

Read an existing capsule and execute its integration plan.

### Load Workflow

**Step 1: Read & Parse**
- Read the capsule at the given path
- Identify tier and sections from the canonical schema
- Validate structure (warn if non-standard format)
- **Legacy detection**: If file uses `.FLOPPY.md` naming or lacks `**Tier:**` metadata, treat as a legacy floppy. Present as context briefing, optionally offer to upgrade to canonical capsule schema. Never attempt to execute a nonexistent Integration Plan.

**Step 2: Briefing**
- Present the Dispatch Summary and Integration Plan to the user
- "This capsule wants to do N things. Here's the plan:"
- List each integration step with a brief description

**Step 3: Prerequisites Check**
- Verify the receiving system has what's needed (tools, directories, permissions)
- Flag gaps before starting execution
- If prerequisites are unmet, present options: install them, skip affected steps, or abort

**Step 4: Step-by-Step Execution**
- Walk through the Integration Plan steps sequentially
- For each step:
  - Explain what it will do
  - Execute (create files, install skills, update configs)
  - Confirm success before moving to the next step
  - Before any file write, check if the target path already exists. If yes, show diff and require explicit user confirmation before overwriting. (Step 5 does this for skills; this extends the same protection to all files.)
- If a step fails, pause and ask the user how to proceed

**Step 5: Skill Installation** (Deep capsules only)
- If a Skill Artifacts section exists, install each skill:
  - **Inline SKILL.md**: Write to `.claude/skills/[name]/SKILL.md`
  - **URL reference**: Fetch and install
  - **Specification**: Generate SKILL.md from spec, confirm with user before writing
- Check for conflicts with existing local skills. If found, flag and ask user to resolve before overwriting.

**Step 6: Verification**
- Run the capsule's verification criteria (from Integration Plan)
- Report what landed and what didn't

**Step 7: Eject**
- Report final results: steps completed, skills installed, issues encountered
- "Capsule consumed. [N/M] steps completed successfully."

### Load Edge Cases

| Scenario | Behavior |
|----------|----------|
| No Integration Plan (Quick tier) | Present content as context briefing, no execution steps |
| Skill conflicts with existing local skill | Flag conflict, show diff, ask user to resolve |
| Unknown/untrusted source | Full sanitization review before executing any steps |
| Malformed capsule (missing sections) | Parse what exists, warn about missing sections, proceed with available content |

---

## Canonical Capsule Schema

All capsules follow this structure. Sections are included or omitted based on tier.
Omitted sections are dropped entirely, not left blank.

```markdown
# [NAME].CAPSULE.md

> [One-line tagline in system-to-system voice]

**Version:** [1.0]
**Created:** [YYYY-MM-DD]
**From:** [Sending system/context]
**To:** [Receiving system/context]
**Purpose:** [1-2 sentences]
**Tier:** [Quick | Standard | Deep]
**Archetype:** [Perishable | Handoff | Seed | Steroid | Delta | Trainer | Dormant]

---

## 1. Dispatch Summary                    [ALL TIERS]
What's being transferred and why. 2-5 sentences.

## 2. Core Content                        [ALL TIERS]
Primary knowledge payload. Structure varies by content type.

## 3. Patterns and Learnings              [STANDARD+]
Transferable principles. Each pattern includes:
- **Name**: Short identifier
- **What**: The pattern itself
- **When**: Trigger conditions
- **Why**: The insight behind it

## 4. Skill Artifacts                     [DEEP only]
Per skill: purpose, invocation, then one of:
  - Inline SKILL.md (if <200 lines)
  - Public URL + install commands
  - Full specification to recreate from scratch

## 5. Integration Plan                    [STANDARD+]
Numbered steps. Prerequisites listed upfront.
Each step follows: **Step N: [Action]** / Where: [path] / Do: [instruction] / Verify: [confirmation] / Rollback: [if fails]. Mark each step as `[auto]` (agent executes) or `[manual]` (human required).
This section is why capsules transfer capability, not just information.

## 6. Signals                             [STANDARD+]
Suggestions for the receiving system to evaluate.
Not mandates — prompts for the receiver's own judgment.

## 7. Sanitization Notes and Left Out    [ALL, when either applies]
What was stripped and why, a "Left out" line for anything
deliberately dropped during compression, and any lenses that were
unavailable. Include this section whenever something was dropped,
even if sanitization itself was skipped. Helps the receiver know
what context is missing and whether to request it.

## 8. Verbatim Payloads                    [STANDARD+, when applicable]

Content below MUST be reproduced exactly. No paraphrasing, reformatting, or compression.

### Payload: {name}
**Type:** {skill-definition | sql-schema | api-contract | config | code-interface}
**Target:** {file path where receiver should write this}
**Hash:** sha256:{first 16 chars}

~~~{language}
{exact content}
~~~

---

*Dispatch complete.*
```

---

## Lens Sequences by Tier

| Tier | Sequence | Rationale |
|------|----------|-----------|
| Quick | Synthesizer | Clarity and focus only |
| Standard | Synthesizer -> Guardian | Strategic extraction + completeness/risk check |
| Deep | Synthesizer -> Architect -> Guardian -> Sculptor | Full analysis: strategy, systems, protection, then narrative polish |

---

## Usage Examples

**Simple transfer:**
```
/capsule "Transfer the notification hook learnings to my other workspace"
```

**Multi-pattern transfer:**
```
/capsule "Package up the lens sequence patterns, compounding loop, and zero-dependency architecture for a new workspace"
```

**Skill replication:**
```
/capsule "Replicate three of my skills for an external system"
```

**Load an existing capsule:**
```
/capsule load packages/work-dispatch-capsule.md
```

**Bare invocation (guided):**
```
/capsule
```

## Integration

Works with other skills:
- **Input from**: Any session context, `/update-from-session` learnings, skill definitions
- **Output to**: Resolved output directory (see Phase 6), receiving systems via load mode
- **Related**: `/projector` (sub-skill principles for Deep tier packaging)

## Outputs

| Artifact | Path | Shape | Consumed by |
|----------|------|-------|-------------|
| Capsule | `{output_dir}/[slug]-capsule.md` | Canonical Capsule Schema (see above) — sections 1-8 by tier | `/capsule load`, `/channel`, agent-to-agent transfer, Claude.ai Projects, ChatGPT Projects |

`output_dir` resolution lives in Phase 6. If schema or path changes, update this table — downstream skills (`/channel`, `/capsule load`) parse the structure.
