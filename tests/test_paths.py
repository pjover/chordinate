import platform

import pytest

from chordinate.paths import (
    UnsupportedOSError,
    jetbrains_config_dir,
    obsidian_registry_path,
    vscode_user_dir,
)


def test_jetbrains_config_dir_on_linux(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setenv("HOME", str(tmp_path))

    assert jetbrains_config_dir() == tmp_path / ".config" / "JetBrains"


def test_jetbrains_config_dir_on_macos(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setenv("HOME", str(tmp_path))

    assert jetbrains_config_dir() == tmp_path / "Library" / "Application Support" / "JetBrains"


def test_vscode_user_dir_on_linux(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setenv("HOME", str(tmp_path))

    assert vscode_user_dir() == tmp_path / ".config" / "Code" / "User"


def test_vscode_user_dir_on_macos(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setenv("HOME", str(tmp_path))

    expected = tmp_path / "Library" / "Application Support" / "Code" / "User"
    assert vscode_user_dir() == expected


def test_obsidian_registry_path_on_linux(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setenv("HOME", str(tmp_path))

    assert obsidian_registry_path() == tmp_path / ".config" / "obsidian" / "obsidian.json"


def test_obsidian_registry_path_on_macos(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setenv("HOME", str(tmp_path))

    expected = tmp_path / "Library" / "Application Support" / "obsidian" / "obsidian.json"
    assert obsidian_registry_path() == expected


def test_unsupported_os_raises(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Windows")

    with pytest.raises(UnsupportedOSError):
        jetbrains_config_dir()
