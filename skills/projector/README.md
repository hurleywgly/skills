# projector

> Package an expert agent harness in minutes

You wish you had a pocket expert for your work, your hobbies, or the shiny thing you found at the end of a late-night internet rabbit hole. Most people settle for a generic assistant — projector turns any topic into a portable, reusable expert you can hand to any major AI platform.

Built for AI coding agents (Claude Code, Codex, and more).

## Install

```bash
npx skills add hurleywgly/skills --skill projector
```

Or add it for a specific agent, e.g. Claude Code:

```bash
npx skills add hurleywgly/skills --skill projector -a claude-code
```

Manual: copy this folder into your agent's skills directory (e.g. `~/.claude/skills/projector/` or `.agents/skills/projector/`).

## What it does

- **Spin up a custom expert.** Point it at a domain or a codebase and it builds a complete package — a layered system prompt plus organized knowledge files — that drops straight into Claude.ai Projects, ChatGPT, NotebookLM, Gemini Gems, or a coding-agent subagent.
- **Interview your way to depth.** Say "interview me" and it asks sharp questions that harness your expertise. It pulls the edge cases, tradeoffs, and scope from you before writing a single file, so the harness you get back is actually useful.

## Why it matters

We all wish we had a pocket expert for our work, hobbies, or the shiny thing we find at the end of a late-night internet rabbit hole. Most people settle for a generic assistant. Projector turns any topic into a portable, reusable expert you can hand to any major AI platform.

## How it fits your workflow

When you start working on a new project, you locate the experts in that field, learn what they know, and piece together a bit of what's most important to them. Then projector takes those seeds and assembles a package of files that you can load into any AI tool you work in.

## Pairs well with

`channel` • `mine` • `capsule` • `research`

## Coverage Levels

Depth of coverage matters more than file count.

| Level | What You Get | Best For | Typical Size |
|-------|-------------|----------|-------------|
| **Essential** | Core persona + key references | Broad roles, general expertise | 3-7 files |
| **Comprehensive** | Full domain coverage, multiple knowledge areas | Domain-specific depth, book synthesis | 8-12 files |
| **Deep** | Primary sources, frameworks, specialized workflows | Hyper-specific experts, source material | 12-20+ files |

## Usage

```
# Standard mode: provide requirements, get a package
"Create a project for a sourdough bread expert"

# Interview mode: deep requirement gathering first
"Interview me to build a fitness coaching project"

# With existing materials
"Build a project from these docs: [attach files]"
```

Output lands in `./packages/[name]/` — a `system_prompt.md`, numbered `knowledge/` files, and a README. The package is portable: upload it to any platform that supports system prompts and knowledge files.

## Examples

![trio-of-projector-examples](https://github.com/user-attachments/assets/f631ac0c-ad5e-4eff-b9ce-718691f13444)

### Dry Cider Expert
**Coverage**: Essential (7 files)

A home cider-making mentor for the Pacific Northwest. Combines fermentation science, regional orchard knowledge, and practical step-by-step guidance.

**Try asking:**
- "What yeast should I use for my first dry cider?"
- "My fermentation seems stuck. What should I do?"
- "What's a good apple blend using grocery store apples?"

---

### Warren Buffett Investment Advisor
**Coverage**: Deep (19 files)

Channels Warren Buffett's investment philosophy with Charlie Munger's intellectual rigor. Backed by 50+ years of shareholder letters, research papers, and primary sources. Challenges your investment theses instead of validating them.

**Try asking:**
- "Should I buy Microsoft at current valuations? Challenge my thesis."
- "I'm consolidating into 3 AI stocks. What am I missing?"
- "Is this a wonderful business at a fair price, or mediocre at a cheap price?"

---

### Parenting Sidekick
**Coverage**: Comprehensive (14 files)

A practical co-pilot that synthesizes 7 parenting books into actionable frameworks. Provides in-the-moment support during tantrums, evidence-based sleep strategies, and age-specific developmental guidance.

**Try asking:**
- "My toddler is having a meltdown about screen time. What do I do right now?"
- "How do I prepare my child for a new sibling?"
- "What does the research say about praise vs. acknowledgment?"

## Using the output packages

You don't need a coding agent to use what projector builds. Each example in `examples/` is a standalone package:

1. Pick an example (or build your own)
2. Copy `system_prompt.md` contents into your platform's instructions field
3. Upload `knowledge/` files as the knowledge base
4. Start chatting

Works with: **Claude Projects** | **ChatGPT Projects** | **Google NotebookLM** | **Gemini Gems**

---

Part of [hurleywgly/skills](https://github.com/hurleywgly/skills). MIT licensed.
