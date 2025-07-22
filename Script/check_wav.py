import os
import soundfile as sf
import pandas as pd

# مسار ملفات الصوت
wav_dir = "/home/abdelrahman-khaled/Projects/SpeechProjects/Sai-TTS/Data/SeqoonData/Seqoon_DS/wavs"
# مسار ملف الميتاداتا
meta_path = "/home/abdelrahman-khaled/Projects/SpeechProjects/Sai-TTS/Data/SeqoonData/Seqoon_DS/metadata.csv"
# الحد الأدنى للعينات (مثلاً 1 ثانية = 48000 عينات لو 48kHz)
MIN_FRAMES = 48000  # عدل إذا تريد أقل من ثانية

# تحميل ملف الميتاداتا
df = pd.read_csv(meta_path, sep="|", header=None)
audio_files = set(df[0].astype(str) + ".wav")

found = set()
missing = []
too_short = []
corrupt = []
wrong_sr = []

for fname in sorted(audio_files):
    fpath = os.path.join(wav_dir, fname)
    if not os.path.exists(fpath):
        missing.append(fname)
        continue
    try:
        info = sf.info(fpath)
        if info.frames < MIN_FRAMES:
            too_short.append((fname, info.frames, info.samplerate, info.duration))
        if info.samplerate != 48000:
            wrong_sr.append((fname, info.samplerate))
        found.add(fname)
    except Exception as e:
        corrupt.append((fname, str(e)))

print("\n=== النتائج ===\n")
print(f"عدد الملفات المطلوبة في metadata: {len(audio_files)}")
print(f"عدد الملفات الموجودة فعلاً: {len(found)}")
print(f"عدد الملفات الناقصة: {len(missing)}")
if missing:
    print("ملفات ناقصة:")
    for m in missing:
        print("  ", m)
print(f"\nعدد الملفات القصيرة جدًا: {len(too_short)}")
if too_short:
    print("ملفات قصيرة جدًا:")
    for t in too_short:
        print(f"  {t[0]} -- frames: {t[1]}, samplerate: {t[2]}, duration: {t[3]:.2f}s")
print(f"\nعدد الملفات التالفة أو غير قابلة للقراءة: {len(corrupt)}")
if corrupt:
    print("ملفات تالفة:")
    for c in corrupt:
        print(f"  {c[0]} -- error: {c[1]}")
print(f"\nعدد الملفات التي معدل العينة لها ليس 48000Hz: {len(wrong_sr)}")
if wrong_sr:
    print("ملفات بمعدل عينة مختلف:")
    for ws in wrong_sr:
        print(f"  {ws[0]} -- samplerate: {ws[1]}")
print("\nانتهى الفحص.")
