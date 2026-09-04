import difflib
import json
import platform

from chordinate.destinations.obsidian import ObsidianDestination
from chordinate.destinations.vscode import VSCodeDestination
from chordinate.entrypoint import main
from chordinate.model import load_bindings


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
    assert target.read_text(encoding="utf-8") == VSCodeDestination().render(load_bindings())


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


def test_apply_writes_identical_content_to_every_discovered_obsidian_vault(tmp_path, monkeypatch, capsys):
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
        }
    }
    (registry_dir / "obsidian.json").write_text(json.dumps(registry), encoding="utf-8")

    main(["--apply"])

    captured = capsys.readouterr()
    expected_content = ObsidianDestination().render(load_bindings())
    target_one = vault_one / ".obsidian" / "hotkeys.json"
    target_two = vault_two / ".obsidian" / "hotkeys.json"
    assert target_one.read_text(encoding="utf-8") == expected_content
    assert target_two.read_text(encoding="utf-8") == expected_content
    assert f"+ wrote: {target_one}" in captured.out
    assert f"+ wrote: {target_two}" in captured.out


def test_apply_reports_line_diff_counts_when_backing_up(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setenv("HOME", str(tmp_path))
    target_dir = tmp_path / ".config" / "Code" / "User"
    target_dir.mkdir(parents=True)
    target = target_dir / "keybindings.json"
    old_content = "[]\n"
    target.write_text(old_content, encoding="utf-8")

    new_content = VSCodeDestination().render(load_bindings())
    diff_lines = list(
        difflib.unified_diff(old_content.splitlines(), new_content.splitlines(), lineterm="")
    )
    expected_removed = sum(1 for line in diff_lines if line.startswith("-") and not line.startswith("---"))
    expected_added = sum(1 for line in diff_lines if line.startswith("+") and not line.startswith("+++"))

    main(["--apply"])

    captured = capsys.readouterr()
    assert (
        f"~ backed up {target} -> " in captured.out
        and f"(+{expected_added}/-{expected_removed} lines)" in captured.out
    )
    assert target.read_text(encoding="utf-8") == new_content
