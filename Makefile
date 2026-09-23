.PHONY: install test run apply clean

install:
	uv sync

test:
	uv run pytest

run:
	uv run chordinate

apply:
	uv run chordinate --apply

clean:
	rm -rf .venv dist build *.egg-info .pytest_cache
