from __future__ import annotations

import json
from pathlib import Path

from chordinate.key_format import to_zed
from chordinate.model import Binding
from chordinate.paths import zed_config_dir


class ZedDestination:
    name = "zed"

    def render(self, bindings: list[Binding]) -> str:
        # One section per context, in first-seen order. Zed layers this file over
        # its defaults; a None action renders as null, unbinding the key there.
        sections: dict[str | None, dict] = {}
        for binding in bindings:
            for entry in binding.zed:
                sections.setdefault(entry.context, {})[to_zed(entry.key)] = entry.action
        keymap = []
        for context, keys in sections.items():
            section = {"context": context} if context else {}
            section["bindings"] = keys
            keymap.append(section)
        return json.dumps(keymap, indent=2) + "\n"

    def merge(self, rendered: str, current: str | None) -> str:
        return rendered  # chordinate owns the whole file

    def target_paths(self) -> list[Path]:
        config_dir = zed_config_dir()
        if not config_dir.is_dir():
            return []
        return [config_dir / "keymap.json"]
