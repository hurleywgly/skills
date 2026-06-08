---
name: claude
description: Claude Code second opinion for Codex. Three modes — review (diff review with pass/fail gate), challenge (adversarial break-your-code), consult (ask anything). Trigger on "claude review", "claude challenge", "ask claude", "second opinion from Claude", "consult Claude".
---

# /claude — Second Opinion via Claude Code

Wraps the `claude` CLI to get an independent second opinion from Claude while Codex is driving the session. Present Claude output verbatim — do not summarize or truncate.

This is the mirror of `/codex`.

## Step 0: Preflight

Verify `claude` is reachable before running any mode:

```bash
claude --help
```

If output contains auth/setup errors or the command is missing, stop and tell the user:
> "Claude setup incomplete. Run `claude auth` interactively to authenticate, then retry `/claude`."

## Step 0.5: Context Brief

Every invocation should prepend this brief to the Claude prompt. Keep it tight; Claude may also load repo-local `CLAUDE.md` automatically.

```text
You are being invoked as the independent second opinion in a Codex-first workflow. Your output will be shown verbatim to the user; Codex may add disagreement notes after, but should not summarize or filter you.

The workspace may be markdown-heavy and often has many generated or untracked files; do not flag noise from generated or untracked files unless it directly affects the requested task. Real code review usually happens in the project source directories.

What the user wants from you:
- No compliments and no generic summary of what the code does.
- Disagree freely with Codex or prior framing when the evidence supports it.
- Use severity markers like [P0], [P1], critical, or high only when they should mechanically fail the gate.
- Be specific: cite files, lines, commands, failure modes, and exact assumptions.
- If the prompt is malformed, the diff is empty, or the scope is too broad, say so directly.

Noise to avoid:
- Praise for structure.
- Generic best-practice reminders unrelated to the diff.
- "Add tests" without naming the behavior that is untested.
- Complaints about untracked generated files.

Your last paragraph is high-value if output is truncated later, so make it a conclusion or the most important finding.
```

## Step 1: Detect Mode

Parse the user's input:

1. `/claude review` or `/claude review <instructions>` -> **Review mode**
2. `/claude challenge` or `/claude challenge <focus>` -> **Challenge mode**
3. `/claude <prompt>` -> **Consult mode**
4. `/claude` alone -> auto-detect:
   - Check for a diff:
     ```bash
     git diff --quiet "origin/$BASE...HEAD" 2>/dev/null && echo "NO_DIFF" || echo "HAS_DIFF"
     ```
   - If `HAS_DIFF`, ask whether to review the diff, challenge the diff, or consult about something else.
   - If `NO_DIFF`, ask what to consult about.

Detect the base branch:

```bash
BASE=$(gh pr view --json baseRefName -q .baseRefName 2>/dev/null \
  || git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' \
  || echo "main")
echo "BASE: $BASE"
```

## Step 2A: Review Mode

Run Claude as a read-oriented reviewer against the current branch diff. Prefer `claude -p` over interactive mode.

Prompt shape:

```text
<context brief>

Review the changes on this branch against origin/$BASE. Inspect the diff with git as needed.

Focus: <custom instructions, or "find correctness, security, data-loss, race-condition, migration, and UX regressions">

Return findings first, ordered by severity, with file/line references where possible. No compliments. No summary preamble.
```

Command shape:

```bash
claude -p "<prompt>" \
  --permission-mode dontAsk \
  --allowedTools "Read,Grep,Glob,Bash(git diff:*),Bash(git status:*),Bash(git log:*),Bash(git show:*),Bash(git branch:*),Bash(git rev-parse:*),Bash(gh pr view:*)" \
  --disallowedTools "Edit,MultiEdit,Write,NotebookEdit" \
  2>&1
```

If constrained tool patterns are rejected by the installed Claude CLI, retry with:

```bash
claude -p "<prompt>" \
  --permission-mode dontAsk \
  --tools "Read,Grep,Glob,Bash" \
  --disallowedTools "Edit,MultiEdit,Write,NotebookEdit" \
  2>&1
```

Parse the output for severity markers:
- `[P0]` or `[P1]` or `critical` or `high` -> gate **FAIL**
- None of the above -> gate **PASS**
- Empty output or setup noise -> gate **UNKNOWN**

Present:

```text
CLAUDE SAYS (code review):
════════════════════════════════════════
<full claude output, verbatim>
════════════════════════════════════════
GATE: PASS / FAIL (N critical findings) / UNKNOWN (no model output)
```

## Step 2B: Challenge Mode

Adversarial mode — Claude tries to break the code or plan.

Default prompt:

```text
<context brief>

Review the changes on this branch against origin/$BASE. Run git diff as needed. Your job is to find ways this code will fail in production. Think like an attacker and a chaos engineer. Find edge cases, race conditions, security holes, resource leaks, data loss, migration traps, and ambiguous product behavior. Be adversarial. No compliments — just the problems.
```

With focus:

```text
<context brief>

Review the changes on this branch against origin/$BASE. Focus specifically on <FOCUS>. Find every way this could fail. Be adversarial. No compliments.
```

Run with the same `claude -p` command shape as review mode.

Present:

```text
CLAUDE SAYS (adversarial challenge):
════════════════════════════════════════
<full output, verbatim>
════════════════════════════════════════
```

## Step 2C: Consult Mode

Ask Claude anything about the codebase, plan, or workspace state.

Prompt shape:

```text
<context brief>

Question from the user via Codex:
<user prompt>

Answer directly. If the question requires inspecting local files, inspect them. If the available context is insufficient, say exactly what is missing.
```

Run:

```bash
claude -p "<prompt>" \
  --permission-mode dontAsk \
  --allowedTools "Read,Grep,Glob,Bash(git diff:*),Bash(git status:*),Bash(git log:*),Bash(git show:*),Bash(find:*),Bash(rg:*)" \
  --disallowedTools "Edit,MultiEdit,Write,NotebookEdit" \
  2>&1
```

Present:

```text
CLAUDE SAYS (consult):
════════════════════════════════════════
<full output, verbatim>
════════════════════════════════════════
```

After presenting, add Codex disagreement notes only when useful:
> "Note: I disagree on X because Y."

## Rules

- **Present output verbatim.** Never summarize Claude's response before showing it. If output exceeds reasonable length, save full output to a temp file and show the tail plus file path.
- **Read-oriented.** Use `claude -p` with write tools disallowed. Do not let the second-opinion call edit files.
- **Use repo context.** Do not pass `--bare` by default; repo-local `CLAUDE.md` is useful context.
- **Add synthesis after, not instead of.** Codex commentary comes after the full Claude output.
- **Auth failures.** If Claude hangs on setup or prints auth errors, stop and tell the user to run `claude auth` interactively first.
- **Keep severity meaningful.** `[P0]`, `[P1]`, `critical`, and `high` affect the review gate.
