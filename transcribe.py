# transcribe.py
import subprocess
import tempfile
from pathlib import Path
import whisper

model = whisper.load_model("base")

def extract_segment_audio(input_audio, start, end, out_path):
    # Use ffmpeg to extract the time range
    cmd = [
        "ffmpeg", "-y", "-i", input_audio,
        "-ss", str(start), "-to", str(end),
        "-ar", "16000", "-ac", "1", "-vn",
        out_path
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return out_path

def transcribe_segment(input_audio, start, end):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmpname = tmp.name
    extract_segment_audio(input_audio, start, end, tmpname)
    res = model.transcribe(tmpname)
    text = res.get("text", "").strip()
    Path(tmpname).unlink(missing_ok=True)
    return text
