from __future__ import annotations

import json
from dataclasses import dataclass, field
from importlib.resources import files


@dataclass(frozen=True)
class JetBrainsEntry:
    action_id: str
    keys: list[str]


@dataclass(frozen=True)
class VSCodeEntry:
    command: str
    key: str
    when: str | None = None


@dataclass(frozen=True)
class ObsidianEntry:
    command_id: str
    key: str
    literal_ctrl: bool = False


@dataclass(frozen=True)
class Binding:
    id: str
    action: str
    jetbrains: list[JetBrainsEntry] = field(default_factory=list)
    vscode: list[VSCodeEntry] = field(default_factory=list)
    obsidian: list[ObsidianEntry] = field(default_factory=list)
    note: str | None = None
    reserved_key: str | None = None


def _load_jetbrains(raw: dict) -> list[JetBrainsEntry]:
    entries = raw.get("jetbrains", {}).get("entries", [])
    return [JetBrainsEntry(action_id=e["action_id"], keys=list(e["keys"])) for e in entries]


def _load_vscode(raw: dict) -> list[VSCodeEntry]:
    entries = raw.get("vscode", {}).get("entries", [])
    return [VSCodeEntry(command=e["command"], key=e["key"], when=e.get("when")) for e in entries]


def _load_obsidian(raw: dict) -> list[ObsidianEntry]:
    entries = raw.get("obsidian", {}).get("entries", [])
    return [
        ObsidianEntry(
            command_id=e["command_id"], key=e["key"], literal_ctrl=e.get("literal_ctrl", False)
        )
        for e in entries
    ]


def _load_binding(raw: dict) -> Binding:
    return Binding(
        id=raw["id"],
        action=raw["action"],
        jetbrains=_load_jetbrains(raw),
        vscode=_load_vscode(raw),
        obsidian=_load_obsidian(raw),
        note=raw.get("note"),
        reserved_key=raw.get("reserved_key"),
    )


def load_bindings() -> list[Binding]:
    text = files("chordinate.data").joinpath("keymap.json").read_text(encoding="utf-8")
    data = json.loads(text)
    return [_load_binding(raw) for raw in data["bindings"]]
