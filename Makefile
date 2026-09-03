.PHONY: install test run clean

install:
	uv sync

test:
	uv run pytest

run:
	uv run chordinate

clean:
	rm -rf .venv dist build *.egg-info .pytest_cache
