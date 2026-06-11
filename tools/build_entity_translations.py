#!/usr/bin/env python3
"""Merge entity translation catalog into strings.json and translations/*.json."""

from __future__ import annotations

import json
from pathlib import Path

from entity_translation_catalog import LANGS, build_entity_block

ROOT = Path(__file__).resolve().parent.parent
COMPONENT = ROOT / "custom_components" / "cupra_eu_data_act"


def _merge(path: Path, lang: str) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    data["entity"] = build_entity_block(lang)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"updated {path.relative_to(ROOT)}")


def main() -> None:
    _merge(COMPONENT / "strings.json", "en")
    for lang in LANGS:
        _merge(COMPONENT / "translations" / f"{lang}.json", lang)


if __name__ == "__main__":
    main()
