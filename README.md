# chordinate

A single source of truth for keymaps across JetBrains, VS Code, and Obsidian — every action bound to one chord (a keystroke combo, like Ctrl+Shift+L), consistent on macOS and Linux, and reconciled against your OS shortcuts and file manager so nothing collides.

## Status

The keymap config and the renderers for all three destinations (JetBrains `Personal.xml`, VS Code `keybindings.json`, Obsidian `hotkeys.json`) are built and tested. Not yet built: applying them — discovering live config paths, backing them up, writing/symlinking into place (the `install.sh`-equivalent layer).

## Requirements

- [uv](https://docs.astral.sh/uv/)
- VS Code: [Markdown All in One](https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one) — required for the surround-with-backticks and surround-with-code-block bindings, which have no built-in VS Code equivalent.

## Keymap summary

Every row is one chord, kept consistent across whichever apps support it. Where an app can't share the headline chord, its own key is shown instead of a checkmark. Full detail and the reasoning behind each choice lives in `src/chordinate/data/keymap.json`.

### Editing

| Action                              | Chord                           |     JetBrains      |  VS Code   | Obsidian | Notes                                                 |
| ----------------------------------- | -------------------------------- | :----------------: | :--------: | :------: | ----------------------------------------------------- |
| Move / Swap Line Up / Down          | Ctrl+Shift+↑ / ↓                |         ✓          |     ✓      |    ✓     |                                                       |
| Move Statement Up / Down            | Ctrl+Alt+Shift+↑ / ↓            |         ✓          |     —      |    —     | No VS Code equivalent                                 |
| Clone Caret Above / Below           | Shift+Alt+↑ / ↓                 |         ✓          |     ✓      |    —     |                                                       |
| Delete Line                         | Ctrl+Y                          |         ✓          |     ✓      |    ✓     | Displaces VS Code's Redo (stays on Ctrl+Shift+Z)      |
| Join Lines                          | Ctrl+Shift+J                    |         ✓          |     ✓      |    —     |                                                       |
| Insert Line Above                   | Ctrl+Shift+Enter                |         ✓          |     ✓      |    —     |                                                       |
| Toggle Word Wrap                    | Alt+Z                           |         ✓          |     ✓      |    —     |                                                       |
| Comment Line                        | Ctrl+/ (+Ctrl+7 / Ctrl+Numpad÷) |         ✓          |     ✓      |    —     | Extra keys for Spanish keyboards                      |
| Organize / Optimize Imports         | Ctrl+Alt+O                      |         ✓          |     ✓      |    —     |                                                       |
| Rename                              | F2                              | ✓ (+Shift+F6 kept) | ✓ (native) |    —     | Matches Nautilus's F2                                 |
| Select All Occurrences Under Cursor | Ctrl+Shift+L                    |         ✓          | ✓ (native) |    —     |                                                       |
| Select Paragraph                    | Ctrl+Alt+U                      |         —          |     —      |    —     | Reserved only — no native action in either editor yet |

### Markdown

| Action                              | Chord        |       JetBrains        | VS Code |   Obsidian    | Notes                                                         |
| ----------------------------------- | ------------ | :--------------------: | :-----: | :-----------: | ------------------------------------------------------------- |
| Surround with `` `code` `` (inline) | Ctrl+Shift+K | ✓ (+Ctrl+Shift+C kept) |    ✓    | Ctrl+Shift+=  | Obsidian keeps its own pre-existing key                       |
| Surround with code block (fenced)   | Ctrl+Alt+K   |           —            |    ✓    | Ctrl+Shift+\\ | No JetBrains action exists; VS Code needs Markdown All in One |

### App / window

| Action                                          | Chord                  |      JetBrains       |   VS Code    |   Obsidian   | Notes                                                                              |
| ----------------------------------------------- | ---------------------- | :------------------: | :----------: | :----------: | ---------------------------------------------------------------------------------- |
| New / Activate Terminal                         | Ctrl+T                 |          ✓           |      ✓       |      —       | Overlaps Nautilus's Ctrl+T = New Tab, deliberately                                 |
| Switch Tool Window (Project/Find/Run/Debug/...) | Ctrl+Alt+1..0          |          ✓           |      —       |      —       | VS Code/Obsidian keep their own native editor-group/tab switching                  |
| Toggle Pin Editor Tab                           | Alt+P                  |          ✓           |      ✓       |      ✓       |                                                                                    |
| Zoom In / Out (UI scale)                        | Ctrl+Plus / Ctrl+Minus |          ✓           |  ✓ (native)  |      ✓       | JetBrains' code-folding family relocated to Ctrl+Alt+Shift+Plus/Minus to free this |
| Copy / Cut / Paste                              | Ctrl+C / X / V         | native (no override) | ✓ (Mac only) | ✓ (Mac only) | Adds working Ctrl+C/X/V on macOS alongside Cmd+C/X/V                               |

### Obsidian only

| Action                         | Chord                       | Notes                                        |
| ------------------------------ | --------------------------- | -------------------------------------------- |
| Reveal Active File in Explorer | Ctrl+Shift+Y                |                                              |
| Open / Show in Default App     | Ctrl+Shift+E / Ctrl+Shift+R |                                              |
| Search & Replace               | Ctrl+R                      |                                              |
| Edit Task (Tasks plugin)       | Ctrl+Shift+T                | No-op without the plugin installed           |
| Previous / Next Tab            | Ctrl+Shift+Tab / Ctrl+Tab   |                                              |
| Open Daily Note                | Ctrl+N                      |                                              |
| Export to PDF                  | Ctrl+Shift+P                | p3 vault only, not part of the canonical set |

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
