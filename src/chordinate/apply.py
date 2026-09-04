from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class ApplyResult:
    path: Path
    action: str
    backup_path: Path | None = None


def apply_to_path(content: str, path: Path) -> ApplyResult:
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.is_file() and path.read_text(encoding="utf-8") == content:
        return ApplyResult(path=path, action="skipped")

    backup_path = None
    if path.exists():
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = path.with_name(f"{path.name}.bak-{timestamp}")
        path.rename(backup_path)

    path.write_text(content, encoding="utf-8")

    action = "backed_up" if backup_path else "written"
    return ApplyResult(path=path, action=action, backup_path=backup_path)
