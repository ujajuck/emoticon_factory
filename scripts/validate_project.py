#!/usr/bin/env python3
"""Validate an emoticon factory project JSON file.

The validator intentionally uses only the Python standard library so it can run
in minimal local agent environments without installing dependencies.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{6}$")
PROJECT_STATUSES = {"planning", "design", "coloring", "review", "packaged"}
EMOJI_STATUSES = {"planned", "sketched", "lined", "colored", "approved"}


def fail(errors: list[str], path: str, message: str) -> None:
    errors.append(f"{path}: {message}")


def require_object(errors: list[str], data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        fail(errors, key, "must be an object")
        return {}
    return value


def require_string(errors: list[str], data: dict[str, Any], key: str, path: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        fail(errors, f"{path}.{key}", "must be a non-empty string")
        return ""
    return value


def require_string_array(errors: list[str], data: dict[str, Any], key: str, path: str, *, min_items: int = 0) -> None:
    value = data.get(key)
    if not isinstance(value, list) or len(value) < min_items or not all(isinstance(item, str) and item.strip() for item in value):
        fail(errors, f"{path}.{key}", f"must be an array of at least {min_items} non-empty string(s)")


def validate_project(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["$: must be an object"]

    project = require_object(errors, data, "project")
    require_string(errors, project, "name", "project")
    target_count = project.get("target_count")
    if not isinstance(target_count, int) or not 24 <= target_count <= 32:
        fail(errors, "project.target_count", "must be an integer between 24 and 32")
    status = project.get("status")
    if status not in PROJECT_STATUSES:
        fail(errors, "project.status", f"must be one of {sorted(PROJECT_STATUSES)}")

    market = require_object(errors, data, "market_research")
    require_string(errors, market, "target", "market_research")
    require_string(errors, market, "theme", "market_research")
    require_string_array(errors, market, "keywords", "market_research", min_items=1)

    character = require_object(errors, data, "character")
    for key in ("name", "species", "style"):
        require_string(errors, character, key, "character")
    require_string_array(errors, character, "personality", "character", min_items=1)

    palette = require_object(errors, character, "palette")
    for key in ("main", "sub", "accent"):
        color = palette.get(key)
        if not isinstance(color, str) or not HEX_COLOR.match(color):
            fail(errors, f"character.palette.{key}", "must be a #RRGGBB HEX color")

    ratios = require_object(errors, character, "ratios")
    for key in ("face_ratio", "eye_ratio", "body_ratio"):
        value = ratios.get(key)
        if not isinstance(value, (int, float)) or not 0 <= value <= 1:
            fail(errors, f"character.ratios.{key}", "must be a number from 0 to 1")

    brand = require_object(errors, data, "brand_guide")
    require_string_array(errors, brand, "must_have", "brand_guide")
    require_string_array(errors, brand, "must_not_have", "brand_guide")
    require_string_array(errors, brand, "reference_images", "brand_guide")

    emoji_set = data.get("emoji_set")
    if not isinstance(emoji_set, list) or not 24 <= len(emoji_set) <= 32:
        fail(errors, "emoji_set", "must contain 24 to 32 items")
        emoji_set = []
    if isinstance(target_count, int) and isinstance(emoji_set, list) and target_count != len(emoji_set):
        fail(errors, "project.target_count", "must match emoji_set item count")

    seen_ids: set[str] = set()
    for index, item in enumerate(emoji_set):
        item_path = f"emoji_set[{index}]"
        if not isinstance(item, dict):
            fail(errors, item_path, "must be an object")
            continue
        emoji_id = require_string(errors, item, "id", item_path)
        if emoji_id in seen_ids:
            fail(errors, f"{item_path}.id", "must be unique")
        seen_ids.add(emoji_id)
        require_string(errors, item, "situation", item_path)
        require_string(errors, item, "emotion", item_path)
        if item.get("status") not in EMOJI_STATUSES:
            fail(errors, f"{item_path}.status", f"must be one of {sorted(EMOJI_STATUSES)}")

    quality = require_object(errors, data, "quality_gates")
    for gate_name in ("planning", "design", "coloring"):
        gate = quality.get(gate_name)
        if not isinstance(gate, dict):
            fail(errors, f"quality_gates.{gate_name}", "must be an object")
            continue
        if not isinstance(gate.get("approved"), bool):
            fail(errors, f"quality_gates.{gate_name}.approved", "must be a boolean")
        require_string_array(errors, gate, "feedback", f"quality_gates.{gate_name}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an emoticon factory project JSON file.")
    parser.add_argument("project_json", type=Path, help="Path to a project JSON file")
    args = parser.parse_args()

    try:
        data = json.loads(args.project_json.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"Could not read {args.project_json}: {exc}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON in {args.project_json}: {exc}", file=sys.stderr)
        return 1

    errors = validate_project(data)
    if errors:
        print(f"{args.project_json} is invalid:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"{args.project_json} is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
