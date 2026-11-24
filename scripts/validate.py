#!/usr/bin/env python3
"""Lint every skill in skills/ against the conventions this repo follows.

Checks (errors fail the run, warnings do not):
  - SKILL.md starts with YAML frontmatter on line 1
  - name matches the folder, is lowercase-hyphen, and is 64 chars or fewer
  - description exists and is 1,024 chars or fewer (Agent Skills spec), and
    warns past 1,536 combined with when_to_use (Claude Code listing cap)
  - SKILL.md is 500 lines or fewer (warning)
  - no absolute home-directory paths (/Users/..., /home/...)
  - relative markdown links and `references/…`-style paths resolve
  - skills that set disable-model-invocation also ship agents/openai.yaml
    with allow_implicit_invocation: false, so Codex behaves the same way
  - no .DS_Store or __pycache__ committed

Standard library only. Usage: python3 scripts/validate.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
errors, warnings = [], []


def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            value = m.group(2).strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1].replace('\\"', '"')
            fields[m.group(1)] = value
    return fields


for skill in sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir()):
    name = skill.name
    md = skill / "SKILL.md"
    if not md.exists():
        errors.append(f"{name}: missing SKILL.md")
        continue
    text = md.read_text(encoding="utf-8")
    fm = frontmatter(text)
    if fm is None:
        errors.append(f"{name}: SKILL.md must open with --- frontmatter on line 1")
        continue
    if fm.get("name") != name:
        errors.append(f"{name}: frontmatter name {fm.get('name')!r} does not match folder")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
        errors.append(f"{name}: name must be lowercase-hyphen and at most 64 chars")
    desc = fm.get("description", "")
    if not desc:
        errors.append(f"{name}: missing description")
    elif len(desc) > 1024:
        errors.append(f"{name}: description is {len(desc)} chars (max 1,024)")
    if len(desc) + len(fm.get("when_to_use", "")) > 1536:
        warnings.append(f"{name}: description + when_to_use exceeds the 1,536-char listing cap")
    lines = text.count("\n") + 1
    if lines > 500:
        warnings.append(f"{name}: SKILL.md is {lines} lines (aim for 500 or fewer; move detail to references/)")
    if re.search(r"(/Users/|/home/)[A-Za-z0-9_.-]+/", text):
        errors.append(f"{name}: SKILL.md contains an absolute home-directory path")
    for target in re.findall(r"\]\(((?!https?://|#|mailto:)[^)\s]+)\)", text):
        if not (skill / target.split("#")[0]).exists():
            errors.append(f"{name}: broken relative link {target}")
    manual = fm.get("disable-model-invocation", "").lower() in {"true", "yes", "on", "1"}
    yaml = skill / "agents" / "openai.yaml"
    if manual and not (
        yaml.exists() and re.search(r"allow_implicit_invocation:\s*false", yaml.read_text())
    ):
        errors.append(
            f"{name}: disable-model-invocation is set but agents/openai.yaml does not set "
            "policy.allow_implicit_invocation: false (Codex would still auto-invoke it)"
        )

for junk in list(ROOT.rglob(".DS_Store")) + list(ROOT.rglob("__pycache__")):
    if ".git" not in junk.parts:
        errors.append(f"remove {junk.relative_to(ROOT)}")

for w in warnings:
    print(f"warning: {w}")
for e in errors:
    print(f"error: {e}")
print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
sys.exit(1 if errors else 0)
