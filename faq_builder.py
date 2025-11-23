from collections import defaultdict

def identify_teacher(segments):
    
    durations = defaultdict(float)
    for s in segments:
        durations[s["speaker"]] += (s["end"] - s["start"])
    teacher = max(durations.items(), key=lambda kv: kv[1])[0]
    return teacher


# 2. Mark segments as Teacher / Student
def merge_adjacent_teacher_segments(segments, teacher_id, max_gap=1.0):
    """
    Produces new segments list where speaker roles are normalized to 'Teacher' or 'Student'
    """
    out = []
    for s in segments:
        role = "Teacher" if s["speaker"] == teacher_id else "Student"
        out.append({**s, "role": role})
    return out


# 3. Question detection logic
QUESTION_STARTERS = (
    "what", "why", "how", "when", "where", "who", "which",
    "could", "can", "would", "is", "are", "do", "does", "did"
)

def is_question(text):
    if not text or len(text) < 3:
        return False

    t = text.strip()

    # punctuation check
    if t.endswith("?"):
        return True

    low = t.lower()

    # starts with question words
    if any(low.startswith(ws + " ") or low.startswith(ws + "?")
           for ws in QUESTION_STARTERS):
        return True

    # contains question-like phrases
    if "could you" in low or "can you" in low or "please explain" in low:
        return True

    return False


# 4. Find teacher answer to each question
def find_teacher_answer(segments, q_index, max_search_seconds=30):
    """
    segments: list of dicts with 'start', 'end', 'role', 'text'
    q_index: index of the question segment
    Returns concatenated teacher answer text (or None)
    """
    q_end = segments[q_index]["end"]
    answer_texts = []

    for i in range(q_index + 1, len(segments)):
        s = segments[i]

        # Stop if too far in time
        if s["start"] - q_end > max_search_seconds:
            break

        if s["role"] == "Teacher":
            answer_texts.append(s.get("text", "").strip())

        # If student starts again soon after, teacher likely finished
        if s["role"] == "Student" and s["start"] - q_end > 0.2:
            break

    if answer_texts:
        return " ".join(answer_texts)

    return None
