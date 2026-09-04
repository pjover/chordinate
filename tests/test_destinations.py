import platform

from chordinate.destinations.jetbrains import JetBrainsDestination
from chordinate.destinations.obsidian import ObsidianDestination
from chordinate.destinations.vscode import VSCodeDestination
from chordinate.model import Binding, JetBrainsEntry, ObsidianEntry, VSCodeEntry, load_bindings


def _binding(**kwargs) -> Binding:
    return Binding(id="test", action="Test", **kwargs)


def test_jetbrains_destination_renders_action_with_keyboard_shortcut():
    binding = _binding(jetbrains=[JetBrainsEntry(action_id="EditorDeleteLine", keys=["ctrl+y"])])

    xml = JetBrainsDestination().render([binding])

    assert '<keymap version="1" name="Personal" parent="$default">' in xml
    assert '<action id="EditorDeleteLine">' in xml
    assert '<keyboard-shortcut first-keystroke="control Y" />' in xml


def test_jetbrains_destination_merges_multiple_keys_on_same_action():
    binding = _binding(jetbrains=[JetBrainsEntry(action_id="RenameElement", keys=["f2", "shift+f6"])])

    xml = JetBrainsDestination().render([binding])

    assert '<keyboard-shortcut first-keystroke="F2" />' in xml
    assert '<keyboard-shortcut first-keystroke="shift F6" />' in xml


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
            ObsidianEntry(command_id="editor:copy", key="ctrl+c", literal_ctrl=True),
        ]
    )

    hotkeys = ObsidianDestination().render([binding])

    assert '"editor:copy"' in hotkeys
    assert '"Ctrl"' in hotkeys
    assert '"C"' in hotkeys


def test_all_destinations_render_the_full_real_config_without_error():
    bindings = load_bindings()

    jetbrains_xml = JetBrainsDestination().render(bindings)
    vscode_json = VSCodeDestination().render(bindings)
    obsidian_json = ObsidianDestination().render(bindings)

    assert "PinActiveTab" in jetbrains_xml
    assert "markdown.extension.editing.toggleCodeSpan" in vscode_json
    assert "workspace:toggle-pin" in obsidian_json


def test_jetbrains_target_paths_finds_matching_products(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setenv("HOME", str(tmp_path))
    jetbrains_dir = tmp_path / ".config" / "JetBrains"
    (jetbrains_dir / "IdeaIC2026.1").mkdir(parents=True)
    (jetbrains_dir / "PyCharm2025.2").mkdir(parents=True)
    (jetbrains_dir / "SomeOtherApp").mkdir(parents=True)

    target_paths = JetBrainsDestination().target_paths()

    assert target_paths == [
        jetbrains_dir / "IdeaIC2026.1" / "keymaps" / "Personal.xml",
        jetbrains_dir / "PyCharm2025.2" / "keymaps" / "Personal.xml",
    ]


def test_jetbrains_target_paths_empty_when_no_config_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setenv("HOME", str(tmp_path))

    assert JetBrainsDestination().target_paths() == []
