# Ink: image generation

Read this only when the user asks for a generated image (hero graphic, illustration, banner). It is optional and needs the user's own API key.

**Fast path:** the skill ships a script that implements both providers and the key lookup described below. Prefer it over hand-writing the HTTP request:

```bash
python3 <skill-folder>/bin/ink-image.py "<enhanced prompt>" --provider gemini|openai --out ./output/<slug>.png
python3 <skill-folder>/bin/ink-image.py --help   # quality and size options
```

The rest of this file is the routing logic, the setup message to show when no key exists, and the raw request shapes for when the script cannot run.

Image generation supports two providers — pick by user preference, content fit, or whichever API key is configured. Both write PNG to `./output/[slug].png`; both are optional, BYO key.

| Provider | Model | Cost / image | Strengths |
|---|---|---|---|
| **Gemini** (default) | `gemini-2.5-flash-image` (Nano Banana) | ~$0.04 | Fast, decent text rendering, good at illustrative/editorial heroes |
| **OpenAI** | `gpt-image-2` | ~$0.006 (low) – $0.21 (high) | Sharper prompt adherence, strong typography/text-in-image, more photoreal |

When in doubt, ask: *"Generate this with Gemini Nano Banana (~$0.04) or OpenAI gpt-image-2 (~$0.04–$0.21 depending on quality)?"* Default to **Gemini** if the user has no preference and only one key is configured — fall back to the provider whose key is present.

## Provider routing (decide once, then generate)

```
Has user named a provider?
├─ "gemini" / "nano" / "nano-banana"  → Gemini path
├─ "openai" / "gpt" / "gpt-image-2"   → OpenAI path
└─ no preference → check keys (env then ~/.ink/config.json):
    ├─ both present → ask the user
    ├─ only one     → use that one
    └─ neither      → first-run setup prompt (below)
```

## First-run setup (no keys found)

```
Ink can generate images via:

1. Google Gemini (~$0.04/image). Free API key: https://aistudio.google.com/apikey
   export GOOGLE_API_KEY="your-key"
   — or — echo '{"google_api_key": "your-key"}' >> ~/.ink/config.json

2. OpenAI gpt-image-2 (~$0.006–$0.21/image, token-based). Key: https://platform.openai.com/api-keys
   export OPENAI_API_KEY="your-key"
   — or — add "openai_api_key" to ~/.ink/config.json

Skip? Ink works great for documents without imagery — use `placeholders` or `none`.
```

If the user skips, offer a document alternative: "I can make this as a styled infographic instead."

## Gemini path (existing — Nano Banana)

**Check for key:** `GOOGLE_API_KEY` env var, else `~/.ink/config.json` → `google_api_key`.

```bash
mkdir -p ./output

curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: ${GOOGLE_API_KEY}" \
  -d '{
    "contents": [{
      "parts": [{"text": "[ENHANCED_PROMPT]"}]
    }],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"]
    }
  }' | python3 -c "
import os, sys, json, base64
resp = json.load(sys.stdin)
out_path = os.path.expanduser('./output/[slug].png')
for part in resp['candidates'][0]['content']['parts']:
    if 'inlineData' in part:
        with open(out_path, 'wb') as f:
            f.write(base64.b64decode(part['inlineData']['data']))
        print(out_path)
        break
"
```

## OpenAI path (gpt-image-2)

**Check for key:** `OPENAI_API_KEY` env var, else `~/.ink/config.json` → `openai_api_key`.

**Request shape:**
- Endpoint: `POST https://api.openai.com/v1/images/generations`
- Required: `model: "gpt-image-2"`, `prompt`
- Optional: `size` (`"1024x1024"`, `"1024x1536"`, `"1536x1024"`, or `"auto"`), `quality` (`"low"` ~$0.006, `"medium"` ~$0.05, `"high"` ~$0.21), `n` (default 1)
- Response: `data[0].b64_json` — base64-encoded PNG (no `response_format` field needed; gpt-image-2 returns b64 by default)

```bash
mkdir -p ./output

curl -s "https://api.openai.com/v1/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${OPENAI_API_KEY}" \
  -d '{
    "model": "gpt-image-2",
    "prompt": "[ENHANCED_PROMPT]",
    "size": "1536x1024",
    "quality": "medium",
    "n": 1
  }' | python3 -c "
import os, sys, json, base64
resp = json.load(sys.stdin)
if 'error' in resp:
    print(f\"OpenAI error: {resp['error']}\", file=sys.stderr); sys.exit(1)
out_path = os.path.expanduser('./output/[slug].png')
img_b64 = resp['data'][0]['b64_json']
with open(out_path, 'wb') as f:
    f.write(base64.b64decode(img_b64))
print(out_path)
"
```

**Picking a `quality` tier:** start at `medium` for general use. Use `high` for hero shots, infographics with embedded typography, and anything that will be printed or projected. Use `low` for iteration / sketching.

## Prompt enhancement (applies to either provider)

Before sending, enhance the user's description with quality keywords:
- Add: "professional quality, clean composition, high detail"
- For illustrations: "editorial illustration style, modern, clean lines"
- For heroes/banners: "wide format, web-optimized, strong visual hierarchy"
- For infographics (where gpt-image-2 shines): "infographic layout, integrated labels and typography, hierarchical, legible at thumbnail and full size"
- Never add: watermarks, text overlays (unless requested), stock photo aesthetics

## Confirm

```
Image created: ./output/[slug].png

Provider: [Gemini Nano Banana | OpenAI gpt-image-2]
Quality:  [n/a | low/medium/high]
Cost:     ~$[0.04 | 0.006 / 0.05 / 0.21]
Resolution: [width x height]

To iterate: describe what to change and I'll regenerate. To switch providers: name the other one.
```
