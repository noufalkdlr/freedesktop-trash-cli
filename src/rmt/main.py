import typer
from datetime import datetime
from pathlib import Path
import shutil

app = typer.Typer()


class TrashManager:
    def __init__(self, target_path: str):
        self.target_path = Path(target_path).resolve()
        self.trash_dir = Path.home() / ".local/share/Trash"
        self.trash_files_dir = self.trash_dir / "files"
        self.trash_info_dir = self.trash_dir / "info"

    def move_to_trash(self):
        shutil.move(self.target_path, self.trash_files_dir)

    def create_trash_info(self):
        info_file_path = self.trash_info_dir / f"{self.target_path.name}.trashinfo"
        deletion_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        content = (
            f"[Trash Info]\nPath={self.target_path}\nDeletionDate={deletion_date}\n"
        )

        info_file_path.write_text(content)

    def delete(self):
        self.move_to_trash()
        self.create_trash_info()


@app.command()
def main(
    target_path: str,
) -> None:

    trash_manager = TrashManager(target_path)
    trash_manager.delete()


if __name__ == "__main__":
    app()
