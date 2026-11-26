# Codex

From Claude Code, get a read-only second opinion from OpenAI Codex: consult, review, or challenge. Runs on the Codex CLI's default model on your ChatGPT subscription and never uses an API key.

## Use

```
/codex review [focus] | challenge <target> | <question> [model] [effort]
```

## Requirements

The `codex` CLI logged in with ChatGPT, and `jq`.

## Install

Copy this folder into your agent's skills directory (for example `~/.claude/skills/codex` or `~/.agents/skills/codex`). `SKILL.md` is the skill; `agents/openai.yaml` carries the Codex display name and invocation policy.

## License

MIT. See `LICENSE`.
