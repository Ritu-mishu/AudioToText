# notes_builder.py

import json

def build_notes(transcript_text):


    if not transcript_text:
        return "No transcript available."

    lines = transcript_text.split(".")
    clean = [l.strip() for l in lines if len(l.strip()) > 3]

    notes = "## 📝 Lecture Notes\n"
    for i, line in enumerate(clean, start=1):
        notes += f"- {line}.\n"

    return notes
