# chordinate

A single source of truth for keymaps across JetBrains, VS Code, and Obsidian — every action bound to one chord (a keystroke combo, like Ctrl+Shift+L), consistent on macOS and Linux, and reconciled against your OS shortcuts and file manager so nothing collides.

This is an *omakase* keymap — [chef's choice](https://learn.omacom.io/3/omacom/76/omakase-computing), the same philosophy behind [Omarchy](https://omarchy.org/): a considered default proposed for you, not a mandate.

As I'm using Mac (for work) and Omarchy (for fun) I wanted to keep compatibility with Omarchy's own default keybindings, so nothing collides out of the box. Use the proposal as-is, or tweak any chord to your own taste — see [Tweaking the keymap](#tweaking-the-keymap) below.

## Status

The keymap config and the renderers for all three destinations (JetBrains `Personal.xml`, VS Code `keybindings.json`, Obsidian `hotkeys.json`) are built and tested. Not yet built: applying them — discovering live config paths, backing them up, writing/symlinking into place (the `install.sh`-equivalent layer).

## Requirements

- [uv](https://docs.astral.sh/uv/)
- VS Code: [Markdown All in One](https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one) — required for the surround-with-backticks and surround-with-code-block bindings, which have no built-in VS Code equivalent.
- VS Code: [Markdown PDF](https://marketplace.visualstudio.com/items?itemName=yzane.markdown-pdf) — required for the export-to-PDF binding.

## Keymap summary

This is the proposed keymap — the omakase default, not a fixed rule. Every row is one chord, kept consistent across whichever apps support it. Where an app can't share the headline chord, its own key is shown instead of a checkmark. Full detail and the reasoning behind each choice lives in `src/chordinate/data/keymap.json`. Want something different? See [Tweaking the keymap](#tweaking-the-keymap).

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
| Export to PDF                       | Shift+Alt+P  |           —            |    ✓    |       ✓       | VS Code needs Markdown PDF                                    |

### App / window

| Action                                          | Chord                  |      JetBrains       |   VS Code    |   Obsidian   | Notes                                                                              |
| ----------------------------------------------- | ---------------------- | :------------------: | :----------: | :----------: | ---------------------------------------------------------------------------------- |
| New / Activate Terminal                         | Ctrl+T                 |          ✓           |      ✓       |      —       | Overlaps Nautilus's Ctrl+T = New Tab, deliberately                                 |
| Switch Tool Window (Project/Find/Run/Debug/...) | Ctrl+Alt+1..0          |          ✓           |      —       |      —       | VS Code/Obsidian keep their own native editor-group/tab switching                  |
| Toggle Pin Editor Tab                           | Ctrl+Alt+P             |          ✓           |      ✓       |      ✓       | Displaces JetBrains' Introduce Parameter (still in Refactor This)                  |
| Zoom In / Out (UI scale)                        | Ctrl+Plus / Ctrl+Minus |          ✓           |  ✓ (native)  |      ✓       | JetBrains' code-folding family relocated to Ctrl+Alt+Shift+Plus/Minus to free this |
| Copy / Cut / Paste                              | Ctrl+C / X / V         | native (no override) | ✓ (Mac only) | ✓ (Mac only) | Adds working Ctrl+C/X/V on macOS alongside Cmd+C/X/V                               |

### Obsidian only

| Action                         | Chord                       | Notes                                        |
| ------------------------------ | --------------------------- | -------------------------------------------- |
| Reveal Active File in Explorer | Ctrl+Shift+Y                |                                              |
| Open / Show in Default App     | Ctrl+Shift+O / Ctrl+Shift+S |                                              |
| Search & Replace               | Ctrl+R                      |                                              |
| Edit Task (Tasks plugin)       | Ctrl+Shift+T                | No-op without the plugin installed           |
| Previous / Next Tab            | Ctrl+Shift+Tab / Ctrl+Tab   |                                              |
| Open Daily Note                | Ctrl+N                      |                                              |

## Tweaking the keymap

Every binding lives in one `keymap.json` file. Since this is just a proposal, don't edit the copy bundled with the package — instead put your own `keymap.json` in one of these locations, checked in order:

1. `$CHORDINATE_HOME/keymap.json`, if the `CHORDINATE_HOME` environment variable is set
2. `./keymap.json`, in the current directory
3. `~/.config/chordinate/keymap.json`

The first one found wins. If none exist, the bundled default (`src/chordinate/data/keymap.json`) is used — so the easiest way to start customizing is to copy that file to `~/.config/chordinate/keymap.json` and edit your copy from there. Each entry looks like:

```json
{
  "id": "delete-line",
  "action": "Delete Line",
  "jetbrains": { "entries": [{"action_id": "EditorDeleteLine", "keys": ["ctrl+y"]}] },
  "vscode":    { "entries": [{"command": "editor.action.deleteLines", "key": "ctrl+y"}] },
  "obsidian":  { "entries": [{"command_id": "editor:delete-paragraph", "key": "ctrl+y"}] },
  "note": "..."
}
```

- **Change a chord**: edit the `key` (or `keys`, for JetBrains) value(s) on whichever app block(s) you want to affect. Keys use one canonical notation (`ctrl+shift+l`, lowercase, `+`-joined) — `src/chordinate/key_format.py` translates it into each app's real syntax, so you never write JetBrains/VS Code/Obsidian syntax by hand.
- **Add a new binding**: append a new object to the `bindings` array with an `id`, a human-readable `action`, and whichever of `jetbrains`/`vscode`/`obsidian` blocks apply — omit any app that shouldn't get the binding.
- **JetBrains specifically**: `keys` is a list, not a single value, because declaring an `<action>` in the keymap replaces its entire inherited shortcut set. If you're adding a key without wanting to lose a default JetBrains already has for that action, list both keys together (see `rename` in the file for an example).
- **Cheat sheet**: the optional `cheatsheet` block controls how a binding appears on the printable cheat sheet — `group` (`Editing`, `Markdown`, `App / window`, `Obsidian only`, or any new name), a shorter `label`, an optional `note`, and `keys` to override the chord shown (otherwise it's collected from the app entries). Set `"cheatsheet": false` to leave a binding off the sheet.
- **Preview the result**: `make run` prints the rendered `Personal.xml`, `keybindings.json`, and `hotkeys.json` content for every binding. `make test` checks the config still loads and renders correctly.

Applying the rendered output to your actual editor config is still a manual copy for now — see [Status](#status).

## Usage

```bash
uvx --from git+https://github.com/pjover/chordinate chordinate
```

By default this renders the bundled omakase proposal. To use your own `keymap.json` instead, see [Tweaking the keymap](#tweaking-the-keymap) — put it at `~/.config/chordinate/keymap.json`, in the current directory, or wherever `$CHORDINATE_HOME` points.

## Development

```bash
make install   # uv sync
make test      # uv run pytest
make run       # uv run chordinate
make cheatsheet  # write cheatsheet.html, a printable (A4 landscape) sheet of every chord
```
