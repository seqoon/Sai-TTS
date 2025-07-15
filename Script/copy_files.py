import os
import shutil
import csv

# User input: paths (edit as needed)
wav_dir = "/home/abdelrahman-khaled/Projects/SpeechProjects/SeqoonTTS/Data/SeqoonData/wavs"
csv_file = "/home/abdelrahman-khaled/Projects/SpeechProjects/SeqoonTTS/Data/SeqoonData/metadata_clean.csv"
new_wav_dir = "/home/abdelrahman-khaled/Projects/SpeechProjects/SeqoonTTS/Data/SeqoonData/wav_dir"

# Make sure the destination directory exists
os.makedirs(new_wav_dir, exist_ok=True)

# Read file names from CSV
file_names = set()
with open(csv_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Remove any accidental whitespace
        fname = row["file_name"].strip()
        file_names.add(fname)

# Copy files
for fname in file_names:
    src = os.path.join(wav_dir, fname)
    dst = os.path.join(new_wav_dir, fname)
    if os.path.isfile(src):
        shutil.copy2(src, dst)
        print(f"Copied: {fname}")
    else:
        print(f"File not found: {fname}")

print("Done copying!")
