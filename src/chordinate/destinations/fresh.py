from __future__ import annotations

import json
from pathlib import Path

from chordinate.destinations.base import MergeError
from chordinate.key_format import to_fresh
from chordinate.model import Binding
from chordinate.paths import fresh_config_dir


class FreshDestination:
    """Fresh keeps keybindings inside its general config.json, next to settings it
    rewrites itself, so chordinate owns only the "keybindings" list in that file."""

    name = "fresh"

    def render(self, bindings: list[Binding]) -> str:
        keybindings = []
        for binding in bindings:
            for entry in binding.fresh:
                modifiers, key = to_fresh(entry.key)
                item: dict = {"key": key, "modifiers": modifiers, "action": entry.action}
                if entry.args:
                    item["args"] = entry.args
                if entry.when:
                    item["when"] = entry.when
                keybindings.append(item)
        return json.dumps({"keybindings": keybindings}, indent=2) + "\n"

    def merge(self, rendered: str, current: str | None) -> str:
        if current is None or not current.strip():
            return rendered
        try:
            config = json.loads(current)
        except json.JSONDecodeError as error:
            # Fresh accepts JSONC; rewriting it would drop the user's comments.
            raise MergeError(
                f"not plain JSON ({error}); remove comments and trailing commas, then re-apply"
            ) from error
        if not isinstance(config, dict):
            raise MergeError("top level is not a JSON object")
        config["keybindings"] = json.loads(rendered)["keybindings"]
        return json.dumps(config, indent=2, ensure_ascii=False) + "\n"

    def target_paths(self) -> list[Path]:
        config_dir = fresh_config_dir()
        if not config_dir.is_dir():
            return []
        return [config_dir / "config.json"]
