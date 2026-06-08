---
name: update-from-session
description: Extract learnings from current session and persist them to memory.
disable-model-invocation: true
---

# /update-from-session

Extract learnings from current session and persist them.

## Behavior

1. Review the session: What did we work on? What problems did we solve?
2. Ask:
   - "What from this session should we remember for next time?"
   - "Any decisions made that should go in the changelog?"
   - "Any patterns worth capturing in memory?"
3. **Gut-check before writing each candidate rule or memory:**
   - *Name the specific friction this fixes.* If you can't name a concrete moment where this would have changed behavior, demote it to a memory note instead of a behavioral rule in your root instruction file (CLAUDE.md / AGENTS.md).
   - One honest question beats a four-question form. The bar is "past-me would have acted differently reading this," not "this sounds wise."
4. Based on answers:
   - Add memory entries to your project's memory directory (e.g. `./memory/`)
   - Append decisions to your project's `changelog.md` (use `**Why:**` field — it's the load-bearing one)
   - If the change affects your workspace itself (new or updated skill, new behavior of an existing skill, root instruction file, persistent memory), also append a one-line entry to your top-level `CHANGELOG.md` under today's date heading. Format: `- [shipped what] — [optional: trigger / why]`. Pure-project decisions don't go here. The CHANGELOG is the lightweight, content-ready surface — keep it scannable.
   - Suggest updates to `context.md` if active state changed
   - Suggest updates to your root instruction file (CLAUDE.md / AGENTS.md) if system-wide learning

## Memory Entry Format

Filename: `[topic]-[type].md` (e.g., `api-design-pattern.md`, `notion-integration-decision.md`)

```markdown
# [Topic]

**Type:** [pattern / decision / learning]
**Date:** [YYYY-MM-DD]
**Context:** [What prompted this]

## Summary

[The learning/pattern/decision]

## Application

[When/how to apply this in future]
```

## Usage

```
/update-from-session
```
