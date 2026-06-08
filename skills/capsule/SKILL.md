---
name: capsule
description: Create and load Capsules — self-contained markdown artifacts for agent-to-agent knowledge transfer with automatic complexity detection and mandatory actionability
disable-model-invocation: true
---

<!-- PORTABILITY: This skill is published to github.com/hurleywgly/skills and must remain workspace-agnostic.
No hardcoded absolute paths. No personal names in logic. Use workspace-relative conventions —
the agent resolves paths from its own CLAUDE.md / AGENTS.md or workspace root at runtime. -->

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
2b. Is a session handoff, meeting prep, or context fork? -> **Standard** (needs Integration Plan for receiver to pick up where sender left off)
3. Otherwise -> **Quick**

Announce the detected tier and rationale. Let the user override if they disagree.

**Category detection**: Alongside tier, classify the capsule category (Full System, Knowledge Pillar, Conversation Thread, or Living Reference) using the heuristics in the Capsule Categories section. Announce the detected category. Category informs compression strategy in Phase 3 but does not change tier selection.

**Archetype detection**: Alongside tier and category, classify the capsule archetype — the temporal transfer pattern describing how the knowledge behaves after delivery. Use the heuristics in the Capsule Archetypes section. Announce the detected archetype. Archetype informs compression strategy in Phase 3 but does not change tier selection.

### Phase 3: Extraction & Assembly

**Artifact classification** — Before compressing, classify each artifact in the source material:
- **NARRATIVE**: Context, explanations, rationale, learnings → compress normally per tier
- **STRUCTURED**: Skill definitions, schemas, configs, API contracts, code interfaces → copy to Verbatim Payloads section exactly as-is

Classification heuristic: **"If changing a single character could change the behavior of a system that consumes this artifact, route to Verbatim Payloads. Everything else gets LLM-compressed."**

Behavior varies by tier. Each tier runs a sequence of review perspectives (a lightweight multi-perspective analysis pass) over the assembled content.

**Quick (50-150 lines)**
- Direct extraction, structured sections
- Perspective: Synthesis only
- Focus on clarity and conciseness
- No Integration Plan required

**Standard (150-400 lines)**
- Multi-topic extraction with pattern identification
- Generate numbered action items and integration steps
- Perspectives: Synthesis -> Risk
- Include Patterns & Learnings, Integration Plan, and Signals sections

**Deep (400+ lines)**
- Full extraction with skill artifacts inline
- JSON schemas if relevant
- Concrete integration plan with install/setup commands
- For each skill artifact, include ONE of:
  - Complete SKILL.md inline (if <200 lines)
  - Public URL + install instructions
  - Full specification sufficient to recreate from scratch
- For Full System capsules: after extracting components, explicitly map how they connect at runtime — dependency chains, composition patterns (parallel vs sequential), workflow sequences, and which components are portable vs platform-specific. Capture these in the System Relationships section.
- Perspectives: Synthesis -> Systems -> Risk -> Design
- Apply packaging principles: discovery, fidelity assessment, knowledge file curation

**Perspective activation**: For each perspective in the sequence, apply that lens to the assembled content — Synthesis (clarity, what matters), Systems (how components relate), Risk (gaps, edge cases, completeness), Design (narrative polish). Each perspective reviews and enriches the output of the previous one.

**Skipping perspectives**: If a perspective doesn't apply to the material, skip it, proceed with the default review, and note in the output which perspectives were skipped.

**Source compression**: When source material is verbose relative to the target tier, compress before assembling:
- Strip ceremony (headers, boilerplate, repeated context the receiver won't need)
- Preserve specifics (exact commands, file paths, config values, code snippets)
- Convert narrative into structured form (paragraphs become bullet points or tables)
- Keep the ratio: if a 500-line source doc feeds a Quick capsule, extract the 10 lines that matter, not a 150-line summary of 500 lines

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
7. **Relationship Fidelity**: For Full System capsules, verify that cross-component relationships, composition patterns, and portability boundaries are explicitly captured — not scattered within component descriptions.

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

## 5b. System Relationships               [DEEP only, when source is Full System]
How components connect at runtime. Dependency declarations, composition
patterns, workflow sequences, and portability boundaries.

Format per relationship:
- **[Component A] → [Component B]**: [how/why they connect]
- **Portable**: [what survives platform changes]
- **Platform-specific**: [what needs replacement on a different system]

## 6. Signals                             [STANDARD+]
Suggestions for the receiving system to evaluate.
Not mandates — prompts for the receiver's own judgment.

## 7. Sanitization Notes                  [ALL, if applied]
What was stripped and why. Helps the receiver know
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

## Perspective Sequences by Tier

| Tier | Sequence | Rationale |
|------|----------|-----------|
| Quick | Synthesis | Clarity and focus only |
| Standard | Synthesis -> Risk | Strategic extraction + completeness/risk check |
| Deep | Synthesis -> Systems -> Risk -> Design | Full analysis: strategy, systems, protection, then narrative polish |

---

## Capsule Categories

Categories are orthogonal to tiers — **category = receiver intent**, **tier = output volume**. Classification question: **"What does the receiver need to DO?"**

| Category | Receiver Intent | Key Preservation Target |
|----------|----------------|------------------------|
| **Full System** | Operate within the system | Operating manual, system boundaries, constraints |
| **Knowledge Pillar** | Understand a domain | Conceptual relationships, depth |
| **Conversation Thread** | Continue in-flight work | Decisions, open questions, temporal context |
| **Living Reference** | Stay current on evolving state | Structure for incremental update, delta-friendliness |

### Category Detection (Phase 2)

Detect category alongside tier during Complexity Detection. Category influences compression strategy in Phase 3 but does NOT override tier selection.

**Detection heuristic:**
1. Source material describes a complete system with operational rules, constraints, skills, or infrastructure → **Full System**
2. Source material is structured domain knowledge organized topically (documentation, guides, specifications) → **Knowledge Pillar**
3. Source material is a temporal conversation or session with decisions, open questions, in-flight work → **Conversation Thread**
4. Source material is an evolving state artifact that changes over time and needs delta-friendly structure → **Living Reference**

### Compression Strategy by Category

- **Full System**: Preserve the operating manual. Keep system boundaries, constraints, decision rationale, integration points. Compress verbose implementation details and redundant documentation.
- **Knowledge Pillar**: Preserve conceptual relationships. Keep how things connect, the "why," and representative examples rather than exhaustive enumeration. Compress boilerplate.
- **Conversation Thread**: Preserve decisions and open questions. Keep what was decided and by whom, what's unresolved, specific in-flight context (file paths, branch names, error messages). Compress deliberation narrative.
- **Living Reference**: Preserve structure over content. Keep the schema and update conventions. Include `last_updated` markers per section. Optimize for cheap incremental updates.

---

## Capsule Archetypes

Archetypes are orthogonal to both tiers and categories — **archetype = temporal transfer pattern**, describing how the knowledge behaves after delivery. Classification question: **"What is the shelf-life and activation pattern of this knowledge?"**

Ordered by shelf-life (shortest to longest):

| Archetype | Transfer Pattern | Optimize For |
|-----------|-----------------|--------------|
| **Perishable** | Use once, discard | Aggressive compression, minimal patterns section |
| **Handoff** | Baton pass, continuity transfer | Decisions made, open threads, where-we-left-off context |
| **Seed** | Intentionally incomplete, designed for receiver to expand | The question/direction; strip supporting detail |
| **Steroid** | Rapid large-scale absorption, act immediately | Action items and critical context; compress background |
| **Delta** | Incremental sync, periodic change snapshot | Changes only; assume base context exists in receiver |
| **Trainer** | Permanent learning, long-term integration | Conceptual relationships, the "why," transferable principles |
| **Dormant** | Pre-loaded, inactive until triggered | Trigger conditions and the full payload |

### Archetype Detection (Phase 2)

Detect archetype alongside tier and category during Complexity Detection. Archetype influences compression strategy in Phase 3 but does NOT override tier selection.

**Detection heuristic:**
1. Source material serves a single task with no reuse value (error logs, one-off requests) → **Perishable**
2. Source material continues in-flight work from a prior session, picking up where it left off → **Handoff**
3. Source material plants a direction or question without prescribing the path, designed for the receiver to explore → **Seed**
4. Source material introduces a large, urgent shift the receiver must internalize and act on immediately → **Steroid**
5. Source material provides incremental updates to an already-established base context → **Delta**
6. Source material teaches concepts, patterns, or principles meant to be retained permanently → **Trainer**
7. Source material should sit inactive until a specific condition or question triggers it → **Dormant**

### Compression Strategy by Archetype

- **Perishable**: Compress aggressively. Minimal or no Patterns section. Strip everything the receiver won't need after the single task completes.
- **Handoff**: Preserve decisions, open questions, and temporal state. Compress deliberation narrative. Keep specific artifacts (branch names, file paths, error messages).
- **Seed**: Preserve the core question or direction. Strip supporting detail and evidence — the receiver should explore fresh, not inherit the sender's framing.
- **Steroid**: Preserve action items and critical context for immediate execution. Compress background rationale and history.
- **Delta**: Preserve changes only. Assume the receiver has base context. Use diff-style structure where possible. Strip unchanged material entirely.
- **Trainer**: Preserve conceptual relationships, the "why," and representative examples. Compress boilerplate and exhaustive enumeration. Optimize for long-term retention.
- **Dormant**: Preserve trigger conditions explicitly and the full payload intact. The receiver needs to know exactly when to activate and have everything ready when that moment comes.

### Audience-Targeting (Modifier)

Any archetype can carry audience-targeting attributes — who sees it, what's redacted, what level of detail is appropriate. This is not a separate archetype but a modifier that applies to any of the seven types. It connects directly to the sanitization layer (same-owner vs. cross-team vs. public transfers).

---

## Usage Examples

**Simple transfer:**
```
/capsule "Transfer the notification hook learnings to my other workspace"
```

**Multi-pattern transfer:**
```
/capsule "Package up the review-perspective patterns, compounding loop, and zero-dependency architecture for a new workspace"
```

**Skill replication:**
```
/capsule "Replicate /jira, /today, and /pdf skills for an external system"
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

Works with other skills in your workspace:
- **Input from**: Any session context, extracted session learnings, skill definitions
- **Output to**: Resolved output directory (see Phase 6), receiving systems via load mode
- **Related**: any packaging skill (sub-skill principles for Deep tier packaging)

## Output Location

Capsules are saved to `{output_dir}/[slug]-capsule.md`. See Phase 6 for resolution logic.
