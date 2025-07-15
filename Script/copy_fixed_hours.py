import os
import shutil
import random
import pandas as pd
from pathlib import Path
from pydub.utils import mediainfo

# === CONFIGURATION ===
INPUT_DIR = "/mnt/nvme1/Speech_datasets/Hend_Total"
OUTPUT_DIR = "/mnt/nvme1/Speech_datasets/Hend_output_6_hours_only"
METADATA_FILE = "/mnt/nvme1/Speech_datasets/Hend_Total/metadata.csv"
FILENAME_COLUMN = "file_name"  # change this if your CSV uses a different column name
TARGET_DURATION_SECONDS = 6 * 3600  # 6 hours

# === Get WAV duration using ffmpeg (via pydub) ===
def get_wav_duration(filepath):
    try:
        info = mediainfo(filepath)
        return float(info['duration'])
    except Exception as e:
        print(f"❌ Failed to get duration for {filepath}: {e}")
        return 0.0

# === Main Logic ===
def main():
    input_dir = Path(INPUT_DIR)
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load and shuffle metadata
    metadata_path = Path(METADATA_FILE)
    metadata = pd.read_csv(metadata_path)

    if FILENAME_COLUMN not in metadata.columns:
        raise ValueError(f"'{FILENAME_COLUMN}' column not found in metadata")

    shuffled = metadata.sample(frac=1, random_state=42).reset_index(drop=True)

    selected_rows = []
    accumulated_duration = 0.0

    for _, row in shuffled.iterrows():
        wav_name = row[FILENAME_COLUMN]
        wav_path = input_dir / wav_name

        if not wav_path.exists():
            print(f"⚠️ Skipping missing file: {wav_name}")
            continue

        duration = get_wav_duration(wav_path)
        if duration <= 0:
            continue

        if accumulated_duration + duration > TARGET_DURATION_SECONDS:
            break

        accumulated_duration += duration
        selected_rows.append(row)

        # Copy .wav file
        shutil.copy(wav_path, output_dir / wav_name)
    
    # Save selected metadata with same structure
    selected_metadata = pd.DataFrame(selected_rows)
    selected_metadata.to_csv(output_dir / "metadata.csv", index=False)

    print(f"\n✅ Done! Total duration copied: {accumulated_duration / 3600:.2f} hours ({len(selected_rows)} files)")

if __name__ == "__main__":
    main()
