#!/usr/bin/env python3
"""Create a high-density HyperFrames knowledge-whiteboard project."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


def project_slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "dense-whiteboard-video"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a dense HyperFrames whiteboard project without overwriting existing work."
    )
    parser.add_argument("target", type=Path, help="Destination project directory")
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    template = skill_root / "assets" / "project-template"
    target = args.target.expanduser().resolve()

    if not template.is_dir():
        raise SystemExit(f"Template not found: {template}")
    if target.exists() and any(target.iterdir()):
        raise SystemExit(f"Target must be absent or empty: {target}")

    target.mkdir(parents=True, exist_ok=True)
    shutil.copytree(template, target, dirs_exist_ok=True)

    slug = project_slug(target.name)
    package_path = target / "package.json"
    package = json.loads(package_path.read_text(encoding="utf-8"))
    package["name"] = slug
    package_path.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    meta_path = target / "meta.json"
    meta = {
        "id": slug,
        "name": target.name,
        "createdAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Created dense HyperFrames whiteboard project: {target}")
    print("Next: replace input/article.md, edit storyboard.json, generate text-free scene images, then run npm run voice")


if __name__ == "__main__":
    main()
