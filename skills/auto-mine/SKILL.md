---
name: auto-mine
description: "Run the mine skill unattended to a budget (the overnight gear): admission-gated, read-only, needs explicit user authorization, and parks a morning bundle for review instead of deciding anything. Requires the mine skill to be installed. For a watched run use mine directly."
argument-hint: "<what to find and where>"
disable-model-invocation: true
---

# /auto-mine

> thin autonomous envelope over `/mine` — runs the loop unattended to a budget, read-only, and parks a morning bundle for review

## What this is

`/auto-mine` wraps the `/mine` core (the engine — cycle, T/S/B scoring, keep/discard, capsule output — single source of truth, untouched) in the autonomous envelope. It runs `/mine` unattended to a declared budget while you sleep, then parks at `awaiting_human` and emits a morning bundle to judge. It is **not** the stretch gear — `/mine stretch` is a longer gated turn that hands back to you at the boundary. This is the overnight gear: admission-gated, authorization-backed, parks with a digest.

## Invocation

`/auto-mine [args]` — same `[args]` as `/mine` (a source + optional mission). This is the overnight / unattended gear; for a watched run use `/mine`, for a long gated turn use `/mine stretch`.

## Admission

Run the admission check at start: confirm the metric is grounded, the budget is bounded, the surface is read-only, and the morning artifact is defined. Any failure → PARK immediately with the reason in the run-log; never run gated-silent. Filled admission block for this core:

```yaml
admission:
  metric:
    name: yield_pct                       # kept / extracted, per the core's keep>=2 rule
    grounding: rubric+authorization            # self-graded T/S/B rubric + standing per-loop authorization
    threshold: ">= 2 of 3 (T/S/B) to KEEP"
    authorization: "kanban: ⚡ Autonomous lane on a task board | or a direct go"
    rubric: "the mine skill's SKILL.md, Scoring section"
  budget:                                  # resource-aware — no hard clock/cycle cap
    allocation: resource-aware             # allocate to available tokens/compute + corpus breadth
    stop: convergence-or-envelope-exhausted   # /mine's 3-consecutive-low-yield convergence is the natural stop
    max_subagents: 0                        # /mine does not fan out
    max_cost_usd: null                      # token-metered
  surface:
    mode: read-only                         # automatic — /mine is read-only by nature (Safety Rule 1)
  morning_artifact:
    log: "mining/runs/<slug>/run-log.md"
    presentation: "output/loops/auto-mine/<run-id>/digest.html"
    render: ink-html
  mutation_policy:
    allows_mutation: false                  # v1: always false
```

`surface: read-only` is not a choice here — the core never modifies, deletes, or creates in any source (mine Safety Rule 1), so the read-only requirement is satisfied automatically. The self-graded metric is grounded only via the authorization below; the rubric alone is insufficient to justify an unattended run.

## Authorization

An unattended run is authorized by EITHER:

- a card for this run in the **`⚡ Autonomous`** lane of a task board — the user drags to approve; the agent PULLS from that lane and NEVER self-approves, OR
- a direct **"get going on this autonomously"** from the user (logged as a card in `Running` for traceability).

Authorization grounds the self-graded metric only. It never waives the resource budget, the read-only surface, the morning bundle, or the no-mutation rule. No approved card and no direct go → admission fails → **PARK with the reason**.


## Run + Park

Lifecycle: admission pass → run `/mine` to budget (its existing cycle, scoring, and keep/discard — do not re-document or fork it here) → stop on the core's own deterministic condition (3 consecutive cycles < 2 kept | source exhausted | mission answered | resource-envelope exhausted) → PARK at `awaiting_human` and emit the morning bundle. Any mutation discovered en route is parked, never applied.

Morning bundle, two surfaces in the loop's own tree:

- **run-log** (markdown, append-only, machine-read) — the core's *existing* `mining/runs/<slug>/run-log.md`. Not new; the envelope appends its admission result + park reason.
- **morning presentation** (HTML digest, human-read) — form-fit = **capsule preview**: top kept insights strip (ranked, by theme) + keep/discard ratio and yield trend + budget cap vs actual + parked-for-decision cards (none auto-resolve) + a link to the full capsule (`mining/<slug>.capsule.md`) and `authorization_ref`. If your workspace has a daily-digest surface, thread one sanitized line into it. If the HTML render fails, the run still parks — degrade to the markdown log.

## What it does NOT do

- **Mutate** anything — v1 `allows_mutation: false`, and the core is read-only regardless.
- **Resolve parked decisions** — the capsule and its parked cards are for you to judge in the morning; nothing auto-resolves.
- **Skip mandatory gates** — admission failure parks (never "continue as gated"); an authorization grounds the metric only and waives no other gate.
- **Re-document or fork** the `/mine` cycle, scoring, or capsule format — that lives in the `mine` skill's own `SKILL.md`, which is installed next to this skill. If `mine` is not installed, stop and say so.
