from __future__ import annotations

import difflib
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class ApplyResult:
    path: Path
    action: str
    backup_path: Path | None = None
    lines_added: int = 0
    lines_removed: int = 0


def apply_to_path(content: str, path: Path) -> ApplyResult:
    path.parent.mkdir(parents=True, exist_ok=True)

    old_text = path.read_text(encoding="utf-8") if path.is_file() else None

    if old_text is not None and old_text == content:
        return ApplyResult(path=path, action="skipped")

    backup_path = None
    lines_added = 0
    lines_removed = 0
    if path.exists():
        if old_text is not None:
            diff_lines = list(
                difflib.unified_diff(old_text.splitlines(), content.splitlines(), lineterm="")
            )
            lines_removed = sum(
                1 for line in diff_lines if line.startswith("-") and not line.startswith("---")
            )
            lines_added = sum(
                1 for line in diff_lines if line.startswith("+") and not line.startswith("+++")
            )
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = path.with_name(f"{path.name}.bak-{timestamp}")
        path.rename(backup_path)

    path.write_text(content, encoding="utf-8")

    action = "backed_up" if backup_path else "written"
    return ApplyResult(
        path=path,
        action=action,
        backup_path=backup_path,
        lines_added=lines_added,
        lines_removed=lines_removed,
    )
