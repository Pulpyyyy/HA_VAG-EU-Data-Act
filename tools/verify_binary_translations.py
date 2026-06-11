#!/usr/bin/env python3
"""Verify every curated binary sensor has multilingual name labels."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(ROOT / "tools"))

from _loader import load_modules  # noqa: E402
from entity_translation_catalog import LANGS, build_entity_block  # noqa: E402
from binary_name_labels import NAME_LABELS  # noqa: E402

data = load_modules("data")["data"]


def main() -> int:
    missing: list[str] = []
    for binary in list(data.CURATED_BINARY_DOTTED) + list(data.CURATED_BINARY_FLAT):
        key = data.curated_translation_key(binary.field_name)
        block = build_entity_block("en")["binary_sensor"]
        if key not in block:
            missing.append(f"{key} ({binary.field_name})")
        elif key not in NAME_LABELS:
            missing.append(f"{key} (no NAME_LABELS entry)")
    if missing:
        print("Missing translation keys:")
        for line in missing:
            print(f"  - {line}")
        return 1
    for lang in LANGS:
        count = len(build_entity_block(lang)["binary_sensor"])
        print(f"{lang}: {count} binary_sensor translations")
    print("OK: all curated binary sensors covered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
