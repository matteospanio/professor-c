import zipfile
import os
from pathlib import Path

def extract_submissions(zip_path: str, target_dir: str):
    """Unzip folder and organize each student's exam in a subfolder."""
    os.makedirs(target_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(target_dir)

    students = []

    for src in Path(target_dir).glob("**/*.c"):
        os.rename(
            src,
            src.parent / "main.c"
        )
        students.append(src.parent.name.split("_")[0])

    return students
