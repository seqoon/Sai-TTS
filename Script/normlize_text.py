import pandas as pd
import re

# Arabic text normalization function
def normalize_arabic(text):
    arabic_numbers = {'٠':'0','١':'1','٢':'2','٣':'3','٤':'4',
                      '٥':'5','٦':'6','٧':'7','٨':'8','٩':'9'}
    for ar_num, en_num in arabic_numbers.items():
        text = text.replace(ar_num, en_num)
    text = re.sub(r'[^\w\s]', ' ', text)  # remove special characters
    text = re.sub(r'\s+', ' ', text).strip()  # clean up extra spaces
    return text

# Load CSV file (pipe-separated, no headers)
input_csv = "/home/abdelrahman-khaled/Projects/SpeechProjects/Sai-TTS/Data/SeqoonData/Seqoon_DS/metadata.csv"
output_csv = "/home/abdelrahman-khaled/Projects/SpeechProjects/Sai-TTS/Data/SeqoonData/Seqoon_DS/normalized_dataset.csv"

# Columns: 0 = file_name, 1 = text, 2 = normlized
df = pd.read_csv(input_csv, sep='|', header=None, names=['file_name', 'text', 'normlized'])

# Apply normalization on 'text' and save result into both 'text' and 'normlized'
df['text'] = df['text'].astype(str).apply(normalize_arabic)
df['normlized'] = df['text']

# Save normalized dataset
df.to_csv(output_csv, sep='|', header=False, index=False, encoding='utf-8')

print(f"Normalization completed. Saved to '{output_csv}'.")
