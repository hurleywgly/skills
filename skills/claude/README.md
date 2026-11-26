# Claude

From Codex or another agent, bring in Claude Code as a teammate: review, challenge, consult, or a bounded delegated task. Runs on the Claude CLI's default model on your subscription and stops before any API-key spend.

## Use

```
/claude review [instructions] | challenge [focus] | delegate <task> | <question> [model effort fast ultracode]
```

## Requirements

The `claude` CLI, logged in with a subscription, and `jq`.

## Install

Copy this folder into your agent's skills directory (for example `~/.claude/skills/claude` or `~/.agents/skills/claude`). `SKILL.md` is the skill; `agents/openai.yaml` carries the Codex display name and invocation policy.

## License

MIT. See `LICENSE`.
