# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`chordinate` renders one keymap definition (`src/chordinate/data/keymap.json`) into native keymap files for VS Code (`keybindings.json`), Obsidian (`hotkeys.json`), Zed (`keymap.json`) and Fresh (the `keybindings` list in its `config.json`), and optionally writes them into the live config dirs. macOS and Linux only (Windows raises `UnsupportedOSError`). Python ≥3.12, managed with `uv`, no runtime dependencies.

## Commands

```bash
make install        # uv sync
make test           # uv run pytest
uv run pytest tests/test_key_format.py::test_name   # single test
make run            # print both renders (writes nothing)
make apply          # chordinate --apply — writes into the REAL editor config on this machine
make cheatsheet     # cheatsheet.html (printable A4 landscape)
```

Avoid running `make apply` / `chordinate --apply` unless asked: it replaces the user's live keymap files (with timestamped `.bak-` backups).

## Architecture

Pipeline: `model.load_bindings()` → each `Destination.render(bindings)` → stdout, or `apply.apply_to_path()` for each `Destination.target_paths()`.

- **`model.py`** — frozen dataclasses (`Binding` with per-app entry lists + `CheatSheetEntry`). Config lookup order: `$CHORDINATE_HOME/keymap.json`, `./keymap.json`, `~/.config/chordinate/keymap.json`, then the bundled `chordinate.data/keymap.json` (loaded via `importlib.resources`). Note `./keymap.json` means a `keymap.json` in the repo root would shadow the bundled one.
- **`key_format.py`** — keys in `keymap.json` are always written in one canonical notation (`ctrl+shift+plus`, lowercase, `+`-joined). This module is the only place translating to each app's syntax (`to_vscode`, `to_obsidian`, `to_zed`, `to_fresh`) and to display glyphs (`to_display`). New key names must be added to the per-app maps here.
- **`destinations/`** — one class per app implementing the `Destination` protocol in `base.py` (`name`, `render`, `merge`, `target_paths`). `merge(rendered, current)` returns what to write over a target's current text: VS Code, Obsidian and Zed own the whole file and return the render; Fresh replaces only `keybindings` in its shared `config.json`, keeping other keys in order, and raises `MergeError` (entrypoint prints `! skipped`, writes nothing) for JSONC it can't rewrite faithfully. Target discovery: VS Code = `Code/User/keybindings.json` if `Code/` exists; Obsidian = every vault in the `obsidian/obsidian.json` registry; Zed = `~/.config/zed/keymap.json` if `~/.config/zed/` exists; Fresh = `~/.config/fresh/config.json` if `~/.config/fresh/` exists (Zed and Fresh use `~/.config` on macOS too, not Application Support). Base dirs come from `paths.py`. Missing apps return `[]` and are skipped — never create directories for absent apps.
- **`apply.py`** — idempotent write of the merged content: identical → skip; existing → rename to `<name>.bak-YYYYMMDD-HHMMSS` and report +/- line counts; else write.
- **`cheatsheet.py`** — groups bindings by `cheatsheet.group` (`GROUP_ORDER` first, unknown groups appended) and fills the template `data/cheatsheet.html`. Chord keys come from `cheatsheet.keys` if set, else collected from all app entries (skipping VS Code `-command` removals, Zed `null` unbinds and Fresh `unbind`s), else `reserved_key`.

## keymap.json semantics worth knowing

- **VS Code removals**: an entry whose `command` starts with `-` unbinds a default on that key.
- **Obsidian removals**: an entry with a `command_id` and no `key` renders `[]`, unbinding that command's default hotkey.
- **Obsidian `ctrl` renders as literal `Ctrl`**, never `Mod` (which is Cmd on macOS), so the same chord means the physical Ctrl key in every app.
- **Zed entries** are `{"action", "key", "context"?}`; `action` is a string, `[name, {args}]`, or `null` (unbinds that key in that context). The render groups entries into one section per context. Zed layers the file over its defaults, and the deepest matching context wins, so chords Zed's editor already uses need `Editor` context. `plus` renders as `+` (Zed matches the typed character), not VS Code's `=`.
- **Fresh entries** are `{"action", "key", "when"?, "args"?}`; `when` is the context (`normal` = text editor). `"action": "unbind"` removes the keymap's own binding on that key; custom bindings always outrank keymap defaults. Fresh treats unknown action names as plugin actions, so a typo binds nothing silently — check names against Fresh's keybinding editor. Named keys render as Fresh spells them (`Up`, `PageUp`), `plus`/`minus` as `+`/`-`. Fresh runs in a terminal, which may swallow a chord first (Alacritty: `ctrl+shift+f`).
- `reserved_key` marks a chord held for future use with no app entries.
- `"cheatsheet": false` hides a binding from the sheet.
- Chord choices are deliberately chosen to avoid collisions with Omarchy (Linux) and macOS system shortcuts and Nautilus; the `note` fields in `keymap.json` record why. The README "Keymap summary" tables mirror `keymap.json` — update them when changing bindings.

## Tests

Tests use `tmp_path` + `monkeypatch` of `platform.system` and `HOME` to simulate macOS/Linux config dirs; follow that pattern for anything touching `paths.py` or `target_paths()`.
