import os
import zipfile
from pathlib import Path

# =========================
# CONFIG
# =========================

PROJECT_DIR = Path(r"C:\Users\abhis\Desktop\STT\whisper_project")

OUTPUT_DIR = PROJECT_DIR.parent / "PACKAGE_OUTPUT"

ZIP_NAME = "whisper_project.zip"

# GitHub safe size
PART_SIZE = 90 * 1024 * 1024  # 90 MB

# Ignore folders
IGNORE_FOLDERS = {
    "__pycache__",
    ".git",
    ".vscode",
}

# =========================
# CREATE OUTPUT
# =========================

OUTPUT_DIR.mkdir(exist_ok=True)

ZIP_PATH = OUTPUT_DIR / ZIP_NAME

print("\n[1] Creating zip...")

# =========================
# CREATE ZIP
# =========================

with zipfile.ZipFile(
    ZIP_PATH,
    "w",
    zipfile.ZIP_DEFLATED
) as zipf:

    for root, dirs, files in os.walk(PROJECT_DIR):

        dirs[:] = [
            d for d in dirs
            if d not in IGNORE_FOLDERS
        ]

        for file in files:

            filepath = Path(root) / file

            arcname = filepath.relative_to(PROJECT_DIR)

            zipf.write(filepath, arcname)

print("[OK] Zip created.")

# =========================
# SPLIT ZIP
# =========================

print("\n[2] Splitting zip...")

with open(ZIP_PATH, "rb") as f:

    part_num = 1

    while True:

        chunk = f.read(PART_SIZE)

        if not chunk:
            break

        part_path = OUTPUT_DIR / f"{ZIP_NAME}.part{part_num:03d}"

        with open(part_path, "wb") as part_file:
            part_file.write(chunk)

        print(f"[OK] Created: {part_path.name}")

        part_num += 1

print("\n[SUCCESS] Package ready.")

print("\nOutput folder:")
print(OUTPUT_DIR)