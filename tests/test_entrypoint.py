from chordinate.entrypoint import main


def test_main_runs_and_prints_every_destination(capsys):
    main()

    captured = capsys.readouterr()
    assert "# jetbrains" in captured.out
    assert "# vscode" in captured.out
    assert "# obsidian" in captured.out
