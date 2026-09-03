from __future__ import annotations

from typing import Protocol

from chordinate.model import Binding


class Destination(Protocol):
    name: str

    def render(self, bindings: list[Binding]) -> str: ...
