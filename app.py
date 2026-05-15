from faster_whisper import WhisperModel

# Load multilingual small model
model = WhisperModel(
     r"./models/faster-whisper-small",
    device="cpu",
    compute_type="int8"
)

# Transcribe audio
segments, info = model.transcribe(
    "audio.m4a",
    beam_size=5
)

print("Detected language:", info.language)
print("Language probability:", info.language_probability)

print("\nTranscription:\n")

for segment in segments:
    print(segment.text)