import os
import csv
import soundfile as sf

# Paths (change these)
txt_dir = "/home/abdelrahman-khaled/Projects/SpeechProjects/SeqoonTTS/Data/Egyptian_Arabic_Conversational_Speech_Corpus/TXT"
wav_dir = "/home/abdelrahman-khaled/Projects/SpeechProjects/SeqoonTTS/Data/Egyptian_Arabic_Conversational_Speech_Corpus/WAV"
output_wav_dir = "/home/abdelrahman-khaled/Projects/SpeechProjects/SeqoonTTS/Data/Egyptian_Arabic_Conversational_Speech_Corpus/Clean"
output_csv_path = "/home/abdelrahman-khaled/Projects/SpeechProjects/SeqoonTTS/Data/Egyptian_Arabic_Conversational_Speech_Corpus/Clean/metadata.csv"

os.makedirs(output_wav_dir, exist_ok=True)

csv_data = []

for txt_file in os.listdir(txt_dir):
    if not txt_file.endswith(".txt"):
        continue

    base_name = os.path.splitext(txt_file)[0]
    txt_path = os.path.join(txt_dir, txt_file)
    wav_path = os.path.join(wav_dir, base_name + ".wav")

    if not os.path.exists(wav_path):
        print(f"Missing WAV for {txt_file}")
        continue

    # Load WAV file
    try:
        wav_data, sample_rate = sf.read(wav_path)
    except Exception as e:
        print(f"Error loading {wav_path}: {e}")
        continue

    # Read alignment data
    with open(txt_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            parts = line.strip().split("\t")
            if len(parts) != 4:
                continue

            time_part, speaker, gender, transcription = parts

            if "[*]" in transcription or not transcription.strip():
                continue  # skip noise or empty transcriptions

            # Extract start and end times
            try:
                start_str, end_str = time_part.strip("[]").split(",")
                start_time = float(start_str)
                end_time = float(end_str)
            except ValueError:
                continue

            start_sample = int(start_time * sample_rate)
            end_sample = int(end_time * sample_rate)

            segment = wav_data[start_sample:end_sample]
            segment_name = f"{base_name}_{i:03d}.wav"
            segment_path = os.path.join(output_wav_dir, segment_name)

            try:
                sf.write(segment_path, segment, sample_rate)
                csv_data.append([segment_name, transcription])
            except Exception as e:
                print(f"Error saving segment {segment_name}: {e}")

# Save metadata to CSV
with open(output_csv_path, "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["file_name", "transcription"])
    writer.writerows(csv_data)

print("✅ Done. Segments saved and metadata.csv created.")
