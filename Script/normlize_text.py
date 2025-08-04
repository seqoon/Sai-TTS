import csv

# تحويل الأرقام العربية إلى إنجليزية
def convert_arabic_digits_to_english(text):
    arabic_to_english_digits = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
    return text.translate(arabic_to_english_digits)

# استبدال "ڤ" بـ "ف" وتطبيق تحويل الأرقام
def clean_text(text):
    if not text:
        return text
    text = text.replace("ڤ", "ف")
    text = convert_arabic_digits_to_english(text)
    return text

# مسار الملف الأصلي والملف الناتج
input_file = "/home/abdelrahman-khaled/Projects/SpeechProjects/Sai-TTS/Data/Nour_Data/metadata_sep.csv"
output_file = "/home/abdelrahman-khaled/Projects/SpeechProjects/Sai-TTS/Data/Nour_Data//output.csv"

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8", newline='') as outfile:
    reader = csv.reader(infile, delimiter="|")
    writer = csv.writer(outfile, delimiter="|")

    for row in reader:
        cleaned_row = [clean_text(cell) for cell in row]
        writer.writerow(cleaned_row)

print("تم تحويل الملف بنجاح إلى:", output_file)
