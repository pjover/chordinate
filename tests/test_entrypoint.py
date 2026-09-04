import platform

from chordinate.entrypoint import main


def test_main_runs_and_prints_every_destination(capsys):
    main([])

    captured = capsys.readouterr()
    assert "# jetbrains" in captured.out
    assert "# vscode" in captured.out
    assert "# obsidian" in captured.out


def test_without_apply_flag_touches_no_files(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setenv("HOME", str(tmp_path))
    (tmp_path / ".config" / "Code").mkdir(parents=True)

    main([])

    captured = capsys.readouterr()
    assert "# vscode" in captured.out
    assert not (tmp_path / ".config" / "Code" / "User" / "keybindings.json").exists()


def test_apply_writes_to_discovered_vscode_target(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setenv("HOME", str(tmp_path))
    (tmp_path / ".config" / "Code").mkdir(parents=True)

    main(["--apply"])

    captured = capsys.readouterr()
    target = tmp_path / ".config" / "Code" / "User" / "keybindings.json"
    assert target.is_file()
    assert f"+ wrote: {target}" in captured.out


def test_apply_reports_missing_destination(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setenv("HOME", str(tmp_path))

    main(["--apply"])

    captured = capsys.readouterr()
    assert "! no jetbrains targets found" in captured.out


def test_apply_is_idempotent_on_second_run(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setenv("HOME", str(tmp_path))
    (tmp_path / ".config" / "Code").mkdir(parents=True)

    main(["--apply"])
    capsys.readouterr()
    main(["--apply"])

    captured = capsys.readouterr()
    target = tmp_path / ".config" / "Code" / "User" / "keybindings.json"
    assert f"= already up to date: {target}" in captured.out
