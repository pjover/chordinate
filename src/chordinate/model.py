from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from importlib.resources import files
from pathlib import Path


@dataclass(frozen=True)
class VSCodeEntry:
    command: str
    key: str
    when: str | None = None


@dataclass(frozen=True)
class ObsidianEntry:
    command_id: str
    key: str | None = None


@dataclass(frozen=True)
class ZedEntry:
    key: str
    # "ns::Action", ["ns::Action", args], or None to unbind the key in `context`.
    action: str | list | None
    context: str | None = None


@dataclass(frozen=True)
class FreshEntry:
    key: str
    # A Fresh action name; "unbind" removes the keymap's own binding on `key`.
    action: str
    when: str | None = None
    args: dict | None = None


@dataclass(frozen=True)
class CheatSheetEntry:
    group: str = "Other"
    label: str | None = None
    keys: list[str] = field(default_factory=list)
    note: str | None = None
    hidden: bool = False


@dataclass(frozen=True)
class Binding:
    id: str
    action: str
    vscode: list[VSCodeEntry] = field(default_factory=list)
    obsidian: list[ObsidianEntry] = field(default_factory=list)
    zed: list[ZedEntry] = field(default_factory=list)
    fresh: list[FreshEntry] = field(default_factory=list)
    note: str | None = None
    reserved_key: str | None = None
    cheatsheet: CheatSheetEntry = field(default_factory=CheatSheetEntry)


def _load_vscode(raw: dict) -> list[VSCodeEntry]:
    entries = raw.get("vscode", {}).get("entries", [])
    return [VSCodeEntry(command=e["command"], key=e["key"], when=e.get("when")) for e in entries]


def _load_obsidian(raw: dict) -> list[ObsidianEntry]:
    entries = raw.get("obsidian", {}).get("entries", [])
    return [
        ObsidianEntry(command_id=e["command_id"], key=e.get("key"))
        for e in entries
    ]


def _load_zed(raw: dict) -> list[ZedEntry]:
    entries = raw.get("zed", {}).get("entries", [])
    return [ZedEntry(key=e["key"], action=e["action"], context=e.get("context")) for e in entries]


def _load_fresh(raw: dict) -> list[FreshEntry]:
    entries = raw.get("fresh", {}).get("entries", [])
    return [
        FreshEntry(key=e["key"], action=e["action"], when=e.get("when"), args=e.get("args"))
        for e in entries
    ]


def _load_cheatsheet(raw: dict) -> CheatSheetEntry:
    entry = raw.get("cheatsheet", {})
    if entry is False:
        return CheatSheetEntry(hidden=True)
    return CheatSheetEntry(
        group=entry.get("group", "Other"),
        label=entry.get("label"),
        keys=list(entry.get("keys", [])),
        note=entry.get("note"),
    )


def _load_binding(raw: dict) -> Binding:
    return Binding(
        id=raw["id"],
        action=raw["action"],
        vscode=_load_vscode(raw),
        obsidian=_load_obsidian(raw),
        zed=_load_zed(raw),
        fresh=_load_fresh(raw),
        note=raw.get("note"),
        reserved_key=raw.get("reserved_key"),
        cheatsheet=_load_cheatsheet(raw),
    )


def _config_search_paths() -> list[Path]:
    paths = []
    chordinate_home = os.environ.get("CHORDINATE_HOME")
    if chordinate_home:
        paths.append(Path(chordinate_home) / "keymap.json")
    paths.append(Path.cwd() / "keymap.json")
    paths.append(Path.home() / ".config" / "chordinate" / "keymap.json")
    return paths


def _load_config_text() -> str:
    for path in _config_search_paths():
        if path.is_file():
            return path.read_text(encoding="utf-8")
    return files("chordinate.data").joinpath("keymap.json").read_text(encoding="utf-8")


def load_bindings() -> list[Binding]:
    text = _load_config_text()
    data = json.loads(text)
    return [_load_binding(raw) for raw in data["bindings"]]
