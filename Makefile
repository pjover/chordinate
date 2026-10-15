.PHONY: install test run apply cheatsheet clean

install:
	uv sync

test:
	uv run pytest

run:
	uv run chordinate

apply:
	uv run chordinate --apply

cheatsheet:
	uv run python -m chordinate.cheatsheet cheatsheet.html

clean:
	rm -rf .venv dist build *.egg-info .pytest_cache cheatsheet.html
