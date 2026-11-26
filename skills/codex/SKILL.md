---
name: codex
description: "Get an independent, read-only second opinion from OpenAI Codex while Claude Code is driving, through the local ChatGPT-authenticated Codex CLI bridge. Three modes: consult (ask anything), review (findings-first diff review), challenge (adversarial failure analysis). Runs on the Codex CLI's own default model unless the user names one (astra, sol, terra, luna, or an exact slug) and an effort. Use on \"codex review\", \"codex challenge\", \"ask codex\", \"consult codex\", \"second opinion\", or a named configuration such as \"Sol high\". Bills the ChatGPT subscription only; never uses an API key or grants write authority."
argument-hint: "review [focus] | challenge <target> | <question> [model] [effort]"
---

# /codex - Subscription-backed Codex teammate

Use the installed bridge to ask Codex for an independent read-only opinion. Show Codex output verbatim before adding Claude commentary.

## Boundary

- This is a one-way Claude Code -> Codex CLI bridge.
- It does not add Claude models to the Codex model selector.
- It accepts ChatGPT-authenticated Codex only; no API key, base URL, proxy, Azure, Bedrock, local, or gateway provider.
- It is read-only, ephemeral, and single-project.
- It never invokes Claude or another agent from inside Codex.
- It does not implement, edit, commit, push, deploy, publish, purchase, or send external messages.

## Which model

Run on the Codex CLI's own default model: pass no `--model`. The CLI's default is what its maker currently recommends, and it moves forward without this file being edited. Pass no `--effort` either; the bridge then uses medium, which is enough reasoning for a useful review without spending the plan's usage on every question.

Use a different model or effort only when the user asks for one in this request, by alias or exact slug ("use Sol", "Astra at high", "gpt-... xhigh"). A harder question is not, by itself, a reason to upgrade; if you think a stronger model or more reasoning effort would change the answer, say so and let the user choose. When they name one, that exact pin holds: never substitute another model or effort.

The bridge owns the model facts so they live in one place:

- `"$CODEX_BRIDGE" --help` lists the aliases it accepts (`astra`, `sol`, `terra`, `luna`).
- `codex debug models --bundled` is the catalog. Any slug in it can be passed as `--model`; the bridge rejects anything that is not there, and any effort the model does not support.

Stronger models and higher efforts use up the ChatGPT plan's included usage faster. Do not enable the Fast/priority service tier for the same reason.

## Spend guardrail

Every call must be covered by the user's ChatGPT subscription. The bridge enforces the route: it strips API-key and provider variables from the child process and stops unless `codex login status` reports a ChatGPT login.

If a call would be billed any other way, stop before running it and tell the user what would be charged and to what:

- The bridge reports that Codex is not logged in through ChatGPT.
- The only way to get the requested model is an API key or another provider.
- The user has said they need zero incremental charge and the plan's included usage may be exhausted (ChatGPT can fall through to purchased credits or auto top-up). Ask them to check Codex Settings > Usage first.

Do not work around a stop by adding a key, a provider, or a different tool.

## Preflight

```bash
CODEX_BRIDGE="<this skill's folder>/bin/codex-subscription-bridge"   # e.g. "$HOME/.claude/skills/codex/bin/codex-subscription-bridge"
test -x "$CODEX_BRIDGE"
```

If it is absent or not executable, stop. Do not recreate it inline.

Run a zero-inference route check when the environment or login has changed, or before the first call with a named model:

```bash
"$CODEX_BRIDGE" --preflight --cwd "$PWD"                 # default route
"$CODEX_BRIDGE" --preflight --model sol --effort high --cwd "$PWD"
```

It verifies that `codex` and `jq` exist, that the login is ChatGPT, and, for a named model, that the model and effort are in the catalog.

`--cwd` can be any folder; it does not have to be a git repository. Review mode still needs one, since it reviews a diff.

## Modes

Add `--model <name>` and `--effort <level>` to any of these only when the user named them.

### Consult

An independent answer.

```bash
PROMPT='<exact user question plus only the context Codex needs>'
printf '%s' "$PROMPT" | "$CODEX_BRIDGE" --mode consult --cwd "$PWD"
```

### Review

Findings-first code review.

```bash
PROMPT='Prioritize bugs, regressions, and missing tests. Findings first.'
printf '%s' "$PROMPT" | "$CODEX_BRIDGE" --mode review --cwd "$PWD" --uncommitted     # uncommitted work
printf '%s' "$PROMPT" | "$CODEX_BRIDGE" --mode review --cwd "$PWD" --base main        # branch diff
```

### Challenge

Adversarial failure analysis.

```bash
PROMPT='<system or change to stress-test>'
printf '%s' "$PROMPT" | "$CODEX_BRIDGE" --mode challenge --cwd "$PWD"
```

## From sub-agents and workflows

The bridge is headless-safe, so a sub-agent or workflow step can call it, for example to put the same question to two models. Use one bridge call per agent and hand the agent the fully assembled command so it does not rebuild flags. Have it return the `ROUTE USED` line and the complete output verbatim. Warnings printed before the answer (MCP sign-in notices, skill-load or model-cache warnings) are normal in headless runs and are not a failure.

## Presentation

The bridge prints `ROUTE USED: <model> @ <effort>` from Codex's own banner. Report that, not what you assumed.

```text
CODEX ROUTE: <model> @ <effort> (from ROUTE USED), ChatGPT auth, read-only, ephemeral
CODEX SAYS:
<complete bridge output verbatim>
CLAUDE NOTES:
<optional agreement, disagreement, or next action>
```

Do not summarize Codex before showing it. If the output is too long, preserve the full raw output in a temporary file and label any excerpt.

## Failure behavior

Stop without fallback when:

- ChatGPT authentication is absent
- a named model is unavailable, or the banner does not match the named model or effort
- the bridge reports a write or approval attempt
- the billing boundary cannot be verified to the user's requirement
- another independent `codex` skill copy creates ambiguous discovery

A failure is information for the user, not something to route around with an API key, another provider, the Fast tier, a broader sandbox, a writable directory, or a bypass flag.
