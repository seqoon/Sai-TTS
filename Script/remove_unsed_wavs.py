import os
import csv
import subprocess

# === Fixed paths ===
WAV_DIR = '/home/abdelrahman-khaled/Projects/SpeechProjects/SeqoonTTS/Data/EGY_conv_speech_corpus/wavs'                  # Path to your .wav files
CSV_PATH = '/home/abdelrahman-khaled/Projects/SpeechProjects/SeqoonTTS/Data/EGY_conv_speech_corpus/metadata.csv'         # Path to your metadata CSV
MIN_DURATION = 1.0                       # Minimum duration in seconds

def get_wav_duration(filepath):
    """Return duration of a wav file using sox."""
    try:
        result = subprocess.run(
            ['sox', '--i', '-D', filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return float(result.stdout.strip())
    except Exception as e:
        print(f"[ERROR] Failed to get duration for {filepath}: {e}")
        return 0.0

def clean_short_wavs():
    """Remove .wav files shorter than MIN_DURATION and update metadata CSV."""
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = list(csv.reader(csvfile))
        header = reader[0]
        rows = reader[1:]

    new_rows = []
    removed_files = []

    for row in rows:
        file_name = row[0]
        wav_path = os.path.join(WAV_DIR, file_name)

        if os.path.exists(wav_path):
            duration = get_wav_duration(wav_path)
            if duration >= MIN_DURATION:
                new_rows.append(row)
            else:
                print(f"[REMOVE] {file_name} — {duration:.2f}s")
                os.remove(wav_path)
                removed_files.append(file_name)
        else:
            print(f"[WARN] Missing file: {file_name}")

    # Rewrite cleaned CSV
    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(new_rows)

    print(f"\n✅ Done. Removed {len(removed_files)} short .wav files.")

if __name__ == '__main__':
    clean_short_wavs()
