#!/usr/bin/env python3
"""Assemble a self-contained HTML file from a template, the print engine, and a pieces file.

usage: build.py gallery|final <pieces.js> <out.html> [--engine other-engine.js]

The output has no external requests: engine and pieces are inlined.
"""
import sys, pathlib

def main():
    a = sys.argv[1:]
    if len(a) < 3 or a[0] not in ("gallery", "final"):
        sys.exit(__doc__)
    root = pathlib.Path(__file__).resolve().parent.parent / "assets"
    engine = root / "engine.js"
    if "--engine" in a:
        engine = pathlib.Path(a[a.index("--engine") + 1])
    tpl = (root / f"{a[0]}-template.html").read_text()
    pieces = pathlib.Path(a[1]).read_text()
    if "</script" in pieces.lower():
        sys.exit("pieces file must not contain </script>")
    out = tpl.replace("/*__ENGINE__*/", engine.read_text()).replace("/*__PIECES__*/", pieces)
    pathlib.Path(a[2]).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a[2]).write_text(out)
    print(f"wrote {a[2]} ({len(out)//1024} KB)")

if __name__ == "__main__":
    main()
