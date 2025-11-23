# faq_pipeline.py
from diarize import diarize_audio
from transcribe import transcribe_segment
from faq_builder import identify_teacher, merge_adjacent_teacher_segments, is_question, find_teacher_answer

def build_notes_with_faq(audio_path):
    diarized = diarize_audio(audio_path)  # list of {'start','end','speaker'}
    # Transcribe each diarized segment
    segments = []
    for d in diarized:
        text = transcribe_segment(audio_path, d["start"], d["end"])
        segments.append({**d, "text": text})
    # identify teacher
    teacher_id = identify_teacher(segments)
    segments = merge_adjacent_teacher_segments(segments, teacher_id)
    # find questions and pair answers
    faq_items = []
    for idx, seg in enumerate(segments):
        if seg["role"] == "Student" and is_question(seg["text"]):
            answer = find_teacher_answer(segments, idx)
            if answer:
                faq_items.append({
                    "question": seg["text"],
                    "answer": answer,
                    "q_time": seg["start"]
                })
    # Build final notes text (you probably already build notes elsewhere; append FAQ)
    # here, create a text block for FAQ
    faq_text = "\n\n## Frequently Asked Questions (auto-generated)\n"
    for i, qa in enumerate(faq_items, start=1):
        faq_text += f"\n### Q{i}. {qa['question']}\nA: {qa['answer']}\n"
    return faq_text, faq_items
