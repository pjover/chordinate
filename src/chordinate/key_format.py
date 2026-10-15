"""Canonical key notation ("ctrl+shift+plus") translated to each app's own syntax.

The target apps do not share a key-naming convention — confirmed against
each app's actual source/docs rather than assumed. See docs/design in the
parent project for the reference table.
"""

from __future__ import annotations

_VSCODE_KEY_NAMES = {
    "plus": "=",
    "minus": "-",
}

_OBSIDIAN_KEY_NAMES = {
    "up": "ArrowUp",
    "down": "ArrowDown",
    "left": "ArrowLeft",
    "right": "ArrowRight",
    "enter": "Enter",
    "tab": "Tab",
    "escape": "Escape",
    "pageup": "PageUp",
    "pagedown": "PageDown",
    "plus": "+",
    "minus": "-",
}

# Zed matches the character a key types, so plus is "+" (the unshifted key on a
# Spanish layout), not VS Code's US-position "=".
_ZED_KEY_NAMES = {
    "plus": "+",
    "minus": "-",
}


_DISPLAY_NAMES = {
    "up": "↑",
    "down": "↓",
    "left": "←",
    "right": "→",
    "pageup": "PgUp",
    "pagedown": "PgDn",
    "numpad_divide": "Numpad÷",
    "numpad_add": "Numpad+",
    "numpad_subtract": "Numpad−",
}


def _split(key: str) -> tuple[list[str], str]:
    *modifiers, base = key.lower().split("+")
    return modifiers, base


def to_vscode(key: str) -> str:
    modifiers, base = _split(key)
    base_name = _VSCODE_KEY_NAMES.get(base, base)
    return "+".join([*modifiers, base_name])


def to_obsidian(key: str) -> tuple[list[str], str]:
    # Literal "Ctrl", never "Mod": Mod is Cmd on macOS, while VS Code binds the
    # physical Ctrl key there. On Linux the two are the same key.
    modifiers, base = _split(key)
    modifier_names = [m.capitalize() for m in modifiers]
    base_name = _OBSIDIAN_KEY_NAMES.get(base, base.upper() if len(base) == 1 else base.capitalize())
    return modifier_names, base_name


def to_zed(key: str) -> str:
    # Zed joins modifiers with "-"; "minus" therefore renders as "ctrl--".
    modifiers, base = _split(key)
    base_name = _ZED_KEY_NAMES.get(base, base)
    return "-".join([*modifiers, base_name])


def to_display(key: str) -> list[str]:
    """Human-readable key names for printed material, e.g. ["Ctrl", "Shift", "↑"]."""
    return [
        _DISPLAY_NAMES.get(part, part.upper() if len(part) == 1 else part.capitalize())
        for part in key.lower().split("+")
    ]
