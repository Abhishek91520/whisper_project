import os
import shutil
import subprocess
from pathlib import Path

# =========================
# CONFIGURATION
# =========================

PROJECT_NAME = "whisper_project"

# Your project folder
PROJECT_DIR = Path(r"C:\Users\abhis\Desktop\STT\whisper_project")

# Temporary build folder
BUILD_DIR = PROJECT_DIR.parent / f"{PROJECT_NAME}_BUILD"

# Final output folder
OUTPUT_DIR = PROJECT_DIR.parent / "OUTPUT_PACKAGE"

# Split size for GitHub safe upload
# 90m = 90 MB
SPLIT_SIZE = "90m"

# 7zip executable path
SEVEN_ZIP = r"C:\Program Files\7-Zip\7z.exe"

# =========================
# CLEAN OLD BUILD
# =========================

if BUILD_DIR.exists():
    shutil.rmtree(BUILD_DIR)

if OUTPUT_DIR.exists():
    shutil.rmtree(OUTPUT_DIR)

BUILD_DIR.mkdir(parents=True)
OUTPUT_DIR.mkdir(parents=True)

print("\n[1] Creating clean build folder...")

# =========================
# COPY PROJECT
# =========================

IGNORE_FOLDERS = {
    "__pycache__",
    ".git",
    ".idea",
    ".vscode",
    "OUTPUT_PACKAGE",
}

IGNORE_EXTENSIONS = {
    ".pyc",
    ".log",
}

def should_ignore(path: Path):
    if path.name in IGNORE_FOLDERS:
        return True

    if path.suffix.lower() in IGNORE_EXTENSIONS:
        return True

    return False


for item in PROJECT_DIR.iterdir():

    if should_ignore(item):
        continue

    dest = BUILD_DIR / item.name

    if item.is_dir():
        shutil.copytree(item, dest)
    else:
        shutil.copy2(item, dest)

print("[OK] Project copied.")

# =========================
# CREATE REQUIREMENTS.TXT
# =========================

print("\n[2] Generating requirements.txt...")

requirements_file = BUILD_DIR / "requirements.txt"

with open(requirements_file, "w", encoding="utf-8") as f:
    result = subprocess.run(
        ["pip", "freeze"],
        capture_output=True,
        text=True
    )

    f.write(result.stdout)

print("[OK] requirements.txt created.")

# =========================
# CREATE README
# =========================

print("\n[3] Creating README_SETUP.txt...")

readme = BUILD_DIR / "README_SETUP.txt"

readme.write_text(
    """
SETUP INSTRUCTIONS

1. Install Python

2. Create venv:
   python -m venv venv

3. Activate:
   venv\\Scripts\\activate

4. Install requirements:
   pip install -r requirements.txt

5. Run app:
   python app.py

IMPORTANT:
- Keep models folder in same directory
- Install GPU torch separately if needed
""",
    encoding="utf-8"
)

print("[OK] README created.")

# =========================
# CREATE SPLIT ZIP
# =========================

print("\n[4] Creating split archive...")

archive_path = OUTPUT_DIR / f"{PROJECT_NAME}.7z"

cmd = [
    SEVEN_ZIP,
    "a",
    str(archive_path),
    str(BUILD_DIR),
    f"-v{SPLIT_SIZE}"
]

result = subprocess.run(cmd)

if result.returncode == 0:
    print("\n[SUCCESS] Split package created.")
else:
    print("\n[ERROR] Failed creating archive.")

# =========================
# FINAL INFO
# =========================

print("\n===================================")
print("OUTPUT LOCATION:")
print(OUTPUT_DIR)
print("===================================")

print("\nUpload all generated .7z files to GitHub.")
print("On VM: download all parts and extract first file.")