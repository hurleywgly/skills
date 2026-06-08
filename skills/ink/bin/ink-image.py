#!/usr/bin/env python3
"""ink-image — generate a single image via Google Gemini or OpenAI gpt-image-2.

Minimum-viable reference implementation. The /ink skill's SKILL.md documents
the full request shape; this script is the executable version so a user can
sanity-check either provider without driving the whole skill.

Usage
-----
  ink-image.py "prompt text" --provider openai --quality medium --size 1536x1024 \\
      --out ./output/foo.png

  ink-image.py "prompt text" --provider gemini --out ./output/foo.png

Auth
----
  GOOGLE_API_KEY or ~/.ink/config.json -> google_api_key
  OPENAI_API_KEY or ~/.ink/config.json -> openai_api_key

If --provider is omitted, picks whichever key is configured; if both are
configured, defaults to openai (sharper text-in-image). Override anytime.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path


def _ssl_context() -> ssl.SSLContext:
    """Build an SSL context that works on macOS Python.framework installs
    without requiring `Install Certificates.command` to have been run.
    Falls back to certifi's bundle if the system store can't verify."""
    try:
        ctx = ssl.create_default_context()
        ctx.load_default_certs()
        # Smoke-test against a well-known host's cert chain — if we can't,
        # try certifi.
        return ctx
    except Exception:
        pass
    try:
        import certifi  # type: ignore
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


_SSL_CTX = _ssl_context()


def load_config_keys() -> dict[str, str]:
    cfg_path = Path("~/.ink/config.json").expanduser()
    if not cfg_path.exists():
        return {}
    try:
        return json.loads(cfg_path.read_text())
    except json.JSONDecodeError:
        return {}


def resolve_key(env_var: str, cfg_key: str) -> str | None:
    return os.environ.get(env_var) or load_config_keys().get(cfg_key)


def pick_provider(provider: str | None) -> str:
    """Honor explicit choice; otherwise prefer whichever key is set."""
    if provider:
        return provider
    has_openai = bool(resolve_key("OPENAI_API_KEY", "openai_api_key"))
    has_gemini = bool(resolve_key("GOOGLE_API_KEY", "google_api_key"))
    if has_openai and not has_gemini:
        return "openai"
    if has_gemini and not has_openai:
        return "gemini"
    if has_openai and has_gemini:
        return "openai"  # default tiebreaker — better in-image typography
    sys.exit(
        "No image provider configured. Set OPENAI_API_KEY or GOOGLE_API_KEY,\n"
        "or add a key to ~/.ink/config.json. See README for details."
    )


def post_json(url: str, headers: dict[str, str], body: dict) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=300, context=_SSL_CTX) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read())
        except Exception:
            err = {"raw": str(e)}
        sys.exit(f"HTTP {e.code} from {url}:\n{json.dumps(err, indent=2)}")
    except urllib.error.URLError as e:
        # Most common cause on macOS Python.framework: the default cert
        # store hasn't been initialized. If we can fall back to certifi,
        # retry once with that.
        if isinstance(e.reason, ssl.SSLCertVerificationError):
            try:
                import certifi  # type: ignore
                fallback_ctx = ssl.create_default_context(cafile=certifi.where())
                with urllib.request.urlopen(req, timeout=300, context=fallback_ctx) as resp:
                    return json.loads(resp.read())
            except ImportError:
                sys.exit(
                    f"SSL verification failed against {url} and certifi isn't installed.\n"
                    f"Fix one of these: `pip install certifi`, or run\n"
                    f"  /Applications/Python\\ 3.*/Install\\ Certificates.command"
                )
        sys.exit(f"Network error talking to {url}: {e}")


def generate_openai(prompt: str, size: str, quality: str, out: Path) -> Path:
    key = resolve_key("OPENAI_API_KEY", "openai_api_key")
    if not key:
        sys.exit("OPENAI_API_KEY not set (env or ~/.ink/config.json).")
    resp = post_json(
        "https://api.openai.com/v1/images/generations",
        {"Authorization": f"Bearer {key}"},
        {
            "model": "gpt-image-2",
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "n": 1,
        },
    )
    if "data" not in resp or not resp["data"]:
        sys.exit(f"OpenAI returned no image: {json.dumps(resp, indent=2)[:500]}")
    b64 = resp["data"][0].get("b64_json")
    if not b64:
        # Some accounts/regions still return a URL; fetch it.
        url = resp["data"][0].get("url")
        if not url:
            sys.exit(f"OpenAI response missing b64_json and url: {resp}")
        with urllib.request.urlopen(url, timeout=300) as r:
            out.write_bytes(r.read())
    else:
        out.write_bytes(base64.b64decode(b64))
    return out


def generate_gemini(prompt: str, out: Path) -> Path:
    key = resolve_key("GOOGLE_API_KEY", "google_api_key")
    if not key:
        sys.exit("GOOGLE_API_KEY not set (env or ~/.ink/config.json).")
    resp = post_json(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent",
        {"x-goog-api-key": key},
        {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
        },
    )
    candidates = resp.get("candidates") or []
    if not candidates:
        sys.exit(f"Gemini returned no candidates: {json.dumps(resp, indent=2)[:500]}")
    for part in candidates[0].get("content", {}).get("parts", []):
        inline = part.get("inlineData") or part.get("inline_data")
        if inline and "data" in inline:
            out.write_bytes(base64.b64decode(inline["data"]))
            return out
    sys.exit(f"Gemini response had no inline image data: {resp}")


def main() -> None:
    p = argparse.ArgumentParser(description="Generate one image via Gemini or OpenAI gpt-image-2.")
    p.add_argument("prompt", help="Text prompt for the image.")
    p.add_argument("--provider", choices=("openai", "gemini"), default=None,
                   help="Force a provider; default picks based on configured keys.")
    p.add_argument("--out", required=True, help="Output path for the PNG.")
    p.add_argument("--size", default="1024x1024",
                   help="OpenAI only: 1024x1024 | 1024x1536 | 1536x1024 | auto. Ignored by Gemini.")
    p.add_argument("--quality", default="medium", choices=("low", "medium", "high"),
                   help="OpenAI only. Ignored by Gemini.")
    args = p.parse_args()

    provider = pick_provider(args.provider)
    out = Path(args.out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)

    if provider == "openai":
        generate_openai(args.prompt, args.size, args.quality, out)
    else:
        generate_gemini(args.prompt, out)

    print(f"wrote {out}  (provider={provider}"
          + (f", quality={args.quality}, size={args.size}" if provider == "openai" else "")
          + ")")


if __name__ == "__main__":
    main()
