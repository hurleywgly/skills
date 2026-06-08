# capsule

> Portable, actionable knowledge transfer between agents.

Skills give agents repeatable workflows, but workflows without context only get you halfway. The context that makes an agent actually good at something usually dies with the session that built it. Capsules bottle that context and hand it to the next agent.

Built for AI coding agents (Claude Code, Codex, and more).

## Install

```bash
npx skills add hurleywgly/skills --skill capsule
```

Or add it for a specific agent, e.g. Claude Code:

```bash
npx skills add hurleywgly/skills --skill capsule -a claude-code
```

Manual: copy this folder into your agent's skills directory (e.g. `~/.claude/skills/capsule/` or `.agents/skills/capsule/`).

## What it does

- **Bottle knowledge, hand it off.** Package an idea or concept into a portable file that compresses context when it's created and expands on arrival. Loading the capsule in a new session transfers the knowledge with ~90% effectiveness.
- **Start fresh with any context.** Extract only the relevant context you need from one conversation into another — a baton pass that delivers just enough to keep pulling the same thread.

## Why it matters

Skills give agents repeatable workflows, but workflows without context only get you halfway. The context that makes an agent actually good at something usually dies with the session that built it. Capsules bottle that context and hand it to the next agent, which loads just what it needs to do the thing you want — do a task, become an expert, whatever the moment calls for.

## How it fits your workflow

You'll fall in love with a plan, then use capsules to distill the key details you need to start separate sessions covering design, PRD writing, user research, whatever's next. Each capsule carries exactly the context that session needs, and nothing it doesn't.

## Pairs well with

`build` • `projector`

## Usage

```
/capsule "Transfer the authentication patterns to the new project"
```

```
/capsule load path/to/capsule.md
```

```
/capsule
```
Bare invocation walks you through it interactively.

### Modes

**Create** builds a new capsule from session context, referenced files, or a description you provide. It runs through six phases: intake (what to transfer and where), complexity detection (auto-triage into Quick, Standard, or Deep tier), extraction & assembly (compress, classify narrative vs. structured, assemble), sanitization (strip credentials, internal URLs, proprietary data), verification (self-check for actionability and completeness), and output (write to disk).

**Load** reads an existing capsule and walks through its integration plan — parse, present the plan, check prerequisites, execute step-by-step with confirmation, verify results. Quick-tier capsules with no integration plan are presented as context briefings.

### Tiers

Auto-detected from content complexity. You can override.

| Tier | Target Size | Use When | Includes |
|------|-------------|----------|----------|
| **Quick** | 50-150 lines | 1-2 focused topics, pure knowledge transfer | Dispatch Summary, Core Content |
| **Standard** | 150-400 lines | 3-5 topics, session handoffs, meeting prep | + Patterns, Integration Plan, Signals |
| **Deep** | 400+ lines | Skill replication, schemas, infrastructure setup | + Skill Artifacts, Verbatim Payloads |

The key difference: Quick capsules inform. Standard capsules instruct. Deep capsules replicate.

### Categories

Orthogonal to tiers — describes **receiver intent**, not output volume.

| Category | Receiver Needs To... | Preserve |
|----------|---------------------|----------|
| **Full System** | Operate within the system | Constraints, boundaries, operating rules |
| **Knowledge Pillar** | Understand a domain | Conceptual relationships, the "why" |
| **Conversation Thread** | Continue in-flight work | Decisions, open questions, temporal context |
| **Living Reference** | Stay current on evolving state | Structure for incremental updates |

### Archetypes

Orthogonal to both tiers and categories — describes the **temporal transfer pattern**, how the knowledge behaves after delivery. Ordered by shelf-life (shortest to longest).

| Archetype | Transfer Pattern | Optimize For |
|-----------|-----------------|--------------|
| **Perishable** | Use once, discard | Aggressive compression, task-specific context only |
| **Handoff** | Baton pass between sessions | Decisions, open threads, where-we-left-off state |
| **Seed** | Intentionally incomplete, receiver expands | The question/direction, not the answer |
| **Steroid** | Rapid large-scale absorption | Action items and critical context for immediate execution |
| **Delta** | Incremental sync over time | Changes only — assumes base context exists |
| **Trainer** | Permanent learning | Conceptual relationships, the "why," principles |
| **Dormant** | Pre-loaded, inactive until triggered | Trigger conditions and full payload |

### Key concepts

**Artifact classification** — Source material is split into NARRATIVE (compress normally) and STRUCTURED (copy verbatim). The rule: if changing a single character could change system behavior, it goes to Verbatim Payloads untouched.

**Sanitization** — Credentials removed, company data redacted, names generalized to roles. Same-owner transfers (both systems belong to the same person) can skip personal sanitization.

**Verification** — Before output, capsules are checked against six criteria: actionability, completeness, assumption clarity, proportionality, receivability, and verbatim fidelity.

**Integration Plans** — Standard and Deep capsules include numbered steps with prerequisites, actions, verification checks, and rollback instructions. Each step is marked `[auto]` (agent executes) or `[manual]` (human required).

---

Part of [hurleywgly/skills](https://github.com/hurleywgly/skills). MIT licensed.
