---
name: codex
description: "Get an independent second opinion from OpenAI Codex while Claude Code (or another agent) is driving. Three read-only modes: review (diff review with a pass/fail gate), challenge (adversarial, tries to break the code), consult (ask anything). Use on \"codex review\", \"codex challenge\", \"ask codex\", \"consult codex\", or \"second opinion\". Requires the codex CLI."
argument-hint: "review [instructions] | challenge [focus] | <question>"
---

# /codex — Second Opinion via OpenAI Codex

Wraps the `codex` CLI to get an independent second opinion from a different AI system. Present Codex output verbatim — do not summarize or truncate.

## Step 0: Preflight

Verify `codex` is reachable before running any mode:

```bash
codex --help 2>&1 | tail -5
```

Allow about 95 seconds for this call (in Claude Code, `timeout: 95000` on the Bash call).

If output contains `Error` or `login` or no commands listed, stop and tell the user:
> "Codex setup incomplete. Run `codex login` interactively to authenticate, then retry `/codex`."

## Step 1: Detect mode

Parse the user's input:

1. `/codex review` or `/codex review <instructions>` → **Review mode**
2. `/codex challenge` or `/codex challenge <focus>` → **Challenge mode**
3. `/codex <prompt>` → **Consult mode**
4. `/codex` alone → auto-detect:
   - Check for a diff:
     ```bash
     git diff --quiet "origin/$BASE...HEAD" 2>/dev/null && echo "NO_DIFF" || echo "HAS_DIFF"
     ```
   - If `HAS_DIFF`, ask the user to pick one of three options (with AskUserQuestion where the host has it): review the diff / challenge the diff / something else (provide prompt).
   - If `NO_DIFF`, ask what to consult about.

Detect the base branch:

```bash
BASE=$(gh pr view --json baseRefName -q .baseRefName 2>/dev/null \
  || git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' \
  || echo "main")
echo "BASE: $BASE"
```

## Step 2A: Review Mode

Run Codex code review against the current branch diff.

```bash
codex review --base "$BASE" 2>&1
```

Allow five minutes (in Claude Code, `timeout: 300000` on the Bash call).

If the user provided custom instructions (e.g., `/codex review focus on security`):

```bash
codex review "focus on security" --base "$BASE" 2>&1
```

Parse the output for severity markers:
- `[P0]` or `[P1]` or `critical` or `high` → gate **FAIL**
- None of the above → gate **PASS**
- Empty output or setup noise → gate **UNKNOWN**

Present:

```
CODEX SAYS (code review):
════════════════════════════════════════
<full codex output, verbatim>
════════════════════════════════════════
GATE: PASS / FAIL (N critical findings) / UNKNOWN (no model output)
```

## Step 2B: Challenge Mode

Adversarial mode — Codex tries to break your code.

Default prompt (no focus):

```
Review the changes on this branch against the base branch. Run
git diff origin/$BASE to see the diff. Your job is to find ways
this code will fail in production. Think like an attacker and a
chaos engineer. Find edge cases, race conditions, security holes,
resource leaks, failure modes. Be adversarial. Be thorough. No
compliments — just the problems.
```

With focus (e.g., "security"):

```
Review the changes on this branch. Run git diff origin/$BASE.
Focus specifically on SECURITY. Find every way an attacker could
exploit this code. Be adversarial.
```

Run:

```bash
codex exec "<prompt>" -s read-only 2>&1
```

Present:

```
CODEX SAYS (adversarial challenge):
════════════════════════════════════════
<full output, verbatim>
════════════════════════════════════════
```

## Step 2C: Consult Mode

Ask Codex anything about the codebase.

```bash
codex exec "<user's prompt>" -s read-only 2>&1
```

Present:

```
CODEX SAYS (consult):
════════════════════════════════════════
<full output, verbatim>
════════════════════════════════════════
```

After presenting, note any points where you disagree with Codex:
> "Note: I disagree on X because Y."

## Rules

- **Present output verbatim.** Never truncate or summarize Codex's response before showing it. If output exceeds reasonable length, save full output to a temp file and show the tail + file path.
- **5-minute timeout** on all `codex review` / `codex exec` Bash calls (`timeout: 300000`).
- **Read-only.** `codex exec` runs with `-s read-only`. The `review` subcommand is inherently read-only.
- **Add synthesis after, not instead of.** Any Claude commentary comes after the full Codex output.
- **Auth failures.** If codex hangs on setup or prints auth errors, stop and tell the user to run `codex login` interactively first.
