import json
import platform

import pytest

from chordinate.destinations.base import MergeError
from chordinate.destinations.fresh import FreshDestination
from chordinate.destinations.obsidian import ObsidianDestination
from chordinate.destinations.vscode import VSCodeDestination
from chordinate.destinations.zed import ZedDestination
from chordinate.model import Binding, FreshEntry, ObsidianEntry, VSCodeEntry, ZedEntry, load_bindings


def _binding(**kwargs) -> Binding:
    return Binding(id="test", action="Test", **kwargs)


def test_vscode_destination_renders_key_command_and_when():
    binding = _binding(
        vscode=[VSCodeEntry(command="editor.action.deleteLines", key="ctrl+y", when="textInputFocus")]
    )

    entries = VSCodeDestination().render([binding])

    assert '"key": "ctrl+y"' in entries
    assert '"command": "editor.action.deleteLines"' in entries
    assert '"when": "textInputFocus"' in entries


def test_vscode_destination_omits_when_if_absent():
    binding = _binding(vscode=[VSCodeEntry(command="editor.action.joinLines", key="ctrl+shift+j")])

    entries = VSCodeDestination().render([binding])

    assert '"when"' not in entries


def test_obsidian_destination_groups_entries_by_command_id():
    binding = _binding(
        obsidian=[
            ObsidianEntry(command_id="editor:copy", key="ctrl+c"),
        ]
    )

    hotkeys = ObsidianDestination().render([binding])

    assert '"editor:copy"' in hotkeys
    assert '"Ctrl"' in hotkeys
    assert '"C"' in hotkeys


def test_obsidian_entry_without_key_unbinds_the_command():
    binding = _binding(obsidian=[ObsidianEntry(command_id="file-explorer:new-file")])

    hotkeys = json.loads(ObsidianDestination().render([binding]))

    assert hotkeys == {"file-explorer:new-file": []}


def test_zed_destination_groups_by_context_in_first_seen_order():
    bindings = [
        _binding(zed=[ZedEntry(key="ctrl+y", action="editor::DeleteLine", context="Editor")]),
        _binding(
            zed=[
                ZedEntry(key="ctrl+r", action=None, context="Workspace"),
                ZedEntry(key="ctrl+d", action="editor::DuplicateSelection", context="Editor"),
                ZedEntry(key="ctrl+plus", action=["zed::IncreaseBufferFontSize", {"persist": False}]),
            ]
        ),
    ]

    keymap = json.loads(ZedDestination().render(bindings))

    assert keymap == [
        {
            "context": "Editor",
            "bindings": {"ctrl-y": "editor::DeleteLine", "ctrl-d": "editor::DuplicateSelection"},
        },
        {"context": "Workspace", "bindings": {"ctrl-r": None}},
        {"bindings": {"ctrl-+": ["zed::IncreaseBufferFontSize", {"persist": False}]}},
    ]


def test_fresh_destination_renders_keybindings_with_optional_args_and_when():
    binding = _binding(
        fresh=[
            FreshEntry(key="ctrl+shift+up", action="move_line_up", when="normal"),
            FreshEntry(key="alt+up", action="unbind", when="normal"),
            FreshEntry(key="ctrl+plus", action="insert_char", args={"char": "+"}),
        ]
    )

    rendered = json.loads(FreshDestination().render([binding]))

    assert rendered == {
        "keybindings": [
            {"key": "Up", "modifiers": ["ctrl", "shift"], "action": "move_line_up", "when": "normal"},
            {"key": "Up", "modifiers": ["alt"], "action": "unbind", "when": "normal"},
            {"key": "+", "modifiers": ["ctrl"], "action": "insert_char", "args": {"char": "+"}},
        ]
    }


def test_fresh_merge_replaces_only_keybindings_and_keeps_other_settings_in_order():
    destination = FreshDestination()
    rendered = destination.render([_binding(fresh=[FreshEntry(key="ctrl+y", action="delete_line")])])
    current = json.dumps(
        {
            "theme": "omarchy.json",
            "keybindings": [{"key": "q", "modifiers": ["ctrl"], "action": "noop"}],
            "editor": {"tab_size": 2},
        }
    )

    merged = json.loads(destination.merge(rendered, current))

    assert list(merged) == ["theme", "keybindings", "editor"]
    assert merged["theme"] == "omarchy.json"
    assert merged["editor"] == {"tab_size": 2}
    assert merged["keybindings"] == [{"key": "y", "modifiers": ["ctrl"], "action": "delete_line"}]


def test_fresh_merge_writes_the_render_when_there_is_no_config_yet():
    destination = FreshDestination()
    rendered = destination.render([])

    assert destination.merge(rendered, None) == rendered
    assert destination.merge(rendered, "  \n") == rendered


@pytest.mark.parametrize(
    "current",
    ['{\n  // dark theme\n  "theme": "dark"\n}', '{"theme": "dark",}', '["not", "an", "object"]'],
)
def test_fresh_merge_refuses_configs_it_cannot_rewrite_faithfully(current):
    destination = FreshDestination()

    with pytest.raises(MergeError):
        destination.merge(destination.render([]), current)


def test_all_destinations_render_the_full_real_config_without_error():
    bindings = load_bindings()

    vscode_json = VSCodeDestination().render(bindings)
    obsidian_json = ObsidianDestination().render(bindings)
    zed_json = ZedDestination().render(bindings)
    fresh_json = FreshDestination().render(bindings)

    assert "markdown.extension.editing.toggleCodeSpan" in vscode_json
    assert "workspace:toggle-pin" in obsidian_json
    assert "pane::TogglePinTab" in zed_json
    assert "open_live_grep" in fresh_json


def test_vscode_target_paths_when_installed(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setenv("HOME", str(tmp_path))
    (tmp_path / ".config" / "Code").mkdir(parents=True)

    assert VSCodeDestination().target_paths() == [
        tmp_path / ".config" / "Code" / "User" / "keybindings.json"
    ]


def test_vscode_target_paths_empty_when_not_installed(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setenv("HOME", str(tmp_path))

    assert VSCodeDestination().target_paths() == []


def test_zed_target_paths_when_installed(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setenv("HOME", str(tmp_path))
    (tmp_path / ".config" / "zed").mkdir(parents=True)

    assert ZedDestination().target_paths() == [tmp_path / ".config" / "zed" / "keymap.json"]


def test_zed_target_paths_empty_when_not_installed(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setenv("HOME", str(tmp_path))

    assert ZedDestination().target_paths() == []


def test_fresh_target_paths_when_installed(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setenv("HOME", str(tmp_path))
    (tmp_path / ".config" / "fresh").mkdir(parents=True)

    assert FreshDestination().target_paths() == [tmp_path / ".config" / "fresh" / "config.json"]


def test_fresh_target_paths_empty_when_not_installed(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setenv("HOME", str(tmp_path))

    assert FreshDestination().target_paths() == []


def test_obsidian_target_paths_from_registry(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setenv("HOME", str(tmp_path))
    vault_dir = tmp_path / "notes"
    vault_dir.mkdir()
    registry_dir = tmp_path / ".config" / "obsidian"
    registry_dir.mkdir(parents=True)
    registry = {"vaults": {"abc123": {"path": str(vault_dir), "ts": 1}}}
    (registry_dir / "obsidian.json").write_text(json.dumps(registry), encoding="utf-8")

    assert ObsidianDestination().target_paths() == [vault_dir / ".obsidian" / "hotkeys.json"]


def test_obsidian_target_paths_skips_stale_vault(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setenv("HOME", str(tmp_path))
    registry_dir = tmp_path / ".config" / "obsidian"
    registry_dir.mkdir(parents=True)
    registry = {"vaults": {"stale": {"path": str(tmp_path / "deleted-vault"), "ts": 1}}}
    (registry_dir / "obsidian.json").write_text(json.dumps(registry), encoding="utf-8")

    assert ObsidianDestination().target_paths() == []


def test_obsidian_target_paths_empty_when_no_registry(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setenv("HOME", str(tmp_path))

    assert ObsidianDestination().target_paths() == []


def test_obsidian_target_paths_empty_when_registry_is_malformed(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setenv("HOME", str(tmp_path))
    registry_dir = tmp_path / ".config" / "obsidian"
    registry_dir.mkdir(parents=True)
    (registry_dir / "obsidian.json").write_text("{not valid json", encoding="utf-8")

    assert ObsidianDestination().target_paths() == []


def test_obsidian_target_paths_from_registry_with_two_valid_vaults_and_a_stale_one(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setenv("HOME", str(tmp_path))
    vault_one = tmp_path / "vault-one"
    vault_one.mkdir()
    vault_two = tmp_path / "vault-two"
    vault_two.mkdir()
    registry_dir = tmp_path / ".config" / "obsidian"
    registry_dir.mkdir(parents=True)
    registry = {
        "vaults": {
            "vault-one-id": {"path": str(vault_one), "ts": 1},
            "vault-two-id": {"path": str(vault_two), "ts": 2},
            "stale-id": {"path": str(tmp_path / "deleted-vault"), "ts": 3},
        }
    }
    (registry_dir / "obsidian.json").write_text(json.dumps(registry), encoding="utf-8")

    target_paths = ObsidianDestination().target_paths()

    assert set(target_paths) == {
        vault_one / ".obsidian" / "hotkeys.json",
        vault_two / ".obsidian" / "hotkeys.json",
    }
    assert len(target_paths) == 2
