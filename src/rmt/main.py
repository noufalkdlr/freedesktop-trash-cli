import typer
from datetime import datetime
from pathlib import Path
import shutil
import questionary

app = typer.Typer()


class TrashManager:
    def __init__(self):
        self.trash_dir = Path.home() / ".local/share/Trash"
        self.trash_files_dir = self.trash_dir / "files"
        self.trash_info_dir = self.trash_dir / "info"

        self.trash_files_dir.mkdir(parents=True, exist_ok=True)
        self.trash_info_dir.mkdir(parents=True, exist_ok=True)

    def _resolve_name_collision(self, trash_dir: Path, target_path: Path) -> Path:
        base_trash_path = trash_dir / target_path.name

        unique_trash_path = base_trash_path
        if base_trash_path.exists():
            count = 2
            while unique_trash_path.exists():
                unique_trash_path = (
                    base_trash_path.parent
                    / f"{base_trash_path.stem}.{count}{base_trash_path.suffix}"
                )
                count += 1

        renamed_local_path = target_path.parent / unique_trash_path.name

        return target_path.rename(renamed_local_path)

    def move_to_trash(self, target_path: str | Path) -> None:
        target_path = Path(target_path).resolve()

        renamed_file_path = self._resolve_name_collision(
            trash_dir=self.trash_files_dir, target_path=target_path
        )
        shutil.move(renamed_file_path, self.trash_files_dir)

        info_file_path = self.trash_info_dir / f"{renamed_file_path.name}.trashinfo"
        deletion_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        content = f"[Trash Info]\nPath={target_path}\nDeletionDate={deletion_date}\n"

        info_file_path.write_text(content)

    def empty_trash(self) -> None:
        shutil.rmtree(self.trash_files_dir)
        shutil.rmtree(self.trash_info_dir)

        self.trash_files_dir.mkdir(parents=True, exist_ok=True)
        self.trash_info_dir.mkdir(parents=True, exist_ok=True)

        typer.secho("Trash cleaned successfully!", fg=typer.colors.GREEN)


@app.command(no_args_is_help=True)
def main(
    target_path: str | None = typer.Argument(None, help="Path to file or folder"),
    clean: bool = typer.Option(None, "--clean", "-c", help="Clean all trash files"),
) -> None:

    if clean:
        is_confirm = questionary.confirm(
            "Are you sure you want to empty the trash?"
        ).ask()
        if is_confirm:
            trash_manager = TrashManager()
            trash_manager.empty_trash()
        else:
            typer.secho("Operation cancelled.", fg=typer.colors.YELLOW)

    elif target_path:
        trash_manager = TrashManager()
        trash_manager.move_to_trash(target_path)


if __name__ == "__main__":
    app()
