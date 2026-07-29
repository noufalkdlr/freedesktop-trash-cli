# rmt

A safer `rm`. `rmt` moves files and folders to your system trash instead of deleting them permanently — with full compliance to the [XDG Trash Specification](https://specifications.freedesktop.org/trash-spec/latest/), so trashed items show up correctly in your file manager (Dolphin, Nautilus, Thunar, etc.) and can be restored.

## Why

`rm` is unforgiving. One typo, one wrong glob, and the file is gone. `rmt` gives you the same instant, no-confirmation-dialog workflow from the terminal, but every deletion is recoverable until you empty the trash yourself.

## Features

- 🗑️ Moves files/folders to `~/.local/share/Trash` instead of deleting them
- 📋 Writes proper `.trashinfo` metadata (original path + deletion timestamp) per the XDG spec
- 🔄 Fully compatible with GUI file managers' trash/restore functionality
- 🧹 `--clean` flag to empty the trash, with a confirmation prompt
- ⚡ Zero-config, single binary-like CLI via `uv`

## Installation

### Using `uv` (recommended)

```bash
uv tool install .
```

This installs `rmt` as an isolated, system-wide command without needing to manage a virtual environment.

### From source

```bash
git clone https://github.com/<your-username>/rmt.git
cd rmt
uv sync
uv run rmt --help
```

### Uninstalling

```bash
uv tool uninstall rmt
```

## Usage

### Trashing a file

```bash
rmt path/to/file_or_folder
```

That's it. The target is moved to `~/.local/share/Trash/files/` and a matching `.trashinfo` entry is written to `~/.local/share/Trash/info/`, recording:

```ini
[Trash Info]
Path=/absolute/original/path
DeletionDate=2026-07-24T12:19:00
```

If a file with the same name already exists in the trash, `rmt` automatically renames the incoming one (`file.2.txt`, `file.3.txt`, ...) instead of overwriting it.

### Emptying the trash

```bash
rmt --clean
# or
rmt -c
```

This asks for confirmation before permanently deleting everything in `~/.local/share/Trash/files` and `~/.local/share/Trash/info`. Answer `y` to proceed or `n` to cancel — nothing is removed until you confirm.

### Restoring a file

Open your file manager's Trash view and restore normally — since `rmt` follows the XDG spec, restoration works exactly like it would for anything deleted through the GUI.

## Requirements

- Python ≥ 3.14
- [`typer`](https://typer.tiangolo.com/) ≥ 0.27.0
- [`questionary`](https://github.com/tmbo/questionary)

## How it works

`rmt` is intentionally minimal — a single `TrashManager` class handles the core responsibilities:

| Step              | What happens                                                                                                                                               |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `move_to_trash()` | Resolves name collisions, moves the target into `~/.local/share/Trash/files`, and writes a `.trashinfo` file recording the original path and deletion time |
| `empty_trash()`   | Clears both `files/` and `info/` directories after user confirmation                                                                                       |

No daemons, no background processes, no config files to set up.

## Roadmap

- [ ] `rmt --list` — view trashed items
- [ ] `rmt --restore <name>` — restore without opening a file manager

## License

MIT
