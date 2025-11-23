import subprocess
import json
import os

def run_diarization(audio_path, output_json="diarization.json"):
    """
    Runs WhisperX diarization using built-in speaker embedding + clustering.
    Does NOT require pyannote.audio.
    Produces diarization.json containing segments + speaker labels.
    """

    cmd = [
        "whisperx",
        audio_path,
        "--diarize",
        "--hf_token", os.environ.get("HF_TOKEN", ""),  # optional HF token
        "--output_format", "json",
        "--output_dir", "."
    ]

    # Execute diarization
    subprocess.run(cmd, check=True)

    # Check if output exists
    if not os.path.exists(output_json):
        raise FileNotFoundError(
            f"Diarization output '{output_json}' not found in current directory."
        )

    # Load diarization segments
    with open(output_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data
