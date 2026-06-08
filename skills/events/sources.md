# Event Sources

This is your curated source list. The `/events` skill reads it on every run to know
where to look and what to prioritize. Build it out for your own metro and interests —
the rows below are platform-agnostic examples to get you started.

## How the tiered model works

Sources are organized into tiers by signal quality. Higher tiers get searched first
and weighted more heavily in scoring (see the rubric in `SKILL.md`).

- **Tier 1 — Community-specific (highest signal):** Named communities/meetups you trust.
  These are the events most worth your time. Add the exact community name + city so the
  skill can search for them directly.
- **Tier 2 — Broad local discovery:** Platform searches scoped to your metro and interests.
- **Tier 3 — Community / creator sources:** Podcasts, newsletters, or creators whose
  in-person events you'd attend.
- **Tier 4 — Conference radar:** Multi-day, ticketed industry conferences (2-6 months out).

For each source, note: the name, a URL or search strategy, and which tier it belongs to.

## Example sources

| Tier | Source | Strategy |
|------|--------|----------|
| 1 | Your top local community/meetup | `WebSearch: "<community name> <city>" <year>` |
| 2 | Luma (local discovery) | `WebSearch: <city> <interest> event site:lu.ma <year>` |
| 2 | Meetup | `WebSearch: <city> <interest> meetup site:meetup.com <year>` |
| 2 | Eventbrite | `WebSearch: site:eventbrite.com <city> <interest> event <year>` |
| 3 | A podcast/newsletter you follow | `WebSearch: "<show name>" event OR meetup <year>` |
| 4 | Major industry conference | `WebSearch: "<conference name>" <year>` |

## Notes

- Prefer structured event platforms (Luma, Meetup, Eventbrite) for detail extraction —
  they have clean date/venue/RSVP fields.
- Some communities only publish events to a private channel (Slack/Discord). For those,
  list the community here and check it manually; the skill will note when it can't find
  public listings.
- Calibrate over time: if scoring feels off, adjust the weights in `SKILL.md` or
  add/remove sources here. The skill adapts to whatever is in these files.
