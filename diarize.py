import subprocess
import json
import os

def diarize_audio(audio_path, output_json="diarization.json"):
    cmd = [
        "whisperx",
        audio_path,
        "--diarize",
        "--hf_token", os.environ.get("HF_TOKEN", ""),
        "--output_format", "json",
        "--output_dir", "."
    ]

    subprocess.run(cmd, check=True)

    if not os.path.exists(output_json):
        raise FileNotFoundError("Diarization output JSON not found!")

    with open(output_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data
