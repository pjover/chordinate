from __future__ import annotations

import json
from pathlib import Path

from chordinate.key_format import to_vscode
from chordinate.model import Binding
from chordinate.paths import vscode_user_dir


class VSCodeDestination:
    name = "vscode"

    def render(self, bindings: list[Binding]) -> str:
        entries = []
        for binding in bindings:
            for entry in binding.vscode:
                item = {"key": to_vscode(entry.key), "command": entry.command}
                if entry.when:
                    item["when"] = entry.when
                entries.append(item)
        return json.dumps(entries, indent=4) + "\n"

    def target_paths(self) -> list[Path]:
        user_dir = vscode_user_dir()
        if not user_dir.parent.is_dir():
            return []
        return [user_dir / "keybindings.json"]
