---
name: claude
description: "Bring in Claude Code as a teammate while Codex (or another agent) is driving. Read-only by default: review (diff review with a pass/fail gate), challenge (adversarial, tries to break the code or plan), consult (ask anything); plus explicit, bounded delegated execution. Runs on the Claude CLI's own default model on the user's subscription unless the user names a model, effort, Fast mode, or Ultracode, and stops to ask before any call that would bill an API key. Use on \"claude review\", \"claude challenge\", \"ask claude\", \"second opinion from Claude\", \"consult Claude\", \"delegate to Claude\", \"Claude teammate\", or requests naming a Claude configuration such as \"Opus high\", \"Opus high fast\", \"Fable ultracode\", or \"Sonnet medium\". Requires the claude CLI."
argument-hint: "review [instructions] | challenge [focus] | delegate <task> | <question> [model effort fast ultracode]"
---

# /claude — Claude Code Teammates for Codex

Use the installed `claude` CLI as a teammate inside a Codex-led workflow. Default to read-only second-opinion work. Enter delegated execution only when the user explicitly asks Claude to implement, execute, or own a bounded task.

Present Claude's answer verbatim. Add Codex synthesis only after Claude's complete output.

## 0. Preflight

Run:

```bash
claude --version
claude --help
claude auth status
```

The flags this skill uses (`--effort`, including `ultracode`, `--settings`, `--setting-sources`, `--max-budget-usd`) must appear in `claude --help` for the installed version. If one is missing, say which and stop; do not guess at an older syntax.

If `claude auth status` is nonzero, reports `"loggedIn": false`, or a smoke call returns an OAuth/authentication error, stop:

> Claude setup incomplete. Run `claude auth login` interactively, then retry `/claude`.

Do not treat `claude --help` succeeding as proof that inference is authenticated.

### Spend guardrail

Before any inference, read `authMethod` in the `claude auth status` output. Calls must run on the user's Claude subscription.

An API key in the environment takes precedence over a subscription login in headless calls, so a machine can be logged in with a subscription and still bill the key. To keep calls on the subscription, run every `claude` command in this skill with the key variables removed from the child process:

```bash
CLAUDE_ENV=(env -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN)
"${CLAUDE_ENV[@]}" claude auth status
```

Read that output. Proceed only when `authMethod` is `claude.ai` (a `subscriptionType` is shown) and no `apiKeySource` line appears.

If the CLI is not logged in once the key is removed, the only way to run would be the API key, billed per token. Stop before running anything and tell the user:

> This Claude call would bill the Anthropic API key, not a subscription. Options: log the CLI in with your subscription (`claude auth login`), or tell me to go ahead on the API key and give a spending cap.

Go ahead on an API key only after the user says so in this conversation, and then pass `--max-budget-usd` with the cap they gave.

The JSON result carries a `total_cost_usd` figure even on a subscription. It is an estimate of what the call would have cost at API rates, not a charge, but it does show how much of the plan's usage a call consumed; report it.

## 1. Select the Teammate Configuration

### Default: let the CLI choose

Pass no `--model` and no `--effort`. The Claude CLI's own default is what its maker currently recommends and what the user's plan is set up for, and it stays current without this file being edited.

Use something else only when the user asks for it in this request. A harder task is not, by itself, a reason to upgrade; if you think a stronger model would change the answer, say so and let the user choose, because stronger models, higher effort, Fast and Ultracode all cost more.

Parse what they named, from flags or natural language:

- `--model <name>` or "using Fable"
- `--effort <level>` or "at medium" (levels are listed in `claude --help`)
- `--fast` / `--standard`
- `--fallback-model <models>` only when the user explicitly permits fallback
- `--subagent-model <model>` only when workflow workers should differ from the lead

Model names are not listed here because they change with each release. When the user names a family ("opus", "sonnet", "fable"), pass that alias; aliases float to the latest model in the family. When they name a version, pass the full model ID exactly as they gave it; if you are unsure of the ID, ask rather than construct one.

### Keep the four controls distinct

- **Model** chooses the model.
- **Effort** chooses adaptive reasoning depth.
- **Fast** is a lower-latency, higher-cost configuration that only some models support, and which ones changes between releases. Never assume: request it, then check `fast_mode_state` in the result (section 6). If it comes back off, say so and do not present the run as Fast.
- **Ultracode** is workflow orchestration, not a model. `--effort ultracode` runs the lead at high effort and lets Claude create dynamic workflows across many subagents.

The word `ultracode` inside a `claude -p` prompt does not trigger a workflow. In headless calls, pass `--effort ultracode`.

### When the user names an exact model

A named model is an exact pin:

1. Pass the full `--model` ID.
2. Pass the requested `--effort`.
3. Set per-run settings with an empty fallback chain.
4. Set `CLAUDE_CODE_NO_MODEL_FALLBACK=1`.
5. Set `CLAUDE_CODE_DISABLE_ADVISOR_TOOL=1` unless the user explicitly requests a mixed-model advisor.
6. For Ultracode or other subagent work, set `CLAUDE_CODE_SUBAGENT_MODEL` to the same exact ID unless the user requests mixed routing.
7. Verify the requested primary model appears in `modelUsage`. A wrong-model result does not satisfy the task.

Use:

```bash
CLAUDE_SETTINGS='{"fastMode":false,"fallbackModel":[]}'
```

For a Fast run:

```bash
CLAUDE_SETTINGS='{"fastMode":true,"fallbackModel":[]}'
```

Passing `fastMode` through `--settings` makes it session-local in `-p` mode and does not change the user's saved default. Always pass `fastMode: false` for standard-speed calls so another session's persistent preference cannot leak in.

Only omit `CLAUDE_CODE_NO_MODEL_FALLBACK` and add `--fallback-model` when the user explicitly authorizes fallback. Remember that a safety fallback is also model substitution; an exact pin should fail closed rather than silently become another model.

## 2. Detect Mode

1. `/claude review [focus]` → **review**, read-only
2. `/claude challenge [focus]` → **challenge**, read-only
3. `/claude consult <question>` or `/claude <question>` → **consult**, read-only
4. `/claude delegate <task>` or `/claude execute <task>` → **delegate**, writable and explicit
5. `/claude` alone → inspect for a diff, then ask the user which mode to use

Never infer delegate mode from a question about capability, a request for a plan, or the presence of an implementation task in repository state.

Detect the review base:

```bash
BASE=$(gh pr view --json baseRefName -q .baseRefName 2>/dev/null \
  || git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' \
  || echo "main")
```

## 3. Context Brief

Prepend this to every prompt:

```text
You are a Claude Code teammate in a Codex-led workflow. Your output will be shown verbatim to the user. Codex may add disagreement notes afterward but will not summarize or filter you.

Follow the repository's AGENTS.md/CLAUDE.md and stay inside the task's write scope.

Be direct. No praise or generic summary. Disagree when evidence supports it. Cite files, lines, commands, failure modes, and assumptions. If the prompt, diff, scope, or evidence is insufficient, state exactly what is missing. End with the conclusion or most important finding.
```

For delegated execution, append:

```text
You own this bounded task. Inspect before editing, stay within the stated write scope, run proportionate verification, and report changed files plus test results. Do not commit, push, open a PR, deploy, publish, message anyone, or alter external state unless the user explicitly authorized that action.
```

## 4. Invocation Contract

Run from the target repository. Use `--setting-sources project` so project settings and instructions apply without inheriting the user's broad user/local permission allowlists.

Capture JSON so routing can be verified while Claude's textual answer remains verbatim. This is the fully pinned form; on the default route, drop `--model`, `--effort`, `CLAUDE_CODE_SUBAGENT_MODEL` and `CLAUDE_CODE_NO_MODEL_FALLBACK`, and keep everything else:

```bash
CLAUDE_JSON=$(
  printf '%s' "$PROMPT" | \
  "${CLAUDE_ENV[@]}" \
  CLAUDE_CODE_NO_MODEL_FALLBACK=1 \
  CLAUDE_CODE_DISABLE_ADVISOR_TOOL=1 \
  CLAUDE_CODE_SUBAGENT_MODEL="$CLAUDE_MODEL" \
  claude -p \
    --model "$CLAUDE_MODEL" \
    --effort "$CLAUDE_EFFORT" \
    --settings "$CLAUDE_SETTINGS" \
    --setting-sources project \
    --output-format json \
    <mode-specific permission flags>
)
```

Send the prompt on stdin, as shown. The tool flags take a list, so a prompt placed after them as a trailing argument is read as one more tool name and the CLI exits with "Input must be provided". Keep stderr separate from `CLAUDE_JSON`; merging it with `2>&1` can make the JSON unparsable. Surface any stderr warning alongside routing metadata.

Do not set `CLAUDE_CODE_SUBAGENT_MODEL` when the user explicitly requests a different worker model. Do not set `CLAUDE_CODE_NO_MODEL_FALLBACK` when the user explicitly supplies a fallback chain.

Claude Code may record a small Haiku auxiliary call for harness work even when the requested primary model and every task subagent are exactly pinned. Treat `claude-haiku-*` in `modelUsage` as auxiliary metadata, not evidence of fallback. `CLAUDE_CODE_NO_MODEL_FALLBACK=1` is the fail-closed substitution guard; the requested primary model must still appear.

On an approved API-key run, always pass `--max-budget-usd` (see the spend guardrail). Ultracode can spawn dozens to hundreds of agents; use it only when requested or clearly named.

### Read-only permission flags

Use for review, challenge, and consult:

```bash
--permission-mode dontAsk \
--tools "Read,Grep,Glob,Bash" \
--allowedTools "Read,Grep,Glob,Bash(git diff *),Bash(git status *),Bash(git log *),Bash(git show *),Bash(git branch *),Bash(git rev-parse *),Bash(gh pr view *),Bash(find *),Bash(rg *)" \
--disallowedTools "Edit,MultiEdit,Write,NotebookEdit"
```

Keep the prompt explicitly read-only. If Ultracode is used in a read-only mode, retain the write-tool denials for every workflow worker.

### Delegate permission flags

Delegate mode requires an explicit target repository and write scope. Use:

```bash
--permission-mode auto
```

Do not use `--dangerously-skip-permissions`. Add narrow `--allowedTools` rules only for commands the bounded task requires. For concurrent Codex/Claude work, use `--worktree <name>` or otherwise partition file ownership before dispatch so teammates cannot overwrite each other.

## 5. Mode Prompts

### Review

```text
<context brief>

Review this branch against origin/<BASE>. Inspect the diff with git.
Focus: <custom focus, or correctness, security, data loss, races, migrations, and UX regressions>.

Return findings first, ordered by severity, with file and line references. No compliments or summary preamble. Do not edit files.
```

Gate the response:

- `[P0]`, `[P1]`, `critical`, or `high` → **FAIL**
- none → **PASS**
- empty output, auth/setup noise, or routing mismatch → **UNKNOWN**

### Challenge

```text
<context brief>

Review this branch against origin/<BASE>. Find every realistic way it can fail in production, especially <focus if supplied>. Think like an attacker and chaos engineer. Look for edge cases, races, security holes, resource leaks, data loss, migration traps, and ambiguous product behavior. No compliments. Do not edit files.
```

### Consult

```text
<context brief>

Question from the user via Codex:
<question>

Answer directly. Inspect local files when needed. Do not edit files. If evidence is insufficient, state exactly what is missing.
```

### Delegate

```text
<context brief>
<delegated-execution brief>

Task:
<outcome>

Write scope:
<exact paths or modules>

Constraints:
<tests, boundaries, forbidden actions, and completion condition>
```

If model routing itself is part of the authorization boundary, do not let Claude select a different model for a workflow stage.

## 6. Verify and Present

Treat the JSON envelope as harness metadata, not Claude's answer.

Check:

```bash
printf '%s' "$CLAUDE_JSON" | jq -r '.modelUsage | keys[]?'
printf '%s' "$CLAUDE_JSON" | jq '{fast_mode_state, speed: .usage.speed}'
printf '%s' "$CLAUDE_JSON" | jq -r '.result // empty'
```

Fail routing when:

- a model was named and that exact model is absent from `modelUsage` (on the default route, report whichever model `modelUsage` shows)
- an unapproved non-Haiku peer model appears without an explicitly mixed-model route
- Fast was requested and `fast_mode_state` is not `on`
- `.is_error` is true, `.terminal_reason` is an API/setup error, or model output is empty

Use `fast_mode_state` as the Fast-mode ground truth. Aggregate `.usage.speed` can remain `standard` when the run includes auxiliary standard-speed work even though the primary request ran with Fast enabled.

An organization may clamp effort. Plain-text Claude runs warn when requested effort is reduced, while JSON can apply the clamp silently. If exact effort is authorization-critical, run a minimal plain-text preflight with the same model and effort and reject any clamp warning before the real task.

Present:

```text
CLAUDE SAYS (<mode> — <CLI default | requested <model> @ <effort>>, <standard|fast>, <single-agent|ultracode>):
════════════════════════════════════════
<.result exactly as returned; no summary or truncation>
════════════════════════════════════════
ROUTING: PASS — primary: <model from modelUsage>; auxiliary: <other modelUsage keys or none>; fast mode: <fast_mode_state>; billing: <subscription | API key, approved cap $N>
GATE: <review mode only>
```

On mismatch, use `ROUTING: FAIL`, show the actual metadata and Claude result verbatim, and do not present the work as satisfying the requested teammate configuration.

## Rules

- Preserve Claude's output verbatim; synthesis comes after it.
- Default to the CLI's own model on the subscription; a named model is an opt-in and then an exact pin unless the user says “latest” or explicitly permits fallback.
- Stop and ask before any call that would bill an API key.
- Read-only is the default. Delegate mode must be explicit and bounded.
- Fast is session-local and only valid where `fast_mode_state` confirms it.
- Ultracode is expensive orchestration, not decorative wording.
- Never claim a route worked from flags alone; verify the returned metadata.
- Never claim the skill is end-to-end ready while Claude authentication is unhealthy.
