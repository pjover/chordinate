from __future__ import annotations

from pathlib import Path
from typing import Protocol

from chordinate.model import Binding


class MergeError(ValueError):
    """The current file at a target can't be merged with the render; leave it alone."""


class Destination(Protocol):
    name: str

    def render(self, bindings: list[Binding]) -> str: ...

    def merge(self, rendered: str, current: str | None) -> str:
        """The content to write to a target whose current text is `current` (None if absent)."""
        ...

    def target_paths(self) -> list[Path]: ...
