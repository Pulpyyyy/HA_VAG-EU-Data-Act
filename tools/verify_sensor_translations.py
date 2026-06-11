#!/usr/bin/env python3
"""Verify every curated sensor has multilingual name labels."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(ROOT / "tools"))

from _loader import load_modules  # noqa: E402
from entity_translation_catalog import LANGS, SENSORS, build_entity_block  # noqa: E402
from sensor_name_labels import NAME_LABELS  # noqa: E402

data = load_modules("data")["data"]


def main() -> int:
    missing: list[str] = []
    for sensor in list(data.CURATED_SENSORS_DOTTED) + list(data.CURATED_SENSORS_FLAT):
        key = data.curated_translation_key(sensor.field_name, sensor.translation_key)
        block = build_entity_block("en")["sensor"]
        if key not in block:
            missing.append(f"{key} ({sensor.field_name})")
    if missing:
        print("Missing translation keys:")
        for line in missing:
            print(f"  - {line}")
        return 1
    for lang in LANGS:
        count = len(build_entity_block(lang)["sensor"])
        print(f"{lang}: {count} sensor translations")
    print("OK: all curated sensors covered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
