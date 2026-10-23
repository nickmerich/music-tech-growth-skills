#!/usr/bin/env python3
"""Validate every skills/*/SKILL.md against the Agent Skills format.

Checks: frontmatter present, name rules, name matches folder, description length,
body under 500 lines, relative links resolve, and no em dashes (house style).
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
errors = []

for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
    folder = skill.parent.name
    text = skill.read_text()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        errors.append(f"{folder}: missing frontmatter")
        continue
    fm, body = m.groups()
    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    desc = re.search(r"^description:\s*(.+)$", fm, re.M)
    if not name or not NAME.match(name.group(1).strip()) or len(name.group(1).strip()) > 64:
        errors.append(f"{folder}: invalid name")
    elif name.group(1).strip() != folder:
        errors.append(f"{folder}: name does not match folder")
    if not desc or not (1 <= len(desc.group(1).strip()) <= 1024):
        errors.append(f"{folder}: description missing or over 1024 chars")
    if len(body.splitlines()) > 500:
        errors.append(f"{folder}: body over 500 lines")

for md in ROOT.rglob("*.md"):
    t = md.read_text()
    if "\u2014" in t:
        errors.append(f"{md.relative_to(ROOT)}: contains an em dash")
    for link in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", t):
        if link.startswith(("http", "mailto:")):
            continue
        if not (md.parent / link).exists():
            errors.append(f"{md.relative_to(ROOT)}: broken link {link}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: {len(list((ROOT / 'skills').glob('*/SKILL.md')))} skills valid")
