import os
import csv

# Edit these paths
wav_dir = "/home/abdelrahman-khaled/Projects/Data/All/Seqoon_DS/wav"
csv_file = "/home/abdelrahman-khaled/Projects/Data/All/Seqoon_DS/valid.csv"

# Read all rows from CSV
with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Filter rows: keep only if the file exists
filtered_rows = [
    row for row in rows
    if os.path.isfile(os.path.join(wav_dir, row["file_name"].strip()))
]

# Write filtered rows back to CSV (overwrite)
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["file_name", "transcription"])
    writer.writeheader()
    writer.writerows(filtered_rows)

print(f"Done! {len(filtered_rows)} rows remain in the CSV.")
