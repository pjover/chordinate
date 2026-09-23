.PHONY: install test run cheatsheet clean

install:
	uv sync

test:
	uv run pytest

run:
	uv run chordinate

cheatsheet:
	uv run python -m chordinate.cheatsheet cheatsheet.html

clean:
	rm -rf .venv dist build *.egg-info .pytest_cache cheatsheet.html
