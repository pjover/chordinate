from chordinate.cheatsheet import chord_keys, group_rows, main, render
from chordinate.model import (
    Binding,
    CheatSheetEntry,
    JetBrainsEntry,
    ObsidianEntry,
    VSCodeEntry,
    load_bindings,
)


def _binding(**kwargs) -> Binding:
    return Binding(id="test", action="Test", **kwargs)


def test_chord_keys_merges_apps_without_duplicates_or_removals():
    binding = _binding(
        jetbrains=[JetBrainsEntry(action_id="EditorDeleteLine", keys=["ctrl+y"])],
        vscode=[
            VSCodeEntry(command="editor.action.deleteLines", key="ctrl+y"),
            VSCodeEntry(command="-redo", key="ctrl+shift+y"),
        ],
        obsidian=[ObsidianEntry(command_id="editor:delete-paragraph", key="ctrl+y")],
    )

    assert chord_keys(binding) == ["ctrl+y"]


def test_chord_keys_prefers_explicit_cheatsheet_keys():
    binding = _binding(
        jetbrains=[JetBrainsEntry(action_id="ExpandAll", keys=["ctrl+alt+shift+plus"])],
        cheatsheet=CheatSheetEntry(keys=["ctrl+plus"]),
    )

    assert chord_keys(binding) == ["ctrl+plus"]


def test_reserved_key_is_shown_and_marked_reserved():
    rows = group_rows([_binding(reserved_key="ctrl+alt+u", cheatsheet=CheatSheetEntry(group="Editing"))])

    assert rows["Editing"][0].keys == ["ctrl+alt+u"]
    assert rows["Editing"][0].note == "reserved"


def test_group_rows_skips_hidden_and_defaults_to_other():
    rows = group_rows([_binding(), _binding(cheatsheet=CheatSheetEntry(hidden=True))])

    assert list(rows) == ["Other"]
    assert len(rows["Other"]) == 1


def test_render_repeats_modifiers_only_when_they_change():
    binding = _binding(
        vscode=[
            VSCodeEntry(command="copy", key="ctrl+c"),
            VSCodeEntry(command="cut", key="ctrl+x"),
        ]
    )

    html = render([binding])

    assert '<kbd>Ctrl</kbd><span class="plus">+</span><kbd>C</kbd></span><span class="slash">/</span><span class="combo"><kbd>X</kbd>' in html


def test_render_bundled_keymap_lists_groups_in_order():
    html = render(load_bindings())

    positions = [html.index(f"<h2>{name}") for name in ["Editing", "Markdown", "App / window", "Obsidian only"]]
    assert positions == sorted(positions)
    assert "Swap Line Up / Down (Obsidian)" not in html
    assert "{{" not in html


def test_main_writes_file(tmp_path):
    output = tmp_path / "sheet.html"

    main([str(output)])

    assert output.read_text(encoding="utf-8").startswith("<!doctype html>")
