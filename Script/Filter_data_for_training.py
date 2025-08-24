import csv
import re
from pyarabic.araby import strip_tashkeel, normalize_ligature  # Ensure pyarabic is installed


def format_number_sequence(sequence):
    """
    Add spaces between digits of a 10-digit number.
    """
    if len(sequence) == 10 and sequence.isdigit():
        return ' '.join(sequence)
    return sequence


def clean_text(text):
    """
    Cleans and normalizes Arabic text:
    - Removes diacritics.
    - Normalizes ligatures.
    - Normalizes Arabic letters (أ -> ا, ة -> ه).
    - Removes specified punctuation: ,, ؟؟ . ؛ ; : ) ( !!
    - Removes "-" unless between numbers.
    - Removes number sequences ending with "."
    - Replaces multiple consecutive dots ("...") with a single dot (".").
    - Removes extra spaces and unwanted characters like "، . ' ،".
    - Normalizes whitespace.
    """
    
    # Remove specified punctuation except "."
    text = re.sub(r"[,\?\؟؛;:)(!]+", "", text)

    # Remove "-" unless between numbers
    text = re.sub(r"(?<!\d)-|-(?!\d)", "", text)

    # Remove number sequences ending with "."
    text = re.sub(r"\b\d+\.\s?", "", text)

    # Replace multiple dots with a single dot
    text = re.sub(r"\.{2,}", ".", text)

    # Remove specific unwanted characters: "، . ' ،"
    text = re.sub(r"[،.']", "", text)

    # Normalize ligatures (e.g., لا)
    text = normalize_ligature(text)

    # Normalize Arabic letters
    text = text.replace("أ", "ا").replace("ة", "ه")

    # Normalize whitespace (remove extra spaces)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def process_csv(input_file, output_file, long_text_file, filtered_file):
    """
    Processes a CSV file to:
    - Remove ".wav" from file_name.
    - Separate 10-digit numeric sequences with spaces.
    - Clean and normalize transcription text.
    - Remove specified punctuation and unwanted characters.
    - Remove multiple consecutive dots.
    - Remove specific unwanted characters: "، . ' ،".
    - Remove records containing 'الساعه'.
    - Filter records where transcription length exceeds 160 characters.
    """
    long_text_records = []
    filtered_records = []

    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8', newline='') as outfile, \
         open(long_text_file, 'w', encoding='utf-8', newline='') as longfile, \
         open(filtered_file, 'w', encoding='utf-8', newline='') as filterfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        long_writer = csv.writer(longfile)
        filter_writer = csv.writer(filterfile)

        # Read and write the header row
        header = next(reader, None)
        if header:
            writer.writerow(header)
            long_writer.writerow(header)
            filter_writer.writerow(header)
        
        # Process each row
        for row in reader:
            if len(row) < 2:
                continue  # Skip rows with insufficient columns

            file_name = row[0]  # First column (file name)
            transcription = row[1]  # Second column (text)

            # Remove ".wav" extension from file_name
            file_name = file_name.replace(".wav", "")

            # Format 10-digit sequences in transcription
            transcription = re.sub(r'\b\d{10}\b', lambda x: format_number_sequence(x.group()), transcription)

            # Clean and normalize the transcription
            transcription = clean_text(transcription)
            
            # Check if the transcription contains 'الساعه'
            # if 'الساعه' in transcription:
            #     filtered_records.append([file_name, transcription])
            #     filter_writer.writerow([file_name, transcription])
            #     continue  # Skip writing this record to the cleaned metadata file

            # Check transcription length
            if len(transcription) > 160:
                long_text_records.append([file_name, transcription])
                long_writer.writerow([file_name, transcription])
            else:
                writer.writerow([file_name, transcription])


if __name__ == "__main__":
    input_csv = "/home/abdelrahman-khaled/Projects/SpeechProjects/Sai-TTS/Data/SeqoonData/Seqoon_DS/metadata.csv"          # Input metadata file (audio_filename, text)
    output_csv = "./metadata_clean.csv" # Cleaned metadata file  (used in the training)
    long_text_csv = "./metadata_long.csv"     # Records with text > 160 characters  (filenames,transcriptions) where transcription text is more than 160 characters (model limitation)
    filtered_csv = "./filtered_output_csv" # 
    
    process_csv(input_csv, output_csv, long_text_csv, filtered_csv)