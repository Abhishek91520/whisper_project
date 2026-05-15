from pathlib import Path
import zipfile

# =========================
# CONFIG
# =========================

PARTS_DIR = Path(r"C:\Users\abhis\Desktop\STT\PACKAGE_OUTPUT")

MERGED_ZIP = PARTS_DIR / "whisper_project_merged.zip"

EXTRACT_DIR = PARTS_DIR / "EXTRACTED_PROJECT"

# =========================
# FIND PART FILES
# =========================

part_files = sorted(
    PARTS_DIR.glob("whisper_project.zip.part*")
)

print("\n[1] Found Parts:")

for p in part_files:
    print(p.name)

# =========================
# MERGE
# =========================

print("\n[2] Merging parts...")

with open(MERGED_ZIP, "wb") as merged:

    for part in part_files:

        print(f"Adding: {part.name}")

        with open(part, "rb") as pf:

            while True:

                chunk = pf.read(1024 * 1024)

                if not chunk:
                    break

                merged.write(chunk)

print("[OK] Merge completed.")

# =========================
# VALIDATE ZIP
# =========================

print("\n[3] Validating zip...")

if not zipfile.is_zipfile(MERGED_ZIP):
    print("[ERROR] Merged file is NOT valid zip.")
    exit()

print("[OK] Zip validation successful.")

# =========================
# EXTRACT
# =========================

print("\n[4] Extracting...")

EXTRACT_DIR.mkdir(exist_ok=True)

with zipfile.ZipFile(MERGED_ZIP, "r") as zipf:
    zipf.extractall(EXTRACT_DIR)

print("\n[SUCCESS] Extraction completed.")

print("\nExtracted To:")
print(EXTRACT_DIR)