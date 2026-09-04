from __future__ import annotations

import argparse

from chordinate.apply import apply_to_path
from chordinate.destinations.base import Destination
from chordinate.destinations.jetbrains import JetBrainsDestination
from chordinate.destinations.obsidian import ObsidianDestination
from chordinate.destinations.vscode import VSCodeDestination
from chordinate.model import load_bindings


def _apply_destination(destination: Destination, content: str) -> None:
    target_paths = destination.target_paths()
    if not target_paths:
        print(f"! no {destination.name} targets found")
        return

    for path in target_paths:
        result = apply_to_path(content, path)
        if result.action == "skipped":
            print(f"= already up to date: {path}")
        elif result.action == "backed_up":
            print(f"~ backed up {path} -> {result.backup_path}, then wrote")
        else:
            print(f"+ wrote: {path}")

    if destination.name == "jetbrains":
        print('  → then: Settings → Keymap → select "Personal"')


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="chordinate")
    parser.add_argument(
        "--apply", action="store_true", help="write to live editor config paths"
    )
    args = parser.parse_args(argv)

    bindings = load_bindings()
    destinations: list[Destination] = [
        JetBrainsDestination(),
        VSCodeDestination(),
        ObsidianDestination(),
    ]

    for destination in destinations:
        content = destination.render(bindings)
        print(f"# {destination.name}")
        if args.apply:
            _apply_destination(destination, content)
        else:
            print(content)


if __name__ == "__main__":
    main()
