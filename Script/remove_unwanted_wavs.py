import os
import csv

# === Fixed paths ===
WAV_DIR = '/home/abdelrahman-khaled/Projects/SpeechProjects/SeqoonTTS/Data/EGY_conv_speech_corpus/wavs'
CSV_PATH = '/home/abdelrahman-khaled/Projects/SpeechProjects/SeqoonTTS/Data/EGY_conv_speech_corpus/metadata.csv'

def get_filenames_from_csv(csv_path):
    """Extract all file names from the first column of the CSV."""
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # skip header
        return set(row[0] for row in reader)

def remove_unlisted_wavs(wav_dir, allowed_filenames):
    """Remove any .wav file in the directory that is not listed in the CSV."""
    removed = []
    for file in os.listdir(wav_dir):
        if file.lower().endswith('.wav') and file not in allowed_filenames:
            path = os.path.join(wav_dir, file)
            try:
                os.remove(path)
                removed.append(file)
                print(f"[REMOVE] {file}")
            except Exception as e:
                print(f"[ERROR] Failed to delete {file}: {e}")
    print(f"\n✅ Done. Removed {len(removed)} unlisted .wav files.")

if __name__ == '__main__':
    listed_files = get_filenames_from_csv(CSV_PATH)
    remove_unlisted_wavs(WAV_DIR, listed_files)
