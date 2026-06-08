#!/usr/bin/env python3
"""Build self-contained example HTMLs for each /ink doc-type.

Reads each template, inlines base-styles.css (replacing the
`/* {{BASE_STYLES}} ... */` marker), substitutes realistic example
content, and writes to examples/type-<name>.html. These are the
renderable inputs for Chrome --headless --screenshot capture.
"""

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"
EXAMPLES = ROOT / "examples"

BASE_STYLES = (TEMPLATES / "base-styles.css").read_text()
BASE_RE = re.compile(r"/\*\s*\{\{BASE_STYLES\}\}.*?\*/", re.DOTALL)


def render(template_name: str, content: dict, out_name: str) -> Path:
    src = (TEMPLATES / template_name).read_text()
    inlined = BASE_RE.sub(lambda _m: BASE_STYLES, src, count=1)
    for key, val in content.items():
        inlined = inlined.replace("{{" + key + "}}", val)
    leftovers = re.findall(r"\{\{[A-Z0-9_]+\}\}", inlined)
    if leftovers:
        print(f"warning: unsubstituted in {template_name}: {sorted(set(leftovers))}")
    out = EXAMPLES / out_name
    out.write_text(inlined)
    return out


# ============================================================================
# PLANNING — kept from previous release
# ============================================================================

PLANNING_CONTENT = {
    "TITLE": "Editorial Cadence",
    "SUBTITLE": "Monthly themes vs. weekly drops — choosing the heartbeat for the next quarter",
    "AUTHOR": "Editorial · Q2 Planning",
    "DATE": "May 2026",
    "STATUS": "Draft for Review",
    "BRAND": "Ink · Planning Doc",
    "CONTEXT_PARAGRAPH_1": (
        "We're entering Q2 with three writers, two designers, and a thesis we're still earning. "
        "The current ad-hoc cadence — publish whenever a piece is ready — produces decent essays but no rhythm "
        "the audience can lock onto, which is the gap subscribers consistently flag in feedback."
    ),
    "CONTEXT_PARAGRAPH_2": (
        "We have to pick a heartbeat. Three plausible cadences emerged from the team retro. "
        "All three are deliverable; the question is which best matches our scarce input — focused writing time — "
        "to the outcome we actually want, which is compounding readership."
    ),
    "OPTION_A_NAME": "Weekly drops",
    "OPTION_A_DESCRIPTION": "Ship one essay every Tuesday, no themes. Highest output volume; trains the audience to check in often.",
    "OPTION_A_TRADEOFFS": "Volume over depth",
    "OPTION_A_COST": "~12 essays / quarter",
    "OPTION_A_RISK": "Burnout, thin pieces",
    "OPTION_B_NAME": "Monthly themes",
    "OPTION_B_DESCRIPTION": "Each month organizes around one question — three essays, one interview, one visual piece. Theme is announced, then explored, then closed with a synthesis.",
    "OPTION_B_TRADEOFFS": "Depth over volume",
    "OPTION_B_COST": "~6 essays + 3 satellites",
    "OPTION_B_RISK": "Theme misses if mis-picked",
    "OPTION_C_NAME": "Hybrid (themes + breaking)",
    "OPTION_C_DESCRIPTION": "Monthly themes as backbone, with reactive weekly posts when news demands it. Tries to capture both compounding and topicality.",
    "OPTION_C_TRADEOFFS": "Both, lightly",
    "OPTION_C_COST": "~9 pieces / quarter",
    "OPTION_C_RISK": "Always feels behind",
    "RECOMMENDATION_HEADLINE": "Adopt monthly themes for two quarters; revisit before Q4.",
    "RECOMMENDATION_RATIONALE": (
        "Themes give the team a shared frame to write into, give the audience a reason to come back, "
        "and let synthesis pieces compound the prior weeks' work — exactly the leverage we lack today. "
        "We pay for it in raw post count, but raw count isn't what's driving subscriber growth."
    ),
    "OPEN_QUESTION_1": "How do we handle a breaking-news week without violating the theme?",
    "OPEN_QUESTION_2": "Do we lock distribution to specific weekdays, or stay flexible inside the month?",
    "OPEN_QUESTION_3": "Who owns theme selection — editorial lead, vote, or rotating curator?",
    "NEXT_ACTION_1": "Pick May + June themes by end of week (editorial lead drafts, team approves)",
    "NEXT_ACTION_2": "Set up a one-page theme brief format so writers can claim angles within 48 hours",
    "NEXT_ACTION_3": "Define the success metric: returning-reader rate at end of Q2 over Q1",
}

# ============================================================================
# EXPLORATION — six distinct onboarding-screen mockups in a grid
# ============================================================================

def mockup_svg(label: str, fills: list[tuple[int, int, int, int, str]]) -> str:
    """Build a stylized onboarding-screen mockup as inline SVG.
    fills: list of (x, y, w, h, fill) rectangles.
    """
    rects = "\n      ".join(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{f}" />'
        for (x, y, w, h, f) in fills
    )
    return f'''
    <svg viewBox="0 0 280 210" preserveAspectRatio="xMidYMid meet" role="img" aria-label="{label}">
      <rect x="0" y="0" width="280" height="210" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1" rx="6"/>
      {rects}
    </svg>'''


# 1. Centered hero — single column, big headline, primary CTA
SVG_HERO = mockup_svg("Centered hero", [
    (90, 28, 100, 6, "#1A1A1A"),
    (60, 42, 160, 4, "#1A1A1A"),
    (70, 50, 140, 4, "#1A1A1A"),
    (40, 78, 200, 60, "#F7F8FA"),
    (90, 152, 100, 12, "#2563EB"),
    (95, 174, 90, 4, "#718096"),
])

# 2. Sidebar tour — left nav, content panel
SVG_SIDEBAR = mockup_svg("Sidebar tour", [
    (12, 12, 70, 186, "#F7F8FA"),
    (20, 24, 50, 4, "#2563EB"),
    (20, 38, 54, 3, "#1A1A1A"),
    (20, 48, 40, 3, "#718096"),
    (20, 58, 50, 3, "#718096"),
    (20, 68, 44, 3, "#718096"),
    (96, 24, 80, 5, "#1A1A1A"),
    (96, 38, 170, 3, "#1A1A1A"),
    (96, 46, 160, 3, "#1A1A1A"),
    (96, 54, 140, 3, "#1A1A1A"),
    (96, 110, 60, 50, "#E2E8F0"),
    (164, 110, 60, 50, "#E2E8F0"),
    (96, 178, 70, 12, "#2563EB"),
])

# 3. Bottom sheet (mobile) — content above, sticky CTA card at bottom
SVG_BOTTOM_SHEET = mockup_svg("Bottom sheet", [
    (40, 16, 200, 110, "#E2E8F0"),
    (102, 60, 76, 22, "#FFFFFF"),
    (114, 68, 52, 6, "#2563EB"),
    (12, 138, 256, 60, "#FFFFFF"),
    (24, 150, 130, 5, "#1A1A1A"),
    (24, 160, 100, 3, "#718096"),
    (24, 168, 110, 3, "#718096"),
    (180, 162, 76, 18, "#1A1A1A"),
])

# 4. Card grid — 2x2 of feature cards
SVG_CARD_GRID = mockup_svg("Card grid", [
    (80, 16, 120, 6, "#1A1A1A"),
    (40, 26, 200, 3, "#718096"),
    (16, 44, 124, 64, "#F7F8FA"),
    (28, 56, 36, 36, "#2563EB"),
    (28, 96, 80, 4, "#1A1A1A"),
    (140, 44, 124, 64, "#F7F8FA"),
    (152, 56, 36, 36, "#38A169"),
    (152, 96, 80, 4, "#1A1A1A"),
    (16, 116, 124, 64, "#F7F8FA"),
    (28, 128, 36, 36, "#D69E2E"),
    (28, 168, 80, 4, "#1A1A1A"),
    (140, 116, 124, 64, "#F7F8FA"),
    (152, 128, 36, 36, "#E53E3E"),
    (152, 168, 80, 4, "#1A1A1A"),
    (110, 192, 60, 8, "#2563EB"),
])

# 5. Full-bleed photo — hero image with text overlay
SVG_PHOTO = mockup_svg("Full-bleed photo", [
    (0, 0, 280, 210, "#FFFFFF"),
    (0, 0, 280, 130, "#1A1A1A"),
    (40, 22, 200, 80, "#4A5568"),
    (90, 50, 100, 24, "#F7F8FA"),
    (40, 144, 180, 5, "#1A1A1A"),
    (40, 154, 160, 3, "#718096"),
    (40, 162, 140, 3, "#718096"),
    (40, 178, 70, 12, "#2563EB"),
    (118, 178, 50, 12, "#FFFFFF"),
])

# 6. Progressive disclosure — stepper at top, single-question form
SVG_STEPPER = mockup_svg("Progressive disclosure", [
    (40, 22, 12, 12, "#2563EB"),
    (52, 28, 36, 1, "#E2E8F0"),
    (88, 22, 12, 12, "#2563EB"),
    (100, 28, 36, 1, "#E2E8F0"),
    (136, 22, 12, 12, "#E2E8F0"),
    (148, 28, 36, 1, "#E2E8F0"),
    (184, 22, 12, 12, "#E2E8F0"),
    (40, 56, 200, 6, "#1A1A1A"),
    (40, 70, 160, 3, "#718096"),
    (40, 92, 200, 28, "#F7F8FA"),
    (40, 128, 200, 28, "#F7F8FA"),
    (140, 174, 100, 14, "#2563EB"),
])

EXPLORATION_CONTENT = {
    "TITLE": "Onboarding Screen — 6 Approaches",
    "SUBTITLE": "Six distinct directions for the post-signup welcome screen. Each varies on layout density, tone, and how much it commits the user up front.",
    "AUTHOR": "Product · Onboarding Sprint",
    "DATE": "May 2026",
    "VARIANT_COUNT": "6",
    "BRAND": "Ink · Exploration",
    "VARIANT_1_NAME": "Centered hero",
    "VARIANT_1_SKETCH": SVG_HERO,
    "VARIANT_1_TRADEOFF": "One thing at a time. Lowest friction. Risks under-explaining the breadth of the product.",
    "VARIANT_1_TAG_A": "Low density",
    "VARIANT_1_TAG_B": "High clarity",
    "VARIANT_2_NAME": "Sidebar tour",
    "VARIANT_2_SKETCH": SVG_SIDEBAR,
    "VARIANT_2_TRADEOFF": "Persistent map of the territory. Lets the user wander but anchors them.",
    "VARIANT_2_TAG_A": "Medium density",
    "VARIANT_2_TAG_B": "Wayfinding",
    "VARIANT_3_NAME": "Bottom sheet",
    "VARIANT_3_SKETCH": SVG_BOTTOM_SHEET,
    "VARIANT_3_TRADEOFF": "Content first, CTA always reachable. Mobile-native feel. Cap on how much you can say above it.",
    "VARIANT_3_TAG_A": "Mobile-first",
    "VARIANT_3_TAG_B": "Sticky CTA",
    "VARIANT_4_NAME": "Feature card grid",
    "VARIANT_4_SKETCH": SVG_CARD_GRID,
    "VARIANT_4_TRADEOFF": "Shows the breadth of capability immediately. Risks paralysis if cards aren't ranked.",
    "VARIANT_4_TAG_A": "High density",
    "VARIANT_4_TAG_B": "Self-serve",
    "VARIANT_5_NAME": "Full-bleed photo",
    "VARIANT_5_SKETCH": SVG_PHOTO,
    "VARIANT_5_TRADEOFF": "Sets emotional tone before any feature. Brand-forward. Costs scroll for actual functionality.",
    "VARIANT_5_TAG_A": "Brand-forward",
    "VARIANT_5_TAG_B": "Editorial",
    "VARIANT_6_NAME": "Progressive disclosure",
    "VARIANT_6_SKETCH": SVG_STEPPER,
    "VARIANT_6_TRADEOFF": "Asks one question per step. Highest completion rate; lowest at-a-glance comprehension.",
    "VARIANT_6_TAG_A": "Stepwise",
    "VARIANT_6_TAG_B": "Form-led",
    "SYNTHESIS_PARAGRAPH": (
        "The variants vary on three axes: how much the screen tells you up front (density), "
        "how much agency it grants vs. directs (sidebar/grid vs. stepper), and how much weight the "
        "brand voice carries (hero/photo lean editorial; grid/stepper lean utilitarian). "
        "Pick by which axis matters most for our audience right now."
    ),
}

# ============================================================================
# EXPLAINER — "How prompt caching works" with SVG flow diagram
# ============================================================================

DIAGRAM_SVG = '''
    <svg viewBox="0 0 760 320" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Prompt caching flow">
      <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z" fill="#1A1A1A"/>
        </marker>
        <marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563EB"/>
        </marker>
      </defs>

      <!-- Request -->
      <g>
        <rect x="20" y="130" width="120" height="56" rx="10" fill="#FFFFFF" stroke="#1A1A1A" stroke-width="1.5"/>
        <text x="80" y="158" text-anchor="middle" font-family="-apple-system, sans-serif" font-size="13" font-weight="600" fill="#1A1A1A">Incoming</text>
        <text x="80" y="174" text-anchor="middle" font-family="-apple-system, sans-serif" font-size="13" font-weight="600" fill="#1A1A1A">request</text>
      </g>

      <!-- Arrow to cache check -->
      <line x1="142" y1="158" x2="208" y2="158" stroke="#1A1A1A" stroke-width="1.5" marker-end="url(#arrow)"/>

      <!-- Cache check (decision) -->
      <g>
        <polygon points="270,108 360,158 270,208 180,158" fill="#F7F8FA" stroke="#1A1A1A" stroke-width="1.5"/>
        <text x="270" y="154" text-anchor="middle" font-family="-apple-system, sans-serif" font-size="12" font-weight="600" fill="#1A1A1A">Prefix</text>
        <text x="270" y="170" text-anchor="middle" font-family="-apple-system, sans-serif" font-size="12" font-weight="600" fill="#1A1A1A">in cache?</text>
      </g>

      <!-- Hit branch -->
      <g>
        <line x1="360" y1="158" x2="430" y2="80" stroke="#2563EB" stroke-width="2" marker-end="url(#arrow-accent)"/>
        <text x="378" y="108" font-family="-apple-system, sans-serif" font-size="11" font-weight="700" fill="#2563EB">HIT</text>

        <rect x="430" y="40" width="200" height="76" rx="10" fill="#EBF2FE" stroke="#2563EB" stroke-width="1.5"/>
        <text x="530" y="64" text-anchor="middle" font-family="-apple-system, sans-serif" font-size="12" font-weight="700" fill="#2563EB">CACHED PREFIX</text>
        <text x="530" y="84" text-anchor="middle" font-family="-apple-system, sans-serif" font-size="12" fill="#1A1A1A">~10× faster, 90% cost</text>
        <text x="530" y="100" text-anchor="middle" font-family="-apple-system, sans-serif" font-size="12" fill="#1A1A1A">reduction on prefix</text>

        <line x1="630" y1="78" x2="700" y2="120" stroke="#2563EB" stroke-width="2" marker-end="url(#arrow-accent)"/>
      </g>

      <!-- Miss branch -->
      <g>
        <line x1="360" y1="158" x2="430" y2="232" stroke="#1A1A1A" stroke-width="1.5" marker-end="url(#arrow)"/>
        <text x="378" y="218" font-family="-apple-system, sans-serif" font-size="11" font-weight="700" fill="#1A1A1A">MISS</text>

        <rect x="430" y="200" width="200" height="76" rx="10" fill="#FFFFFF" stroke="#1A1A1A" stroke-width="1.5"/>
        <text x="530" y="224" text-anchor="middle" font-family="-apple-system, sans-serif" font-size="12" font-weight="700" fill="#1A1A1A">FULL PROCESSING</text>
        <text x="530" y="244" text-anchor="middle" font-family="-apple-system, sans-serif" font-size="12" fill="#4A5568">prefix written to cache</text>
        <text x="530" y="260" text-anchor="middle" font-family="-apple-system, sans-serif" font-size="12" fill="#4A5568">for next request</text>

        <line x1="630" y1="238" x2="700" y2="195" stroke="#1A1A1A" stroke-width="1.5" marker-end="url(#arrow)"/>
      </g>

      <!-- Response -->
      <g>
        <rect x="700" y="130" width="40" height="56" rx="10" fill="#1A1A1A"/>
        <text x="720" y="166" text-anchor="middle" font-family="-apple-system, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF">→</text>
      </g>
      <text x="720" y="208" text-anchor="middle" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" fill="#4A5568">Response</text>
    </svg>'''

CODE_BLOCK = (
    '<span class="code-comment"># Mark the system prompt as cacheable</span>\n'
    'response = client.messages.create(\n'
    '    model=<span class="code-string">"claude-opus-4-7"</span>,\n'
    '    system=[\n'
    '        {\n'
    '            <span class="code-keyword">"type"</span>: <span class="code-string">"text"</span>,\n'
    '            <span class="code-keyword">"text"</span>: long_system_prompt,        <span class="code-comment"># 50KB+ ideally</span>\n'
    '            <span class="code-keyword">"cache_control"</span>: {<span class="code-keyword">"type"</span>: <span class="code-string">"ephemeral"</span>},\n'
    '        }\n'
    '    ],\n'
    '    messages=[\n'
    '        {<span class="code-keyword">"role"</span>: <span class="code-string">"user"</span>, <span class="code-keyword">"content"</span>: query},\n'
    '    ],\n'
    ')\n'
    '<span class="code-comment"># 5-min TTL on the cached prefix; second call to this prompt</span>\n'
    '<span class="code-comment"># pays only for the user-message tokens.</span>'
)

EXPLAINER_CONTENT = {
    "TITLE": "Prompt Caching, From the Inside",
    "SUBTITLE": "How the cache decides what survives, why long prefixes win, and the gotchas that erase your savings.",
    "AUTHOR": "Engineering · Inference Notes",
    "DATE": "May 2026",
    "READING_TIME": "8 min read",
    "BRAND": "Ink · Explainer",
    "LEAD_PARAGRAPH": (
        "Prompt caching is the rare optimization that's both cheap to adopt and easy to misuse. "
        "Mark a long, stable prefix as cacheable, and the next call that reuses that exact prefix gets it "
        "back at roughly a tenth of the cost and a fraction of the latency. The whole story is in what "
        "counts as 'exact' and what counts as 'long enough.' This explainer walks the request path end-to-end, "
        "shows the exact API surface, and names the gotchas that quietly destroy hit rates in production."
    ),
    "SECTION_1_TITLE": "How the cache decides",
    "SECTION_1_PARAGRAPH_1": (
        "Every request enters with an ordered list of content blocks. The cache walks that list from the "
        "start and asks, for each block: have I seen exactly this content recently? The first block that "
        "doesn't match is where the cache stops contributing. Anything after that block is treated as fresh "
        "input — full price, full latency."
    ),
    "SECTION_1_PARAGRAPH_2": (
        "That ordering is the entire mental model. Stable content (system prompts, tool definitions, "
        "long static context) belongs at the front. Variable content (user messages, dynamic state) "
        "belongs at the back. Putting a single dynamic field — a timestamp, a session id — into the "
        "system prompt collapses your hit rate to zero, because the cache can't match past the first "
        "byte that changed."
    ),
    "DIAGRAM_SVG": DIAGRAM_SVG,
    "DIAGRAM_CAPTION": "On hit, the cached prefix returns at ~10× speed and 10% of the prefix cost. On miss, the prefix is written to cache for the next call.",
    "SECTION_2_TITLE": "The minimum-viable invocation",
    "SECTION_2_PARAGRAPH": (
        "Marking a block as cacheable is one field. The block needs a minimum length — currently 1024 "
        "tokens for most models — and the TTL is short by default (5 minutes), which is the right tradeoff "
        "for chat-style workloads where the same prefix is hit many times in a session."
    ),
    "CODE_BLOCK": CODE_BLOCK,
    "PULL_QUOTE": "Cache hits don't survive small edits. They survive identical prefixes. The discipline is putting variation at the back.",
    "PULL_QUOTE_ATTRIBUTION": "— Inference team postmortem, after the templating bug erased a quarter of cache savings",
    "SECTION_3_TITLE": "Tradeoffs at a glance",
    "SECTION_3_PARAGRAPH": (
        "The cache helps most when the prefix is long, the prefix is reused often within the TTL, and the "
        "variable tail is small relative to the prefix. The same conditions, inverted, are where caching "
        "stops paying off."
    ),
    "TRADEOFF_COL_1": "Dimension",
    "TRADEOFF_COL_2": "Helps when…",
    "TRADEOFF_COL_3": "Hurts when…",
    "TRADEOFF_ROW_1A": "Prefix length",
    "TRADEOFF_ROW_1B": "Prefix is 10K+ tokens (system prompt, tools, RAG context)",
    "TRADEOFF_ROW_1C": "Prefix is short and hand-built per request",
    "TRADEOFF_ROW_2A": "Reuse pattern",
    "TRADEOFF_ROW_2B": "Same prefix hit many times within 5-min TTL",
    "TRADEOFF_ROW_2C": "Cold-start workloads (rare, isolated requests)",
    "TRADEOFF_ROW_3A": "Tail variance",
    "TRADEOFF_ROW_3B": "User message is small; rest is fixed context",
    "TRADEOFF_ROW_3C": "Each request rewrites large parts of the prompt",
    "TRADEOFF_ROW_4A": "Stability",
    "TRADEOFF_ROW_4B": "System prompt is content-addressed and version-pinned",
    "TRADEOFF_ROW_4C": "System prompt has timestamps, request IDs, or per-user data inline",
    "GOTCHA_1": "Whitespace counts. A trailing newline added to the system prompt by your templating engine breaks every cache hit until something cycles it back.",
    "GOTCHA_2": "Tool definitions are part of the prefix. Reordering tools — even alphabetizing them later — invalidates the cached prefix.",
    "GOTCHA_3": "TTL is sliding from last hit, not from first write. A prefix that gets hit every 4.5 minutes can stay warm indefinitely; one that goes 6 minutes idle has to be rewritten.",
}

# ============================================================================
# EDITOR — Linear-style ticket reprioritizer with drag/drop + copy-as-markdown
# ============================================================================

EDITOR_TICKETS = [
    {"id": "ENG-301", "title": "Migrate auth flow off legacy session middleware", "tags": ["auth", "L"], "bucket": "now"},
    {"id": "ENG-302", "title": "Add rate limit headers to public API responses", "tags": ["api", "S"], "bucket": "now"},
    {"id": "ENG-303", "title": "Fix flaky test in checkout integration suite", "tags": ["tests", "XS"], "bucket": "now"},
    {"id": "ENG-304", "title": "Quote engine: round-trip currency conversion bug", "tags": ["billing", "M"], "bucket": "now"},
    {"id": "ENG-305", "title": "Webhook retry budget — exponential, not linear", "tags": ["webhooks", "S"], "bucket": "next"},
    {"id": "ENG-306", "title": "Audit log surface for compliance dashboard", "tags": ["compliance", "M"], "bucket": "next"},
    {"id": "ENG-307", "title": "Self-serve API key rotation for org admins", "tags": ["api", "M"], "bucket": "next"},
    {"id": "ENG-308", "title": "Storybook coverage for revamped form primitives", "tags": ["frontend", "S"], "bucket": "next"},
    {"id": "ENG-309", "title": "Revisit OTel sampling strategy for prod traces", "tags": ["observability", "L"], "bucket": "later"},
    {"id": "ENG-310", "title": "Investigate moving job queue from Redis to NATS", "tags": ["infra", "L"], "bucket": "later"},
    {"id": "ENG-311", "title": "i18n scaffolding for billing emails", "tags": ["i18n", "M"], "bucket": "later"},
    {"id": "ENG-312", "title": "Server-rendered marketing site (was Next-on-Vercel)", "tags": ["marketing", "L"], "bucket": "later"},
    {"id": "ENG-313", "title": "Re-skin deprecated admin tool to new design system", "tags": ["frontend", "M"], "bucket": "cut"},
    {"id": "ENG-314", "title": "On-call rotation portal (replace Google Sheet)", "tags": ["ops", "M"], "bucket": "cut"},
]

EDITOR_RATIONALE = {
    "now": "Quarter-blockers — auth migration deadline, the API rate-limit promise, and the two production bugs we owe customers.",
    "next": "Picked up the moment a Now slot frees. All four are Q3 commitments; none are blocking today.",
    "later": "Real work, not committed yet. We'd love to get to these but won't promise.",
    "cut": "Off the roadmap unless the cost of not doing them changes. Be explicit so they stop drifting back in.",
}

EDITOR_CONTENT = {
    "TITLE": "Reprioritize the Engineering Backlog",
    "SUBTITLE": "Drag tickets between Now / Next / Later / Cut. Hit Copy when you're happy; paste back into Claude with a one-line rationale per bucket.",
    "BRAND": "Ink · Editor",
    "CONTROLS_LABEL": "Drag to sort",
    "CONTROLS_HEADING": "14 tickets · arrange by quarter",
    "COPY_TITLE": "Engineering Backlog — May 2026 reprioritization",
    "INITIAL_DATA": ",\n      ".join(json.dumps(t) for t in EDITOR_TICKETS),
    "RATIONALE_OBJECT": json.dumps(EDITOR_RATIONALE),
}


if __name__ == "__main__":
    p = render("planning-template.html", PLANNING_CONTENT, "type-planning.html")
    e = render("exploration-template.html", EXPLORATION_CONTENT, "type-exploration.html")
    x = render("explainer-template.html", EXPLAINER_CONTENT, "type-explainer.html")
    d = render("editor-template.html", EDITOR_CONTENT, "type-editor.html")
    for path in (p, e, x, d):
        print(f"wrote {path}")
