from __future__ import annotations

from xml.sax.saxutils import quoteattr

from chordinate.key_format import to_jetbrains
from chordinate.model import Binding


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
