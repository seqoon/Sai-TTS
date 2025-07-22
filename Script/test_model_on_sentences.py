import os
import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
"""
edit the following variables as preferences:
   1. `texts`: list of sentences we want to generate wavs for it
   2. `l.inference.temperature` model inference temperature try different values gradually between 0.55 : 0.75
   3. `BASE_DIR` : base dir containing the models, the next directories below are found in it.
   4. `TRAINING_DIR` :dir containing the checkpoints of the resulted from finetuning process.
   5. `TRAINING_DIR` dir containing the original files of the model resulted from fine-tuning process.
   6. `XTTS_CHECKPOINT` : path to the chosen checkpoint.
   7. `SPEAKER_REFERENCE` : sample wav of the speaker we want to clone in inference.

"""

# Define base directories
BASE_DIR = "/home/abdelrahman-khaled/Projects/SpeechProjects/Sai-TTS"
TRAINING_DIR = os.path.join(BASE_DIR, "models/seqoon_ckpt")

# Define paths
CONFIG_PATH = os.path.join(TRAINING_DIR, "config.json")
TOKENIZER_PATH = os.path.join(TRAINING_DIR, "vocab.json")
XTTS_CHECKPOINT = os.path.join(TRAINING_DIR, "best_model_31977.pth")
SPEAKER_REFERENCE = "/home/abdelrahman-khaled/Projects/SpeechProjects/Sai-TTS/Data/SeqoonData/wavs/H1-00001.wav"

# Output directory
OUTPUT_WAV_PATH = os.path.join(TRAINING_DIR, "output", "test_sentences_best_model_CS")
os.makedirs(OUTPUT_WAV_PATH, exist_ok=True)  # Ensure output directory exists

# Arabic texts for inference

texts = [
    "لو عايز تستثمر في وحدة على البحر، عندنا مشاريع مميزة وأسعار تبدأ من مليون جنية.",
    "عندنا وحدات جاهزة للتسليم الفوري وأقساط تبدأ من 7000 جنيه في الشهر من غير فوائد.",
    "فريق المبيعات بتاعنا هيشرحلك كل التفاصيل خطوة بخطوة وهيكون معاك لحد استلام وحدتك.",
    "إنت وصلت ولا لسه في الطريق؟",
    "أهلا أنا صاي مساعدك الرقمي",
    "مساء الفُل، أنا صاي، مساعدك الصوتي.",
    "على فكرة، عندنا عروض جديدة ممكن تفيدك، تحب أقولك عليها؟",
    "لو عندك أي مشكلة أو استفسار، أنا هنا عشان أساعدك"
]


print("Loading model...")
config = XttsConfig()
config.load_json(CONFIG_PATH)
model = Xtts.init_from_config(config)
model.load_checkpoint(
    config,
    checkpoint_path=XTTS_CHECKPOINT,
    vocab_path=TOKENIZER_PATH,
    use_deepspeed=False,  # Set to True if using DeepSpeed
    speaker_file_path="",  # Optional: Path to speaker file if using multi-speaker model
    checkpoint_dir=TRAINING_DIR,  # Directory of the checkpoint
)
model.cuda()  # Move model to GPU

# Compute speaker latents
print("Computing speaker latents...")
gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=[SPEAKER_REFERENCE])

# # Perform inference
print("Inference...")

 #Perform inference for each text
for idx, text in enumerate(texts):
    print(f"Synthesizing text {idx+1}/{len(texts)}...")
    out = model.inference(
        text=text,
        language="ar",  # Arabic
        gpt_cond_latent=gpt_cond_latent,
        speaker_embedding=speaker_embedding,
        temperature=0.65,                     #range-> 0.55:0.75
        length_penalty=1.0,
        repetition_penalty=2.0,
        top_k=50,
        top_p=0.8,
        speed=1.0,
        enable_text_splitting=False,
    )

    output_wav_path = os.path.join(OUTPUT_WAV_PATH, f"output_{idx+1}.wav")
    torchaudio.save(output_wav_path, torch.tensor(out["wav"]).unsqueeze(0), 24000)
    print(f"Output saved to {output_wav_path}")

print("Synthesis complete.")