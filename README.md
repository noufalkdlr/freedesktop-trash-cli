# rmt

A safer `rm`. `rmt` moves files and folders to your system trash instead of deleting them permanently — with full compliance to the [XDG Trash Specification](https://specifications.freedesktop.org/trash-spec/latest/), so trashed items show up correctly in your file manager (Dolphin, Nautilus, Thunar, etc.) and can be restored.

## Why

`rm` is unforgiving. One typo, one wrong glob, and the file is gone. `rmt` gives you the same instant, no-confirmation-dialog workflow from the terminal, but every deletion is recoverable until you empty the trash yourself.

## Features

- 🗑️ Moves files/folders to `~/.local/share/Trash` instead of deleting them
- 📋 Writes proper `.trashinfo` metadata (original path + deletion timestamp) per the XDG spec
- 🔄 Fully compatible with GUI file managers' trash/restore functionality
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

## Usage

```bash
rmt path/to/file_or_folder
```

That's it. The target is moved to `~/.local/share/Trash/files/` and a matching `.trashinfo` entry is written to `~/.local/share/Trash/info/`, recording:

```ini
[Trash Info]
Path=/absolute/original/path
DeletionDate=2026-07-24T12:19:00
```

### Restoring a file

Open your file manager's Trash view and restore normally — since `rmt` follows the XDG spec, restoration works exactly like it would for anything deleted through the GUI.

## Requirements

- Python ≥ 3.14
- [`typer`](https://typer.tiangolo.com/) ≥ 0.27.0

## How it works

`rmt` is intentionally minimal — a single `TrashManager` class handles two responsibilities:

| Step                  | What happens                                                             |
| --------------------- | ------------------------------------------------------------------------ |
| `move_to_trash()`     | Moves the resolved target path into `~/.local/share/Trash/files`         |
| `create_trash_info()` | Writes a `.trashinfo` file recording the original path and deletion time |

No daemons, no background processes, no config files to set up.

## Roadmap

- [ ] `rmt --list` — view trashed items
- [ ] `rmt --restore <name>` — restore without opening a file manager
- [ ] `rmt --empty` — permanently clear the trash
- [ ] Conflict handling when a file of the same name already exists in trash

## License

MIT
