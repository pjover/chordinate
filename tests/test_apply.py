from chordinate.apply import apply_to_path


def test_apply_to_path_writes_when_missing(tmp_path):
    target = tmp_path / "sub" / "Personal.xml"

    result = apply_to_path("new content\n", target)

    assert result.action == "written"
    assert result.backup_path is None
    assert target.read_text(encoding="utf-8") == "new content\n"


def test_apply_to_path_skips_when_content_identical(tmp_path):
    target = tmp_path / "Personal.xml"
    target.write_text("same content\n", encoding="utf-8")

    result = apply_to_path("same content\n", target)

    assert result.action == "skipped"
    assert result.backup_path is None
    assert target.read_text(encoding="utf-8") == "same content\n"


def test_apply_to_path_backs_up_when_content_differs(tmp_path):
    target = tmp_path / "Personal.xml"
    target.write_text("old content\n", encoding="utf-8")

    result = apply_to_path("new content\n", target)

    assert result.action == "backed_up"
    assert result.backup_path is not None
    assert result.backup_path.name.startswith("Personal.xml.bak-")
    assert result.backup_path.read_text(encoding="utf-8") == "old content\n"
    assert target.read_text(encoding="utf-8") == "new content\n"


def test_apply_to_path_creates_missing_parent_directories(tmp_path):
    target = tmp_path / "a" / "b" / "c" / "keybindings.json"

    apply_to_path("[]\n", target)

    assert target.is_file()
