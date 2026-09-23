"""Printable HTML cheat sheet: every binding's action and chord, grouped by topic."""

from __future__ import annotations

import html
import sys
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path

from chordinate.key_format import to_display
from chordinate.model import Binding, load_bindings

GROUP_ORDER = ["Editing", "Markdown", "App / window", "Obsidian only"]
DEFAULT_OUTPUT = Path("cheatsheet.html")


@dataclass(frozen=True)
class Row:
    label: str
    keys: list[str]
    note: str | None = None


def chord_keys(binding: Binding) -> list[str]:
    """The keys to print for a binding, in canonical notation, without duplicates.

    An explicit cheatsheet `keys` list wins; otherwise keys are collected from every
    app's entries (VS Code `-command` removals skipped), falling back to the reserved key.
    """
    if binding.cheatsheet.keys:
        return binding.cheatsheet.keys
    keys = [key for entry in binding.jetbrains for key in entry.keys]
    keys += [entry.key for entry in binding.vscode if not entry.command.startswith("-")]
    keys += [entry.key for entry in binding.obsidian]
    if not keys and binding.reserved_key:
        keys = [binding.reserved_key]
    return list(dict.fromkeys(keys))


def to_row(binding: Binding) -> Row:
    note = binding.cheatsheet.note
    if note is None and binding.reserved_key and not binding.cheatsheet.keys:
        note = "reserved"
    return Row(label=binding.cheatsheet.label or binding.action, keys=chord_keys(binding), note=note)


def group_rows(bindings: list[Binding]) -> dict[str, list[Row]]:
    groups: dict[str, list[Row]] = {name: [] for name in GROUP_ORDER}
    for binding in bindings:
        if binding.cheatsheet.hidden:
            continue
        groups.setdefault(binding.cheatsheet.group, []).append(to_row(binding))
    return {name: rows for name, rows in groups.items() if rows}


def _render_chord(keys: list[str]) -> str:
    combos = []
    previous_modifiers: list[str] | None = None
    for key in keys:
        *modifiers, base = to_display(key)
        # "Ctrl+C / X / V": repeat modifiers only when they change.
        parts = [base] if modifiers == previous_modifiers else [*modifiers, base]
        previous_modifiers = modifiers
        caps = '<span class="plus">+</span>'.join(f"<kbd>{html.escape(p)}</kbd>" for p in parts)
        combos.append(f'<span class="combo">{caps}</span>')
    return '<span class="slash">/</span>'.join(combos)


def _render_label(label: str) -> str:
    escaped = html.escape(label)
    return escaped.replace("`code`", "<code>`code`</code>")


def _render_group(name: str, rows: list[Row]) -> str:
    body = []
    for row in rows:
        note = f'<span class="note">{html.escape(row.note)}</span>' if row.note else ""
        body.append(
            f'<tr><th scope="row">{_render_label(row.label)}{note}</th>'
            f"<td>{_render_chord(row.keys)}</td></tr>"
        )
    return (
        f'<section class="group"><h2>{html.escape(name)}<span class="count">{len(rows)}</span></h2>'
        f'<table><colgroup><col><col class="c-chord"></colgroup><tbody>{"".join(body)}</tbody></table>'
        "</section>"
    )


def render(bindings: list[Binding]) -> str:
    groups = group_rows(bindings)
    template = files("chordinate.data").joinpath("cheatsheet.html").read_text(encoding="utf-8")
    sections = "\n".join(_render_group(name, rows) for name, rows in groups.items())
    count = sum(len(rows) for rows in groups.values())
    return template.replace("{{count}}", str(count)).replace("{{sections}}", sections)


def main(argv: list[str] | None = None) -> None:
    args = sys.argv[1:] if argv is None else argv
    output = Path(args[0]) if args else DEFAULT_OUTPUT
    output.write_text(render(load_bindings()), encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
