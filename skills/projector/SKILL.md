---
name: projector
description: Creates complete Claude Project packages with system prompts and knowledge files for Claude.ai Projects, ChatGPT Projects, Google NotebookLM, Gemini Gems, or Claude Code subagents. Supports interview mode for deep requirement gathering.
version: "2.0.0"
---

# Projector

Create complete Claude Project packages (system prompt + knowledge files) that give Claude deep expertise in specific domains or codebases. Output packages can be imported into Claude.ai Projects, ChatGPT Projects, Google NotebookLM, Gemini Gems, or used as Claude Code subagent contexts.

## When to Use This Skill

**Auto-triggers when:**
- User asks to "create a project", "build a project", "make a Claude project"
- User mentions "projector" skill explicitly
- User wants to package knowledge for any RAG-based project system

**Interview Mode triggers when:**
- User message contains "interview" keyword
- Examples: "interview me to build [name] agent", "interview me for [name] project"

**Do NOT trigger for:**
- Simple one-off questions that don't need a full project
- Existing project modifications (use direct editing instead)

## Core Workflow

### Step 0: Review Quality Examples (MANDATORY)

Before generating ANY package, read the examples in this skill's `examples/` directory:

| Example | Coverage | Key Features |
|---------|----------|--------------|
| `dry-cider-expert/` | Essential | Clean persona + regional expertise, 6 knowledge files |
| `buffett-investment-advisor/` | Deep | Persona + 17 primary source knowledge files (PDFs, research) |
| `parenting-sidekick/` | Comprehensive | system_prompt.md + 13 knowledge files, book synthesis |

Study these for:
- System prompt depth and structure
- Knowledge file organization (numbered prefixes for order)
- README format and completeness
- Tone calibration and persona definition

### Step 1: Clarification (MANDATORY)

Before creating any package, use AskUserQuestion to clarify:

**Essential questions:**
- **End user**: Who will use this Project? What's their technical level?
- **Target platform**: Claude.ai Projects, Claude Code subagent, ChatGPT, Google Gems, or multi-platform?
- **Coverage depth**: Essential, Comprehensive, or Deep? (See Fidelity Levels below)
- **Project type**: Repository-based (codebase context) or domain-based (general expertise)?
- **Persona**: What tone/personality should the agent have?
- **Core tasks**: What are the 3-5 primary use cases?
- **Existing materials**: Are there documents, codebases, books, or conversations to draw from?

Group questions thematically (2-4 per round). Don't ask obvious questions.

### Step 2: Determine Operating Mode

**Standard Mode** (default):
User provides requirements -> clarify scope -> create package immediately

**Interview Mode** (triggered by "interview" keyword):
Deep requirement gathering through systematic questioning before creating package

### Step 3: Content Extraction

#### Repository-Based Projects
When working within a codebase, extract:
- Architecture documentation and design patterns
- Code style guides and conventions
- Setup guides and development workflows
- API references and integration patterns
- Database schemas and data models
- Testing strategies and examples
- Deployment and CI/CD documentation

#### Domain-Based Projects
For general domain expertise, curate:
- Framework best practices and patterns
- Language-specific idioms and conventions
- Industry standards and guidelines
- Common anti-patterns to avoid
- Performance optimization techniques
- Security best practices

### Step 4: System Prompt Engineering

Craft a system prompt using these layers:

**Identity & Role**
- Who the agent is, their expertise, their scope boundaries
- What they know deeply vs. what's outside their domain

**Voice Calibration**
- Do/don't lists for communication style
- Tone anchors (e.g., "direct and warm", "blunt but constructive")
- Communication patterns specific to the domain

**Behavioral Guardrails**
- When to push back on the user
- How to handle uncertainty or gaps in knowledge
- Boundary conditions (what the agent refuses to do)

**Quality Framework**
- Baked-in evaluation criteria for the agent's own outputs
- Standards the agent holds itself to

**Output Format Specs**
- Default structure for responses
- Length expectations and formatting preferences

The system prompt should feel like a complete briefing document. Move detailed reference material to knowledge files; keep the prompt focused on identity, behavior, and operating rules.

### Step 5: Knowledge File Curation

For each knowledge file:
- Use clear, descriptive filenames with numbered prefixes (01_, 02_, etc.)
- Keep files focused on a single topic
- Include examples and code snippets where relevant
- Organize hierarchically (overview -> specific patterns -> edge cases)
- Ensure consistency across all files
- Format in clean, readable Markdown

**Best Practices:**
- **Single-topic focus**: Each file should cover one domain, one framework, or one reference. Don't combine unrelated topics.
- **Ideal sizing**: Aim for focused, well-organized content. A 2,000-word file that covers a topic thoroughly beats a 10,000-word file that sprawls.
- **Numbered prefixes**: Use 01_, 02_ etc. for retrieval priority. Core concepts first, specialized material later.
- **Quality over quantity**: Well-organized, focused files outperform large numbers of loosely related docs. Three excellent files beat ten mediocre ones.

### Step 6: README Generation (MANDATORY)

Every package gets a README with:
- **Description**: What this Project does and who it's for
- **Package contents**: File listing with brief descriptions
- **Setup instructions**: Platform-specific upload steps (Claude.ai, ChatGPT, etc.)
- **Example queries**: 5-8 starter prompts showing the range of use cases
- **Coverage level**: Which fidelity band this package targets
- **Disclaimers**: Where applicable (investment advice, medical info, etc.)
- **Footer**: `*Created with /projector*`

### Step 7: Generate Package

**Output all files to: `./packages/[name]/`** (relative to your workspace)

## Fidelity Levels

Coverage depth matters more than file count. Well-organized, focused content outperforms large volumes of loosely related material.

| Level | Coverage | Best For | Typical Size |
|-------|----------|----------|-------------|
| **Essential** | Core persona + key references | Broad roles, general expertise | 3-7 files |
| **Comprehensive** | Full domain coverage, multiple knowledge areas | Domain-specific depth | 8-12 files |
| **Deep** | Source materials, frameworks, specialized workflows | Hyper-specific, primary sources | 12-20+ files |

**Choosing the right level:**
- **Essential**: The agent needs a clear identity and a few reference points. Good for content strategists, coding assistants, general advisors.
- **Comprehensive**: The agent needs to synthesize across multiple sources or frameworks. Good for domain experts, book-based advisors, multi-faceted roles.
- **Deep**: The agent needs primary source materials and specialized workflows. Good for investment advisors with shareholder letters, medical references, or codebase-specific contexts.

File count is secondary guidance, not the metric. Match depth to the user's actual needs.

## Interview Mode Guidelines

### Question Quality Standards

**DO Ask** (expose hidden complexity):
- "How should the system handle X when Y is in an invalid state?"
- "What's the expected behavior if the API returns a 429 rate limit?"
- "Should this action be reversible? What's the undo strategy?"
- "How do we prioritize between performance and feature completeness?"
- "What happens when users have conflicting permissions?"
- "At what scale does this approach break down?"
- "Are there specialized workflows or modes users invoke repeatedly?" (Skills consideration)
- "Would this agent benefit from distinct sub-capabilities?" (Skills consideration)

**DON'T Ask** (too obvious):
- "What color should the button be?"
- "Do you want this to work on mobile?"
- "Should we handle errors?"

### Question Depth Strategy

**Layer 1: Clarify Ambiguity**
- Identify vague or underspecified requirements
- Surface implicit assumptions
- Define success criteria

**Layer 2: Expose Decision Points**
- Technical architecture choices
- UX pattern selection
- Data model design
- Integration approaches

**Layer 3: Explore Edge Cases**
- Error scenarios
- Performance boundaries
- State conflicts
- Race conditions

**Layer 4: Document Tradeoffs**
- Quick wins vs technical debt
- Feature richness vs simplicity
- Performance vs cost
- Flexibility vs constraints

### Interview Flow

**Phase 1: Initial Analysis** (Silent)
- Read all provided materials thoroughly
- Identify gaps, ambiguities, and decisions needed
- Categorize questions by priority
- Plan question sequence

**Phase 2: Questioning Rounds** (Interactive)
- Ask 2-4 related questions per round using AskUserQuestion
- Group questions by theme (architecture, UX, edge cases)
- Build on previous answers
- Dive deeper into uncovered complexity
- Adapt rounds based on context:
  - **High context** (lots of files): 2-3 rounds
  - **Medium context** (some materials): 4-6 rounds
  - **Low context** (minimal/no files): 6+ rounds

**Phase 3: Validation** (Confirmatory)
- Summarize understanding
- Confirm critical decisions
- Verify edge case handling
- Check for remaining gaps

**Phase 4: Completion** (Create Package)
- Synthesize all gathered information
- Create comprehensive package
- Include: requirements, decisions, tradeoffs, edge cases

### Interview Exit Criteria

Complete the interview when:
- All architectural decisions are documented
- Edge cases and error scenarios are defined
- Technical approach is clear and specific
- Tradeoffs and limitations are acknowledged
- User confirms "ready to build" confidence
- No remaining "how would we..." questions

**Exit prompt**: "I have a clear picture of the requirements. Ready for me to create the Project package, or are there other aspects we should explore?"

**Handling Uncertainty:**
If concerns persist:
"I can create the Project package now, but I want to flag that [X] is still somewhat ambiguous. We could:
A) Document it as an open question to resolve during implementation
B) Spend a few more minutes clarifying it now
C) Create the package and revisit this specific point later

What's your preference?"

## Output Format

All packages are written to `./packages/[name]/` with this structure:

```
[name]/
├── README.md              # Package overview, usage guide, contents
├── system_prompt.md       # Role definition, personality, scope, guidelines
└── knowledge/
    ├── 01_[topic].md      # Numbered for reading order
    ├── 02_[topic].md
    └── ...
```

**Optional skills directory** (for complex agents with specialized workflows):
```
[name]/
├── README.md
├── system_prompt.md
├── knowledge/
│   └── ...
└── skills/
    ├── skill-name-1.md
    └── skill-name-2.md
```

Skills are valuable when:
- The agent needs repeatable, structured workflows for specific tasks
- There are multiple specialized modes or operations within the agent's domain
- Users benefit from invoking targeted capabilities (e.g., "run the tax-optimizer skill")
- The project has distinct sub-capabilities that warrant their own instructions

## Quality Checklist

Before delivering, verify:
- [ ] Reviewed examples in this skill's `examples/` directory for quality bar
- [ ] Asked clarifying questions before generating
- [ ] System prompt uses layered structure (identity, voice, guardrails, quality, format)
- [ ] Knowledge files cover all essential topics with single-topic focus
- [ ] Examples are accurate and current
- [ ] No redundancy between files
- [ ] Files are properly named with numbered prefixes
- [ ] Markdown formatting is clean and consistent
- [ ] README includes setup instructions, example queries, and package contents
- [ ] Package written to `./packages/[name]/`
- [ ] Coverage depth matches the stated fidelity level
- [ ] Footer reads `*Created with /projector*`

## Examples

Reference implementations in this skill's `examples/` directory:

### dry-cider-expert (Essential)
- **Persona**: Direct and warm mentor, builder-first mentality
- **Structure**: system_prompt.md + 6 knowledge files
- **Features**: Fermentation science, regional sourcing, equipment guides, legal reference
- **Use as reference for**: Clean Essential packages, regional expertise, hobby domains

### buffett-investment-advisor (Deep)
- **Persona**: Warren Buffett channeling Charlie Munger's intellectual rigor
- **Structure**: system_prompt.md + QUICK_START.md + 17 knowledge files (PDFs, research papers, shareholder letters)
- **Features**: Investment frameworks, mental models, primary source materials spanning 50+ years
- **Use as reference for**: Deep packages with primary sources, persona-heavy advisors

### parenting-sidekick (Comprehensive)
- **Persona**: Practical, grounded, supportive with strong backbone
- **Structure**: system_prompt.md + 13 knowledge files
- **Features**: Book-based frameworks, age-specific guides, in-the-moment toolkit, medical reference
- **Use as reference for**: Comprehensive book synthesis, multi-framework integration, practical toolkits

## Troubleshooting

### Package too generic
- Increase coverage depth
- Ask more specific questions in interview mode
- Add more knowledge files with concrete examples
- Include actual user content/voice samples

### System prompt too long
- Move detailed information to knowledge files
- System prompt should be identity + voice + behavioral guardrails
- Details, frameworks, and examples go in knowledge files

### Knowledge files overlapping
- Each file should have single focus
- Use numbered prefixes to show hierarchy
- Merge related content, split overloaded files

### Missing user context
- Run interview mode for deeper discovery
- Ask about specific use cases and scenarios
- Request examples of desired outputs
- Probe for edge cases and error handling

## Best Practices

- **Be comprehensive but focused**: Include everything necessary, nothing superfluous
- **Prioritize practical examples**: Show, don't just tell
- **Maintain consistency**: Use consistent terminology and formatting across all files
- **Version awareness**: Note framework/language versions when relevant
- **Test mentally**: Ask yourself "Could Claude effectively help with X using these files?"
