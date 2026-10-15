# chordinate

A single source of truth for keymaps across VS Code, Obsidian and Zed — every action bound to one chord (a keystroke combo, like Ctrl+Shift+L), consistent on macOS and Linux, and reconciled against your OS shortcuts and file manager so nothing collides.

As I'm using Mac (for work) and Omarchy (for fun) I wanted to keep compatibility with Omarchy's own default keybindings, so nothing collides out of the box. Use the proposal as-is, or tweak any chord to your own taste — see [Tweaking the keymap](#tweaking-the-keymap) below.

## Status

Complete for all three destinations on macOS and Linux. The keymap config and the renderers (VS Code `keybindings.json`, Obsidian `hotkeys.json`, Zed `keymap.json`) are built and tested, and so is applying them: `chordinate --apply` finds your live config paths, backs up what's already there, and writes the rendered files into place — the `install.sh`-equivalent layer. See [Usage](#usage).

Windows isn't supported.

## Requirements

- [uv](https://docs.astral.sh/uv/)
- VS Code: [Markdown All in One](https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one) — required for the surround-with-backticks and surround-with-code-block bindings, which have no built-in VS Code equivalent.

## Keymap summary

This is the proposed keymap — a considered default, not a fixed rule. Every row is one chord, kept consistent across whichever apps support it. Where an app can't share the headline chord, its own key is shown instead of a checkmark. Full detail and the reasoning behind each choice lives in `src/chordinate/data/keymap.json`. Want something different? See [Tweaking the keymap](#tweaking-the-keymap).

### Editing

| Action                      | Chord                           |  VS Code   | Obsidian |  Zed  | Notes                                                 |
| --------------------------- | ------------------------------- | :--------: | :------: | :---: | ----------------------------------------------------- |
| Move / Swap Line Up / Down  | Ctrl+Shift+↑ / ↓                |     ✓      |    ✓     |   ✓   |                                                       |
| Clone Caret Above / Below   | Shift+Alt+↑ / ↓                 |     ✓      |    —     |   ✓   |                                                       |
| Delete Line                 | Ctrl+Y                          |     ✓      |    ✓     |   ✓   | Displaces VS Code's and Zed's Redo (stays on Ctrl+Shift+Z) |
| Duplicate Line or Selection | Ctrl+D                          |     ✓      |    —     |   ✓   | Displaces VS Code's Add Selection to Next Find Match (on Ctrl+Shift+L) and Zed's Select Next; no Obsidian command |
| Join Lines                  | Ctrl+Shift+J                    |     ✓      |    —     |   ✓   |                                                       |
| Insert Line Above           | Ctrl+Shift+Enter                |     ✓      |    —     |   ✓   |                                                       |
| Toggle Word Wrap            | Ctrl+Alt+Shift+Z                |     ✓      |    —     |   ✓   |                                                       |
| Comment Line                | Ctrl+/ · Ctrl+Alt+Shift+Q (+Ctrl+7 / Ctrl+Numpad÷) |     ✓      |    ✓     |   ✓   | Extra keys for Spanish keyboards (Ctrl+7 in VS Code and Zed, Numpad÷ in VS Code); on macOS replaces Obsidian's Cmd+/ |
| Search in File              | Ctrl+F                          |     ✓      |    ✓     |   ✓   | Native on Linux; on macOS replaces Obsidian's Cmd+F (VS Code and Zed keep it) |
| Replace in File             | Ctrl+R                          |     ✓      |    ✓     |   ✓   | Displaces VS Code's and Zed's Open Recent             |
| Search in All Files         | Ctrl+Shift+F                    |     ✓      |    ✓     |   ✓   | Native on Linux; on macOS replaces Obsidian's Cmd+Shift+F (VS Code and Zed keep it) |
| Replace in All Files        | Ctrl+Shift+R                    |     ✓      |    —     |   ✓   | Displaces VS Code's Refactor… and Zed's Rerun Task (Linux); no Obsidian command |

### Markdown

| Action                              | Chord            | VS Code | Obsidian | Zed | Notes                             |
| ----------------------------------- | ---------------- | :-----: | :------: | :-: | --------------------------------- |
| Surround with `` `code` `` (inline) | Ctrl+Alt+Shift+G |    ✓    |    ✓     |  —  | VS Code needs Markdown All in One; no Zed action |
| Surround with code block (fenced)   | Ctrl+Alt+Shift+B |    ✓    |    ✓     |  —  | VS Code needs Markdown All in One; no Zed action |

### App / window

| Action                         | Chord                  |   VS Code    |   Obsidian   |       Zed        | Notes                                                |
| ------------------------------ | ---------------------- | :----------: | :----------: | :--------------: | ---------------------------------------------------- |
| Toggle Pin Editor Tab          | Ctrl+Alt+Shift+T       |      ✓       |      ✓       |        ✓         |                                                      |
| Reveal Active File in Explorer | Ctrl+Alt+Shift+E       |      ✓       |      ✓       |        ✓         | Displaces Zed's Toggle Edit Prediction (Linux)       |
| Show in File Explorer / Finder | Ctrl+Alt+Shift+W       |      ✓       |      ✓       |        ✓         |                                                      |
| Zoom In / Out (UI scale)       | Ctrl+Plus / Ctrl+Minus |  ✓ (native)  |      ✓       |  ✓ (text size)   | Zed has no whole-app zoom; uses its View → Zoom (buffer font) |
| Copy / Cut / Paste             | Ctrl+C / X / V         | ✓ (Mac only) | ✓ (Mac only) |   ✓ (Mac only)   | Adds working Ctrl+C/X/V on macOS alongside Cmd+C/X/V; Zed's terminal keeps Ctrl+C |

### Obsidian only

| Action              | Chord                     | Notes            |
| ------------------- | ------------------------- | ---------------- |
| Open in Default App | Ctrl+Alt+Shift+A          |                  |
| Previous / Next Tab | Ctrl+Shift+Tab / Ctrl+Tab |                  |
| Open Daily Note     | Ctrl+N                    | Unbinds New Note |

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
  "vscode":    { "entries": [{"command": "editor.action.deleteLines", "key": "ctrl+y"}] },
  "obsidian":  { "entries": [{"command_id": "editor:delete-paragraph", "key": "ctrl+y"}] },
  "zed":       { "entries": [{"action": "editor::DeleteLine", "key": "ctrl+y", "context": "Editor"}] },
  "note": "..."
}
```

- **Change a chord**: edit the `key` value(s) on whichever app block(s) you want to affect. Keys use one canonical notation (`ctrl+shift+l`, lowercase, `+`-joined) — `src/chordinate/key_format.py` translates it into each app's real syntax, so you never write VS Code/Obsidian/Zed syntax by hand.
- **Add a new binding**: append a new object to the `bindings` array with an `id`, a human-readable `action`, and whichever of `vscode`/`obsidian`/`zed` blocks apply — omit any app that shouldn't get the binding.
- **Zed entries**: `action` is a Zed action name (`"editor::DeleteLine"`) or, for actions that take arguments, `[name, {args}]` (see `replace-in-all-files`). `context` is optional and picks which part of Zed the binding applies to (`Editor`, `Pane`, `Workspace`, …); the deepest matching context wins, so a chord Zed already uses in its editor needs an `Editor` context to override it.
- **Removing an app's own default**: VS Code — add an entry on the same key whose `command` is the displaced one prefixed with `-` (see `delete-line`, which frees Ctrl+Y from Redo). Obsidian — add an entry with just a `command_id` and no `key`, which renders an empty hotkey list (see `daily-notes-obsidian`, which frees Ctrl+N from New Note). Zed — add an entry with `"action": null` on that key and context (see `replace-in-file`, which frees Ctrl+R from Open Recent).
- **Cheat sheet**: the optional `cheatsheet` block controls how a binding appears on the printable cheat sheet — `group` (`Editing`, `Markdown`, `App / window`, `Obsidian only`, or any new name), a shorter `label`, an optional `note`, and `keys` to override the chord shown (otherwise it's collected from the app entries). Set `"cheatsheet": false` to leave a binding off the sheet.
- **Preview the result**: `make run` prints the rendered `keybindings.json`, `hotkeys.json` and Zed `keymap.json` content for every binding. `make test` checks the config still loads and renders correctly.
- **Apply the result**: `make apply` writes the renders into your real editor config — see [Usage](#usage).

## Usage

```bash
# preview — print the rendered config for every app, write nothing
uvx --from git+https://github.com/pjover/chordinate chordinate

# apply — write them into your live editor config
uvx --from git+https://github.com/pjover/chordinate chordinate --apply
```

By default this renders the bundled proposal. To use your own `keymap.json` instead, see [Tweaking the keymap](#tweaking-the-keymap) — put it at `~/.config/chordinate/keymap.json`, in the current directory, or wherever `$CHORDINATE_HOME` points.

### What `--apply` writes where

Config lives under `~/.config` on Linux and `~/Library/Application Support` on macOS — except Zed, which uses `~/.config` on both. From there:

| App       | Discovered from                                 | Written to                                |
| --------- | ----------------------------------------------- | ----------------------------------------- |
| VS Code   | `Code/User/`                                    | `Code/User/keybindings.json`              |
| Obsidian  | every vault in the `obsidian/obsidian.json` registry | `<vault>/.obsidian/hotkeys.json`     |
| Zed       | `zed/`                                          | `zed/keymap.json`                         |

An app you don't have installed is reported as `! no <app> targets found` and skipped — no directories are created for it. For every path that is found:

- **already identical** → skipped, nothing written (`= already up to date`)
- **file exists** → renamed to `<name>.bak-YYYYMMDD-HHMMSS`, then written (`~ backed up`), with the number of lines added and removed shown so you can see what it replaced
- **no file yet** → written (`+ wrote`)

VS Code, Obsidian and Zed pick up the new file on their own (restart Obsidian if it doesn't).

> **`--apply` replaces each file, it does not merge.** Any VS Code keybinding, Obsidian hotkey or Zed binding you added by hand and that isn't in your `keymap.json` disappears from the live file — it survives only in the timestamped backup next to it. Move anything you want to keep into your own `keymap.json` first (see [Tweaking the keymap](#tweaking-the-keymap)), then re-apply. (Zed's own defaults are unaffected: Zed layers `keymap.json` over them.)

## Development

```bash
make install   # uv sync
make test      # uv run pytest
make run       # uv run chordinate — print the renders
make apply     # uv run chordinate --apply — write them into your live config
make cheatsheet  # write cheatsheet.html, a printable (A4 landscape) sheet of every chord
```
