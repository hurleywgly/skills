---
name: events
description: Scan for upcoming networking events in your metro area, scored for relevance to your AI/product/builder interests
disable-model-invocation: true
---

# /events — Networking Events Scanner

Scan the web for upcoming networking events in your configured metro area, score them against your profile, optionally cross-reference with your networking contacts, and present a curated shortlist of 2-5 events worth attending.

Built for AI coding agents (Claude Code, Codex, and more) — no API keys, just WebSearch + WebFetch.

## When to Use

- Weekly check-in: "What events are coming up?"
- Pre-planning: "Anything good this month?"
- Targeted: `/events` for the full scan

## Subcommands

| Form | Behavior |
|------|----------|
| `/events` | Full scan — all tiers, networking overlay, conference radar |
| `/events quick` | Tier 1 only — known sources, fast check, skip conference radar |
| `/events conferences` | Conference radar only — 2-6 month lookahead for larger events |

---

## Phase 1: Load Config + State

Read these files from the skill directory (`.claude/skills/events/`):

1. **`config.json`** — Location, interests, output preferences
2. **`sources.md`** — Curated source list with URLs and search strategies
3. **`seen.json`** — Previously surfaced events

If `config.json` → `networking_overlay` is `true`, also read your networking contact source if you have one (configure its path in `config.json` → `networking_source`). This is optional — the skill works fine without it.

**Extract from networking data (if present):**
- All contact names and their companies
- Local contacts specifically (for "who might be there" overlay)
- Active networking targets and current priorities

---

## Phase 2: Gather Events

Calculate the search window:
- **Start date**: Today
- **End date**: Today + `lookahead_weeks` from config (default: 6 weeks)
- **Conference end date**: Today + `conference_lookahead_months` (default: 6 months)

Use the month names for the search window in queries (e.g., "April May 2026").

### Search Execution

Run queries **in parallel where possible**. Target 6-8 WebSearch queries total across tiers. Substitute `[metro]`, `[neighborhoods]`, and `[interests]` from your `config.json`; the examples below show the shape using generic placeholders.

**Tier 1 — Community-specific (highest signal):**
```
WebSearch: "[your top community/meetup] [metro]" [year]
WebSearch: [metro] [primary interest] event site:lu.ma OR site:meetup.com [year]
```

**Tier 2 — Broad local discovery:**
```
WebSearch: [metro] "developer" OR "product" meetup event [month range] [year]
WebSearch: [metro] startup founder event [year] -[exclusion term]
WebSearch: "[primary interest]" OR "[secondary interest]" event [metro] [year]
WebSearch: "[industry interest]" OR "[industry conference]" [year] -workshop -101
WebSearch: "[interest area]" conference OR summit [year] -beginner
```

**Tier 3 — Community sources:**
```
WebSearch: "[creator/podcast you follow]" event [metro] [year]
WebSearch: "[community/podcast]" event OR meetup [year]
```

**Tier 4 — Conference radar** (skip if `/events quick`):
```
WebSearch: [primary interest] conference [year] [region] OR [metro]
WebSearch: product management OR developer tools conference [year] [metro] OR [nearby major city]
WebSearch: "[industry conference 1]" OR "[industry conference 2]" [year]
WebSearch: "[industry expo]" OR "[industry summit]" [year]
```

### Detail Extraction

For the **top 3-5 most promising URLs** from search results:
- Use **WebFetch** to load the page
- Extract: event name, exact date/time, venue name + neighborhood, description, registration URL, speakers (if listed), organizer, capacity/RSVP count
- Prioritize fetching from lu.ma, meetup.com, eventbrite.com (structured event pages)
- Skip fetching generic blog posts or news articles

### Query Adaptation

If Tier 1-2 results are sparse (fewer than 3 events found):
- Try broader queries: `[metro] tech event [month] [year]`
- Try alternate platforms: `site:eventbrite.com [metro] technology event`
- Note thin results in output — don't pad with low-quality events

---

## Phase 3: Score + Filter

### Hard Filters (instant discard)

Remove any event that:
- Has already passed (date < today)
- Is outside your configured metro area (unless it's a major conference)
- Matches an exclusion term from `config.json` → `interests.exclude`
- Is obvious spam: generic "networking mixer" with no community backing, no named speakers, no agenda
- Is a beginner/hobbyist event: title matches a "101"/"getting started"/"launch your ___" pattern, or organizer is a single individual with no community/platform backing
- Costs >$100 and is not a major conference

### Scoring Rubric

Score each surviving event on four dimensions (0-30 scale):

| Dimension | Weight | 3 (Best) | 2 (Good) | 1 (Low) | 0 (Discard) |
|-----------|--------|-----------|-----------|---------|--------------|
| **Topic Relevance** | 3x | Matches a `primary` interest from config (top-tier industry events) | Matches a `secondary` interest; builder/product-focused | General tech, tangential | Off-topic |
| **Community Quality** | 3x | Named high-signal community you trust | Curated meetup with track record | Open Eventbrite with some curation | Generic spam, no community |
| **Networking Value** | 2x | Target company speakers; contacts likely present | Industry peers, potential contacts | General tech crowd | No networking relevance |
| **Convenience** | 2x | A `neighborhoods` entry from config | Anywhere in your metro | Virtual (partial credit) | Requires travel (unless conference) |

**Threshold**: Drop events scoring below **12/30**.

---

## Phase 4: Networking Overlay

If `networking_overlay` is enabled:

1. For each event, check:
   - Is the organizing company one of your networking targets?
   - Are any listed speakers in your contact list?
   - Is the event topic aligned with a specific contact's role? (e.g., an AI safety event → a contact who works in AI safety)
   - Would a local contact plausibly attend? (events matching their domain)

2. Annotate matching events with a **Network note**, e.g.:
   - "Team members from [target company] sometimes attend this community"
   - "Topic aligns with [contact]'s work — potential natural intro"
   - "[Contact] may find this angle relevant"

3. **Language rules:**
   - Always probabilistic: "may attend", "potential overlap", "aligns with"
   - Never definitive: NOT "[contact] will be there"
   - Only include if the connection is substantive, not forced

4. Events with networking overlap get a **+3 bonus** to their score.

---

## Phase 5: Rank + Render

### Selection

1. Sort all scored events descending
2. Select top events, ensuring the mix from `config.json`:
   - 1-2 technical / builder-focused
   - 1-2 startup / product / networking
   - 0-1 virtual (optional)
3. Cap at `max_events` (default: 5), floor at `min_events` (default: 2)
4. If fewer than `min_events` pass the threshold, note "Thin week — fewer events met the bar" rather than padding with low-quality results

### Conference Radar (separate section)

Events from Tier 4 queries that are:
- >6 weeks out
- Conference-scale (multi-day, named speakers, $100+ ticket)
- Strongly aligned with your identity / primary interests

List 1-3 max with early bird deadlines if known.

### Output Format

```markdown
## /events — Scanned [Day], [Month Day, Year]
**Window:** [Start Date] → [End Date] | **Sources:** [N] checked

---

### Recommended Events

#### 1. [Event Name] ⏰ SOON
**When:** [Full weekday], [Month Day, Year] · [Time]
**Where:** [Venue Name], [Neighborhood]
**Why:** [1 sentence — specific to your profile, not generic]
**Register:** [URL]
**Network note:** [If overlay found a match — omit line entirely if none]

#### 2. [Event Name]
**When:** [Full weekday], [Month Day, Year] · [Time]
**Where:** [Venue Name], [Neighborhood]
**Why:** [1 sentence]
**Register:** [URL]

...

---

### Conference Radar (2-6 months out)

- **[Conference Name]** — [Date range], [City] — [Why it fits] — [Early bird: Date] — [Link]

---

### Skipped
- [Event name] — [1-word reason: academic, robotics, spam, past, low-score]

### Sources Checked
- [Source/Query]: [N found, N kept]
- [Community source]: No public events found — check the community's private channel directly
```

### Output Rules

- **Absolute dates always** — never "this Thursday" or "next week"
- **SOON tag** on events within `soon_threshold_days` (default: 14 days)
- **[seen before]** tag on events that appeared in a previous run (from `seen.json`)
- **Why sentence must be specific to your profile** — not "Great networking event!" but "Applied AI demos from local builders — aligns with your developer tools positioning"
- **Omit empty sections** — no "Conference Radar" header if nothing found
- **Registration links must be real URLs** from search results — never fabricated

---

## Phase 6: Update State

After rendering output:

1. **Write to `seen.json`:**
   - Add all newly discovered events (those not already in `seen_events`)
   - Each entry: `{ "name": "...", "date": "YYYY-MM-DD", "url": "...", "first_seen": "YYYY-MM-DD", "status": "surfaced" }`
   - Update `last_run` timestamp

2. **Prune `seen.json`:**
   - Remove events with dates before today (past events)

---

## Graceful Degradation

| Failure | Behavior |
|---------|----------|
| WebSearch returns error | Log `[SOURCE UNAVAILABLE — WebSearch failed]`, continue with other results |
| WebFetch fails on a URL | Skip that URL, note in Sources Checked |
| Community source returns nothing | Note "No public events found — check the community's private channel directly" |
| Fewer than min_events pass threshold | Show what passed, note "Thin week" — never pad with low-quality |
| Networking source file missing | Skip overlay silently, note "Networking overlay skipped — state file not found" |
| All sources fail | Report "All sources unavailable — try again later or check manually" |

---

## Notes

- **No API keys required** — WebSearch + WebFetch only
- **Privacy**: No contact names in Discord delivery (future). Networking notes are for local output only.
- **Scheduling** (future): `CronCreate: "0 0 9 * * 1"` for Monday 9 AM. Requires Discord delivery config.
- **Calibration**: If scoring feels off, adjust weights in the rubric or add/remove sources in `sources.md`. The skill adapts to whatever is in those files.
