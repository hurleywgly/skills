# Capsule categories and archetypes

Read this in Phase 2 when classifying a capsule, and in Phase 3 for the matching compression strategy.

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

- **Full System**: Preserve the operating manual. Keep system boundaries, constraints, decision rationale, integration points. Preserve how components compose at runtime (workflow sequences, trigger chains, parallel vs sequential modes). Keep portable-vs-platform-specific distinctions when present. Compress verbose implementation details and redundant documentation.
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
