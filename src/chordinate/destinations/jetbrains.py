from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import quoteattr

from chordinate.key_format import to_jetbrains
from chordinate.model import Binding
from chordinate.paths import jetbrains_config_dir

_PRODUCT_PREFIXES = (
    "PyCharm",
    "IntelliJIdea",
    "IdeaIC",
    "Rider",
    "WebStorm",
    "GoLand",
    "CLion",
    "DataGrip",
    "RubyMine",
    "PhpStorm",
    "RustRover",
)


class JetBrainsDestination:
    name = "jetbrains"

    def render(self, bindings: list[Binding]) -> str:
        shortcuts_by_action: dict[str, list[str]] = {}
        for binding in bindings:
            for entry in binding.jetbrains:
                shortcuts_by_action.setdefault(entry.action_id, [])
                shortcuts_by_action[entry.action_id].extend(entry.keys)

        lines = ['<keymap version="1" name="Personal" parent="$default">']
        for action_id in sorted(shortcuts_by_action):
            lines.append(f"  <action id={quoteattr(action_id)}>")
            for key in shortcuts_by_action[action_id]:
                shortcut = to_jetbrains(key)
                lines.append(f"    <keyboard-shortcut first-keystroke={quoteattr(shortcut)} />")
            lines.append("  </action>")
        lines.append("</keymap>")
        return "\n".join(lines) + "\n"

    def target_paths(self) -> list[Path]:
        base = jetbrains_config_dir()
        if not base.is_dir():
            return []
        products = sorted(
            entry
            for entry in base.iterdir()
            if entry.is_dir() and entry.name.startswith(_PRODUCT_PREFIXES)
        )
        return [product / "keymaps" / "Personal.xml" for product in products]
