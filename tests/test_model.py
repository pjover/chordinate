import json
from pathlib import Path

from chordinate.model import load_bindings


def _write_config(directory: Path, marker_id: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    config = {"bindings": [{"id": marker_id, "action": "Test"}]}
    (directory / "keymap.json").write_text(json.dumps(config), encoding="utf-8")


def test_load_bindings_returns_every_binding():
    bindings = load_bindings()
    assert len(bindings) == 29


def test_delete_line_binding_has_all_three_app_targets():
    bindings = {b.id: b for b in load_bindings()}
    delete_line = bindings["delete-line"]

    assert delete_line.jetbrains[0].action_id == "EditorDeleteLine"
    assert delete_line.vscode[0].command == "editor.action.deleteLines"
    assert delete_line.obsidian[0].command_id == "editor:delete-paragraph"


def test_reserved_but_unbound_binding_has_no_app_targets():
    bindings = {b.id: b for b in load_bindings()}
    select_paragraph = bindings["select-paragraph"]

    assert select_paragraph.reserved_key == "ctrl+alt+u"
    assert select_paragraph.jetbrains == []
    assert select_paragraph.vscode == []
    assert select_paragraph.obsidian == []


def test_switch_tool_window_binding_covers_all_ten_slots():
    bindings = {b.id: b for b in load_bindings()}
    switch_tool_window = bindings["switch-tool-window"]

    assert len(switch_tool_window.jetbrains) == 10
    by_action = {e.action_id: e.keys for e in switch_tool_window.jetbrains}
    assert by_action["ActivateProjectToolWindow"] == ["ctrl+alt+1"]
    assert by_action["ActivateCommitToolWindow"] == ["ctrl+alt+0"]


def test_falls_back_to_bundled_config_when_no_override_exists(tmp_path, monkeypatch):
    monkeypatch.delenv("CHORDINATE_HOME", raising=False)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("HOME", str(tmp_path / "empty-home"))

    bindings = load_bindings()

    assert len(bindings) == 29


def test_chordinate_home_env_var_takes_priority_over_cwd_and_user_config(tmp_path, monkeypatch):
    chordinate_home = tmp_path / "chordinate-home"
    cwd_dir = tmp_path / "cwd"
    user_config_dir = tmp_path / "userhome" / ".config" / "chordinate"
    _write_config(chordinate_home, "from-chordinate-home")
    _write_config(cwd_dir, "from-cwd")
    _write_config(user_config_dir, "from-user-config")

    monkeypatch.setenv("CHORDINATE_HOME", str(chordinate_home))
    monkeypatch.chdir(cwd_dir)
    monkeypatch.setenv("HOME", str(tmp_path / "userhome"))

    bindings = load_bindings()

    assert [b.id for b in bindings] == ["from-chordinate-home"]


def test_cwd_config_used_when_no_chordinate_home_env_var(tmp_path, monkeypatch):
    cwd_dir = tmp_path / "cwd"
    user_config_dir = tmp_path / "userhome" / ".config" / "chordinate"
    _write_config(cwd_dir, "from-cwd")
    _write_config(user_config_dir, "from-user-config")

    monkeypatch.delenv("CHORDINATE_HOME", raising=False)
    monkeypatch.chdir(cwd_dir)
    monkeypatch.setenv("HOME", str(tmp_path / "userhome"))

    bindings = load_bindings()

    assert [b.id for b in bindings] == ["from-cwd"]


def test_user_config_dir_used_as_last_resort_before_bundled_default(tmp_path, monkeypatch):
    empty_cwd = tmp_path / "cwd"
    empty_cwd.mkdir()
    user_config_dir = tmp_path / "userhome" / ".config" / "chordinate"
    _write_config(user_config_dir, "from-user-config")

    monkeypatch.delenv("CHORDINATE_HOME", raising=False)
    monkeypatch.chdir(empty_cwd)
    monkeypatch.setenv("HOME", str(tmp_path / "userhome"))

    bindings = load_bindings()

    assert [b.id for b in bindings] == ["from-user-config"]
