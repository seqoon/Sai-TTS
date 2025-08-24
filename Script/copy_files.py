import os
import shutil
import csv
from tqdm import tqdm  # ✅ import tqdm

# User input: paths (edit as needed)
wav_dirs = [
    "/home/abdelrahman-khaled/Projects/Data/All/Seqoon_DS/wavs"
]  # ✅ Add as many dirs as you want

csv_file = "/home/abdelrahman-khaled/Projects/Data/All/Seqoon_DS/valid.csv"
new_wav_dir = "/home/abdelrahman-khaled/Projects/Data/All/Seqoon_DS/wav"

# Make sure the destination directory exists
os.makedirs(new_wav_dir, exist_ok=True)

# Read file names from CSV
file_names = set()
with open(csv_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        fname = row["file_name"].strip()
        file_names.add(fname)

# Copy files with progress bar
for fname in tqdm(file_names, desc="Copying files", unit="file"):
    found = False
    for wav_dir in wav_dirs:
        src = os.path.join(wav_dir, fname)
        if os.path.isfile(src):
            dst = os.path.join(new_wav_dir, fname)
            shutil.copy2(src, dst)
            # tqdm.write lets you log messages without breaking the bar
            tqdm.write(f"Copied: {fname} (from {wav_dir})")
            found = True
            break  # stop searching once found
    if not found:
        tqdm.write(f"File not found in any directory: {fname}")

print("✅ Done copying!")
