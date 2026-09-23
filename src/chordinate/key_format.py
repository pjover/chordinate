"""Canonical key notation ("ctrl+shift+plus") translated to each app's own syntax.

The three target apps do not share a key-naming convention — confirmed against
each app's actual source/docs rather than assumed. See docs/design in the
parent project for the reference table.
"""

from __future__ import annotations

_JETBRAINS_MODIFIER_NAMES = {"ctrl": "control", "alt": "alt", "shift": "shift"}

_JETBRAINS_KEY_NAMES = {
    "up": "UP",
    "down": "DOWN",
    "left": "LEFT",
    "right": "RIGHT",
    "enter": "ENTER",
    "tab": "TAB",
    "escape": "ESCAPE",
    "plus": "EQUALS",
    "minus": "MINUS",
    "/": "SLASH",
    "\\": "BACK_SLASH",
    "numpad_divide": "DIVIDE",
    "numpad_add": "ADD",
    "numpad_subtract": "SUBTRACT",
}

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
    "plus": "+",
    "minus": "-",
}


_DISPLAY_NAMES = {
    "up": "↑",
    "down": "↓",
    "left": "←",
    "right": "→",
    "numpad_divide": "Numpad÷",
    "numpad_add": "Numpad+",
    "numpad_subtract": "Numpad−",
}


def _split(key: str) -> tuple[list[str], str]:
    *modifiers, base = key.lower().split("+")
    return modifiers, base


def to_jetbrains(key: str) -> str:
    modifiers, base = _split(key)
    modifier_names = [_JETBRAINS_MODIFIER_NAMES[m] for m in modifiers]
    base_name = _JETBRAINS_KEY_NAMES.get(base, base.upper())
    return " ".join([*modifier_names, base_name])


def to_vscode(key: str) -> str:
    modifiers, base = _split(key)
    base_name = _VSCODE_KEY_NAMES.get(base, base)
    return "+".join([*modifiers, base_name])


def to_obsidian(key: str, literal_ctrl: bool = False) -> tuple[list[str], str]:
    modifiers, base = _split(key)
    modifier_names = [
        ("Ctrl" if literal_ctrl else "Mod") if m == "ctrl" else m.capitalize() for m in modifiers
    ]
    base_name = _OBSIDIAN_KEY_NAMES.get(base, base.upper() if len(base) == 1 else base.capitalize())
    return modifier_names, base_name


def to_display(key: str) -> list[str]:
    """Human-readable key names for printed material, e.g. ["Ctrl", "Shift", "↑"]."""
    return [
        _DISPLAY_NAMES.get(part, part.upper() if len(part) == 1 else part.capitalize())
        for part in key.lower().split("+")
    ]
