from __future__ import annotations

from chordinate.destinations.base import Destination
from chordinate.destinations.jetbrains import JetBrainsDestination
from chordinate.destinations.obsidian import ObsidianDestination
from chordinate.destinations.vscode import VSCodeDestination
from chordinate.model import load_bindings


def main() -> None:
    bindings = load_bindings()
    destinations: list[Destination] = [
        JetBrainsDestination(),
        VSCodeDestination(),
        ObsidianDestination(),
    ]

    for destination in destinations:
        print(f"# {destination.name}")
        print(destination.render(bindings))


if __name__ == "__main__":
    main()
