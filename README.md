# chordinate

A single source of truth for keymaps across JetBrains, VS Code, and Obsidian — every action bound to one chord (a keystroke combo, like Ctrl+Shift+L), consistent on macOS and Linux, and reconciled against your OS shortcuts and file manager so nothing collides.

## Status

Early scaffolding — the project structure exists, but the keymap config and the logic that applies it haven't been built yet.

## Requirements

- [uv](https://docs.astral.sh/uv/)
- VS Code: [Markdown All in One](https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one) — required for the surround-with-backticks and surround-with-code-block bindings, which have no built-in VS Code equivalent.

## Usage

```bash
uvx --from git+https://github.com/pjover/chordinate chordinate
```

## Development

```bash
make install   # uv sync
make test      # uv run pytest
make run       # uv run chordinate
```
