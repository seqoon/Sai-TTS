import csv
import re

# Settings
input_file = '/home/abdelrahman-khaled/Projects/Data/All/Raghda/wavs/metadata.csv'
valid_file = '/home/abdelrahman-khaled/Projects/Data/All/Raghda/wavs/valid.csv'
not_valid_file = '/home/abdelrahman-khaled/Projects/Data/All/Raghda/wavs/not_valid.csv'
MAX_CHARS = 166

# Digit maps: Arabic-Indic (U+0660–0669) and Eastern Arabic-Indic / Persian (U+06F0–06F9)
ARABIC_TO_EN_DIGITS = str.maketrans({
    "٠":"0","١":"1","٢":"2","٣":"3","٤":"4","٥":"5","٦":"6","٧":"7","٨":"8","٩":"9",
    "۰":"0","۱":"1","۲":"2","۳":"3","۴":"4","۵":"5","۶":"6","۷":"7","۸":"8","۹":"9",
})

def normalize_text(text):
    # Trim
    text = text.strip()

    # Letter normalization
    text = text.replace("ڤ", "ف")

    # Digit normalization (Arabic → English)
    text = text.translate(ARABIC_TO_EN_DIGITS)

    # Punctuation & spacing normalization
    text = re.sub(r'[{}!,:;\'\"“”‘’“”()،؟\.]', '', text)  # Remove western & Arabic punctuation
    text = re.sub(r'[…]+', '.', text)                     # Replace ellipsis
    text = re.sub(r'\.{2,}', '.', text)                   # Multiple dots → single dot
    text = re.sub(r'!{2,}', '!', text)                    # Multiple exclamations → one
    text = re.sub(r'\s+', ' ', text)                      # Collapse whitespace
    return text

def contains_english(text):
    """Check if the string contains any English letters (A–Z, a–z)."""
    return bool(re.search(r'[A-Za-z]', text))

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(valid_file, 'w', encoding='utf-8', newline='') as valid_outfile, \
     open(not_valid_file, 'w', encoding='utf-8', newline='') as not_valid_outfile:

    reader = csv.DictReader(infile)  # expects header: file_name,text
    valid_writer = csv.writer(valid_outfile, delimiter=',')
    not_valid_writer = csv.writer(not_valid_outfile, delimiter=',')

    # write headers
    valid_writer.writerow(["file_name", "text"])
    not_valid_writer.writerow(["file_name", "text"])

    valid_count = 0
    not_valid_count = 0

    for row in reader:
        file_name = row.get("file_name", "")
        text = normalize_text(row.get("text", ""))

        # Rule: must not exceed max length AND must not contain English letters
        if len(text) <= MAX_CHARS and not contains_english(text):
            valid_writer.writerow([file_name, text])
            valid_count += 1
        else:
            not_valid_writer.writerow([file_name, text])
            not_valid_count += 1

print(f"✅ Done. Normalized and split into 'valid.csv' and 'not_valid.csv'.")
print(f"✔ Finished processing. Valid: {valid_count}, Not valid: {not_valid_count}")
