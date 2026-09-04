from chordinate.apply import apply_to_path


def test_apply_to_path_writes_when_missing(tmp_path):
    target = tmp_path / "sub" / "Personal.xml"

    result = apply_to_path("new content\n", target)

    assert result.action == "written"
    assert result.backup_path is None
    assert result.lines_added == 0
    assert result.lines_removed == 0
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
    # "old content" -> "new content" is a single line replaced: one line
    # removed, one line added.
    assert result.lines_added == 1
    assert result.lines_removed == 1


def test_apply_to_path_reports_multi_line_diff_counts(tmp_path):
    target = tmp_path / "keybindings.json"
    target.write_text("line one\nline two\nline three\n", encoding="utf-8")

    result = apply_to_path("line one\nline two changed\nline three\nline four\n", target)

    assert result.action == "backed_up"
    # "line two" -> "line two changed" is one removal + one addition, and
    # "line four" is a new trailing line: 1 removed, 2 added.
    assert result.lines_removed == 1
    assert result.lines_added == 2


def test_apply_to_path_creates_missing_parent_directories(tmp_path):
    target = tmp_path / "a" / "b" / "c" / "keybindings.json"

    apply_to_path("[]\n", target)

    assert target.is_file()
