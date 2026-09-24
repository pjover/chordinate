from __future__ import annotations

import json
from pathlib import Path

from chordinate.key_format import to_obsidian
from chordinate.model import Binding
from chordinate.paths import obsidian_registry_path


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

    def target_paths(self) -> list[Path]:
        registry_path = obsidian_registry_path()
        if not registry_path.is_file():
            return []
        try:
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return []
        paths = []
        for vault in registry.get("vaults", {}).values():
            vault_path = Path(vault["path"])
            if vault_path.is_dir():
                paths.append(vault_path / ".obsidian" / "hotkeys.json")
        return paths
