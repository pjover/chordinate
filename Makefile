.PHONY: install test run apply cheatsheet cheatsheet-pdf clean

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

cheatsheet-pdf: cheatsheet
	@# Headless Chromium/Chrome prints with the sheet's own print CSS (A4 landscape). Override with CHROME=/path/to/browser.
	@chrome="$(CHROME)"; \
	for c in chromium chromium-browser google-chrome-stable google-chrome \
		"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
		"/Applications/Chromium.app/Contents/MacOS/Chromium"; do \
		[ -n "$$chrome" ] && break; \
		if [ -x "$$c" ]; then chrome="$$c"; else chrome=$$(command -v "$$c" 2>/dev/null); fi; \
	done; \
	[ -n "$$chrome" ] || { echo "Chromium or Google Chrome not found; set CHROME=/path/to/browser"; exit 1; }; \
	[ -x "$$chrome" ] || command -v "$$chrome" >/dev/null 2>&1 || { echo "CHROME=$$chrome is not an executable"; exit 1; }; \
	"$$chrome" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf=cheatsheet.pdf "file://$(CURDIR)/cheatsheet.html" 2>/dev/null
	@echo "Wrote cheatsheet.pdf"

clean:
	rm -rf .venv dist build *.egg-info .pytest_cache cheatsheet.html cheatsheet.pdf
