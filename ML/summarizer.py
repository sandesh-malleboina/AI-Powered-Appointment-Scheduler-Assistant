# ML/summarizer.py

import spacy
import re
import dateparser
from datetime import datetime

# Load transformer-based SpaCy model once
nlp = spacy.load("en_core_web_trf")

# Predefined medical departments
DEPARTMENTS = [
    "Cardiology", "Radiology", "ENT", "Dermatology",
    "Neurology", "Orthopedics", "Pediatrics", "Oncology"
]

# -----------------------------
# Helper functions
# -----------------------------
def clean_date_text(text: str) -> str:
    """Clean OCR-extracted date/time text."""
    if not text:
        return text
    # Replace 'O' or 'o' with zero when between digits (e.g., 2O25 → 2025)
    text = re.sub(r'(\d)[Oo](\d)', lambda m: m.group(1) + "0" + m.group(2), text)
    # Remove stray quotes and odd characters
    text = text.replace("’", "").replace("‘", "").replace("`", "").replace("'", "")
    return text.strip()

def normalize_date_time(date_text: str, time_text: str, base_datetime=None):
    """Parse date and time into normalized formats."""
    parsed_date, parsed_time = None, None
    if base_datetime is None:
        base_datetime = datetime.now()

    if date_text:
        date_text = clean_date_text(date_text)
        dt = dateparser.parse(date_text, settings={'RELATIVE_BASE': base_datetime})
        if dt:
            parsed_date = dt.strftime("%Y-%m-%d")

    if time_text:
        time_text = clean_date_text(time_text)
        dt_time = dateparser.parse(time_text, settings={'RELATIVE_BASE': base_datetime})
        if dt_time:
            parsed_time = dt_time.strftime("%H:%M")

    return parsed_date, parsed_time

# -----------------------------
# Main extraction functions
# -----------------------------
def extract_appointment(text: str):
    """Extract raw date, time, and department from text."""
    doc = nlp(text)
    date, time, dept = None, None, None

    # --- Extract date using SpaCy NER and regex fallback ---
    for ent in doc.ents:
        if ent.label_ == "DATE":
            date = ent.text
            break
    if not date:
        date_pattern = r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}(st|nd|rd|th)?\s\w+|\w+\s\d{1,2}(st|nd|rd|th)?)"
        match = re.search(date_pattern, text)
        if match:
            date = match.group(0)

    # --- Extract time using SpaCy NER and regex fallback ---
    for ent in doc.ents:
        if ent.label_ == "TIME":
            time = ent.text
            break
    if not time:
        time_pattern = r"(\d{1,2}(:\d{2})?\s?(AM|PM|am|pm))"
        match = re.search(time_pattern, text)
        if match:
            time = match.group(0)

    # --- Extract department ---
    for d in DEPARTMENTS:
        if d.lower() in text.lower():
            dept = d
            break

    return {"date": date, "time": time, "department": dept}

def summarize_text(text: str):
    """Return normalized appointment info from text."""
    print("SUMMARISER STARTED.......")

    raw = extract_appointment(text)
    norm_date, norm_time = normalize_date_time(raw["date"], raw["time"])

    print("SUMMARISER DONE.......")

    return {
        "date": norm_date,
        "time": norm_time,
        "department": raw["department"]
    }

