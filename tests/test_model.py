from chordinate.model import load_bindings


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
