from pathlib import Path
import shutil

target = Path("a").resolve()

if target.exists():
    shutil.rmtree(target)

target.mkdir(parents=True, exist_ok=True)
