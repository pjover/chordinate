from chordinate.entrypoint import main


def test_main_runs_and_prints(capsys):
    main()

    captured = capsys.readouterr()
    assert captured.out.strip() == "chordinate: not implemented yet"
