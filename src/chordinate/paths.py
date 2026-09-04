from __future__ import annotations

import platform
from pathlib import Path


class UnsupportedOSError(RuntimeError):
    pass


def _config_base() -> Path:
    system = platform.system()
    if system == "Darwin":
        return Path.home() / "Library" / "Application Support"
    if system == "Linux":
        return Path.home() / ".config"
    raise UnsupportedOSError(f"Unsupported OS: {system}")


def jetbrains_config_dir() -> Path:
    return _config_base() / "JetBrains"


def vscode_user_dir() -> Path:
    return _config_base() / "Code" / "User"


def obsidian_registry_path() -> Path:
    return _config_base() / "obsidian" / "obsidian.json"
