---
name: pull-digg
description: Pull curated high-signal Digg AI-news items, rank movement, citations, authors, and GitHub feeds through read-only digg-pp-cli.
disable-model-invocation: true
---

# /pull-digg — Curated Digg AI Signal Pull

Pull a tight, curated readout from Digg's AI-news surface using `digg-pp-cli`. Use this for on-demand briefings, topic research, AI-repo discovery, source credibility checks, and rank-movement monitoring.

## When to Use This Skill

**Triggers when:**
- User invokes `/pull-digg`
- User asks what is trending on Digg or Di.gg
- User asks for Digg AI stories, AI-news rank movement, replaced stories, Digg authors, or Digg GitHub feeds
- User wants citations from Digg-tracked X posts around a story or topic

**Do NOT trigger for:**
- General builder signal pulls across X, podcasts, and newsletters; use `/pull-feed`
- Broad web research that should search beyond Digg; use `/research`
- Posting, commenting, voting, scraping private data, or changing anything on Digg

## Safety Posture

`digg-pp-cli` is read-only and uses public Digg surfaces. Do not use this skill for mutation, automation against authenticated sessions, or high-frequency polling unless the user explicitly asks for watch behavior. Prefer one-shot pulls.

No Digg authentication is required.

## Setup Check

Before the first CLI call in a session:

```bash
command -v digg-pp-cli || npx -y @mvanhorn/printing-press install digg --cli-only
digg-pp-cli --version
digg-pp-cli doctor
```

If installation succeeds but the command is still missing, check `$HOME/go/bin` and `$GOPATH/bin` for `digg-pp-cli` and add the right directory to PATH for the current shell. Do not run Digg commands until `digg-pp-cli --version` works.

If `digg-pp-cli github --help` fails but the user asked for GitHub feeds, install the current linked repo build:

```bash
go install github.com/mvanhorn/printing-press-library/library/media-and-entertainment/digg/cmd/digg-pp-cli@main
mkdir -p "$HOME/.local/bin"
ln -sf "$HOME/go/bin/digg-pp-cli" "$HOME/.local/bin/digg-pp-cli"
digg-pp-cli github --help
```

## Invocation

| Command | Behavior |
|---------|----------|
| `/pull-digg` | Curated briefing: top 3-5 signals across stories, movers, replacements, and GitHub repos |
| `/pull-digg top [--limit N]` | Raw current top Digg AI stories |
| `/pull-digg topic "<query>" [--since 30d]` | Search Digg stories for a topic and pull source posts for the strongest clusters |
| `/pull-digg github` | Digg GitHub feeds: starred AI repos and recent activity |
| `/pull-digg authors` | Top tracked authors, movers, and newly listed accounts |
| `/pull-digg author <handle>` | Credibility lookup for one X handle |
| `/pull-digg story <clusterUrlId>` | Story detail, evidence, sentiment, crossrefs, and top source posts |
| `/pull-digg pipeline` | Current ingestion status and recent pipeline events |
| `/pull-digg full` | Less-curated feed view: more stories and repo items, still summarized |
| `/pull-digg raw <args>` | Direct passthrough to `digg-pp-cli <args> --json --no-input --no-color --yes` |

Default candidate-pull limits unless the user specifies otherwise:
- Top stories pool: 15
- Fast climbers pool: since 6h
- Replaced stories pool: since 24h
- GitHub stars pool: 10
- GitHub recent activity pool: 20
- Source posts per selected story: 3

Default selected-output caps:
- Lead signals: 3-5 total
- Repo signals: 2-4 total
- Watchlist: 0-3 lower-confidence items
- Source voices: only when they materially change the readout

## Workflow

### Step 1: Parse Intent

Map the user request to the narrowest command. If unclear, run:

```bash
digg-pp-cli which "<plain language request>"
```

If `which` has no confident match, use `digg-pp-cli --help` or the relevant subcommand help.

### Step 2: Refresh Local State

For default briefings and any command that depends on local rank history, run:

```bash
digg-pp-cli sync
```

Skip `sync` only when the user asks for a fast live lookup, raw passthrough, or a command that is explicitly live-first.

### Step 3: Pull the Right Signals

**Default briefing:**

```bash
digg-pp-cli sync
digg-pp-cli top --limit 15 --json --no-input --no-color --yes --select clusterUrlId,title,tldr,currentRank,peakRank,delta,likes,views,lastSeenAt
digg-pp-cli events --since 6h --type fast_climb --json --no-input --no-color --yes --select clusterId,label,delta,currentRank,previousRank
digg-pp-cli replaced --since 24h --json --no-input --no-color --yes
digg-pp-cli github stars --limit 10 --json --no-input --no-color --yes
digg-pp-cli github recent --limit 20 --json --no-input --no-color --yes
```

**Topic research with citations:**

```bash
digg-pp-cli search "<query>" --since 30d --limit 10 --json --no-input --no-color --yes
digg-pp-cli posts <clusterUrlId> --by rank --limit 5 --json --no-input --no-color --yes
```

Pull posts for the top 2-4 clusters only. Cite X URLs when available.

**Story detail:**

```bash
digg-pp-cli story <clusterUrlId> --json --no-input --no-color --yes
digg-pp-cli evidence <clusterUrlId> --json --no-input --no-color --yes
digg-pp-cli sentiment <clusterUrlId> --window 6h --json --no-input --no-color --yes
digg-pp-cli crossref <clusterUrlId> --json --no-input --no-color --yes
digg-pp-cli posts <clusterUrlId> --by rank --limit 5 --json --no-input --no-color --yes
```

**Author credibility:**

```bash
digg-pp-cli authors get <handle> --json --no-input --no-color --yes
```

For off-1000 handles, explain `peer_follow_gap` as the gap to the rank-1000 account measured in AI-1000 peer follows. Do not describe it as raw X follower distance.

**Authors browse:**

```bash
digg-pp-cli authors top --by influence --limit 25 --json --no-input --no-color --yes
digg-pp-cli authors list --by rankChange --limit 20 --json --no-input --no-color --yes
digg-pp-cli authors list --only-new --json --no-input --no-color --yes
```

**Pipeline check:**

```bash
digg-pp-cli pipeline status --json --no-input --no-color --yes
```

If `pipeline status` is not available in the installed version, use:

```bash
digg-pp-cli trending status --json --no-input --no-color --yes
```

### Step 4: Curate

Default `/pull-digg` is a scout pass, not a feed dump. Pull enough raw material to compare, then select only items that clear a bar.

Keep an item when it has at least one strong reason:
- **Builder relevance:** agent tooling, coding tools, local models, evals, open-source infrastructure, AI workflow design, or model/tool behavior you can use or write about.
- **Rank momentum:** fast climb, replacement rationale, sharp rank reversal, or newly visible cluster.
- **Credible-source signal:** high-ranked or unusually relevant Digg-tracked accounts are posting/starring it.
- **Repo signal:** concrete GitHub project with credible starrers, practical use case, breakout/novel score, or direct relevance to agents/tools.
- **Strategic signal:** frontier lab strategy, compute economics, distribution/platform shifts, safety/product constraints with practical implications.

Drop or demote:
- Generic launch/announcement items with no practical angle.
- AI culture-war or ideology bait unless there is real methodological detail or unusually broad uptake.
- Duplicate stories that say the same thing as a higher-signal item.
- Big view-count stories whose only merit is being weird.
- GitHub repos with low relevance or no clear "why now" despite stars.

Score candidates quickly before writing:

| Dimension | 0 | 1 | 2 |
|-----------|---|---|---|
| Practical value | Trivia | Interesting context | Usable for building, writing, research, or decisions |
| Novelty | Seen everywhere | New angle | New primitive, benchmark, workflow, or shift |
| Signal quality | Weak/unclear source | Some credible uptake | Multiple credible accounts, strong rank move, or concrete repo evidence |

Default inclusion threshold: **4/6**. A 3/6 item can appear only in Watchlist. Do not pad to fill sections.

### Step 5: Synthesize

Turn selected items into a compact signal readout. Prioritize:

1. Why the signal matters to your builder context
2. What changed since a generic AI-news scan
3. What to inspect next if the item deserves deeper work
4. Links to Digg, X, or GitHub evidence

Do not overstate Digg's rankings as objective truth. Treat them as one signal from a curated AI-news graph.

## Output Format

```markdown
# Digg Signal — [Day, Month Date, Year]

_Pulled from Digg via `digg-pp-cli` · [live/local provenance if known]_

## Lead Signals

1. **[Title]** — #[rank] ([movement if meaningful])
   Why it survived: [specific curation reason]
   What to do with it: [builder/research/content angle]
   Link: [Digg cluster URL]

## Repo Signals

- **[repo]** — [why Digg-tracked accounts are surfacing it] — [GitHub URL]

## Watchlist

- **[Story/repo]** — [why it is not a lead signal yet, and what would upgrade it]

## Source Voices

- **@handle** (rank #[rank]) on **[story]**: [short paraphrase] — [X URL]

## Dropped

- [Optional: 2-4 notable items skipped, with one-word reason: duplicate, weird-only, generic, low-practical-value]

## Scout Notes

- [2-4 bullets on the overall pattern and best next investigation]
```

Omit empty sections. Keep the briefing concise; link to raw Digg, X, or GitHub URLs for evidence rather than pasting long post bodies. If only 2 items clear the bar, output 2 items.

## Error Handling

- Missing CLI: install with the setup command, then verify `digg-pp-cli --version`.
- Empty local results: run `digg-pp-cli sync`, then retry.
- HTTP 429: stop, report rate limit, and suggest a later retry. Do not loop.
- `cluster not found`: use `clusterUrlId`, not the UUID-style cluster ID. Get IDs from `digg-pp-cli top --json --select clusterUrlId,title`.
- Pipeline command mismatch: try `trending status` if `pipeline status` fails.
- Verbose output: rerun with `--select` to narrow fields.

## CLI Notes

- Prefer `--json --no-input --no-color --yes` for skill workflows. Use `--agent` only when compact output is acceptable; it can remove fields needed for synthesis.
- Use `--select a,b,nested.path` to reduce context on array outputs. If an envelope command returns `{}`, rerun without `--select` and parse `.results`.
- Most data commands wrap results in an envelope: read `.results` for data and `.meta.source` for live/local provenance.
- `digg-pp-cli feedback "short note"` records local feedback at `~/.digg-pp-cli/feedback.jsonl`; use it only for concrete CLI surprises discovered while working.
