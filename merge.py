import subprocess
from pathlib import Path

# =========================
# CONFIG
# =========================

# Path to 7zip
SEVEN_ZIP = r"C:\Program Files\7-Zip\7z.exe"

# Folder containing split files
ARCHIVE_FOLDER = Path(r"C:\Users\abhis\Downloads")

# First split file
FIRST_PART = ARCHIVE_FOLDER / "whisper_project.7z.001"

# Extraction output folder
OUTPUT_FOLDER = ARCHIVE_FOLDER / "EXTRACTED_PROJECT"

# =========================
# CREATE OUTPUT FOLDER
# =========================

OUTPUT_FOLDER.mkdir(exist_ok=True)

print("\n[1] Starting extraction...")

# =========================
# EXTRACT
# =========================

cmd = [
    SEVEN_ZIP,
    "x",
    str(FIRST_PART),
    f"-o{OUTPUT_FOLDER}",
    "-y"
]

result = subprocess.run(cmd)

# =========================
# RESULT
# =========================

if result.returncode == 0:
    print("\n[SUCCESS] Project extracted successfully.")
    print("\nLocation:")
    print(OUTPUT_FOLDER)
else:
    print("\n[ERROR] Extraction failed.")