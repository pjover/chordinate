from chordinate.model import load_bindings


def test_load_bindings_returns_every_binding():
    bindings = load_bindings()
    assert len(bindings) == 28


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
