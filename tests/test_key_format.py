from chordinate.key_format import to_display, to_jetbrains, to_obsidian, to_vscode


def test_to_jetbrains_simple_letter():
    assert to_jetbrains("ctrl+y") == "control Y"


def test_to_jetbrains_function_key():
    assert to_jetbrains("f2") == "F2"


def test_to_jetbrains_three_modifiers_and_symbol():
    assert to_jetbrains("ctrl+alt+shift+plus") == "control alt shift EQUALS"


def test_to_jetbrains_slash_and_numpad_divide():
    assert to_jetbrains("ctrl+/") == "control SLASH"
    assert to_jetbrains("ctrl+numpad_divide") == "control DIVIDE"


def test_to_jetbrains_page_keys():
    assert to_jetbrains("ctrl+pageup") == "control PAGE_UP"
    assert to_jetbrains("ctrl+pagedown") == "control PAGE_DOWN"


def test_to_vscode_passes_through_letters():
    assert to_vscode("ctrl+shift+l") == "ctrl+shift+l"


def test_to_vscode_translates_plus_and_minus():
    assert to_vscode("ctrl+plus") == "ctrl+="
    assert to_vscode("ctrl+alt+shift+minus") == "ctrl+alt+shift+-"


def test_to_obsidian_maps_ctrl_to_mod_by_default():
    modifiers, key = to_obsidian("ctrl+shift+up")
    assert modifiers == ["Mod", "Shift"]
    assert key == "ArrowUp"


def test_to_obsidian_page_keys_keep_camel_case():
    assert to_obsidian("ctrl+pageup") == (["Mod"], "PageUp")
    assert to_obsidian("ctrl+pagedown") == (["Mod"], "PageDown")


def test_to_obsidian_literal_ctrl_stays_ctrl():
    modifiers, key = to_obsidian("ctrl+c", literal_ctrl=True)
    assert modifiers == ["Ctrl"]
    assert key == "C"


def test_to_display_uses_printable_names():
    assert to_display("ctrl+shift+up") == ["Ctrl", "Shift", "↑"]
    assert to_display("ctrl+numpad_divide") == ["Ctrl", "Numpad÷"]
    assert to_display("f2") == ["F2"]
    assert to_display("ctrl+pageup") == ["Ctrl", "PgUp"]
