from __future__ import annotations

import json

from chordinate.key_format import to_obsidian
from chordinate.model import Binding


class ObsidianDestination:
    name = "obsidian"

    def render(self, bindings: list[Binding]) -> str:
        hotkeys: dict[str, list[dict]] = {}
        for binding in bindings:
            for entry in binding.obsidian:
                modifiers, key = to_obsidian(entry.key, entry.literal_ctrl)
                hotkeys.setdefault(entry.command_id, [])
                hotkeys[entry.command_id].append({"modifiers": modifiers, "key": key})
        return json.dumps(hotkeys, indent=2) + "\n"
