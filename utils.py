import re
import docx2txt
import fitz  # PyMuPDF

def parse_pdf(file) -> str:
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def parse_docx(file) -> str:
    return docx2txt.process(file)

def extract_resume_data(text: str) -> dict:
    data = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "experience": extract_experience(text),
        "education": extract_education(text),
    }
    return data

def extract_email(text: str) -> str:
    match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    return match.group(0) if match else ""

def extract_phone(text: str) -> str:
    match = re.search(r"\+?\d[\d\s().-]{8,}\d", text)
    return match.group(0) if match else ""

def extract_name(text: str) -> str:
    lines = text.split("\n")
    for line in lines[:5]:
        if len(line.strip().split()) in [2, 3] and line[0].isupper():
            return line.strip()
    return ""

def extract_skills(text: str) -> str:
    skills_keywords = ["Python", "SQL", "Excel", "Java", "C++", "Machine Learning", "Data Analysis"]
    found = [skill for skill in skills_keywords if re.search(rf"\b{skill}\b", text, re.IGNORECASE)]
    return ", ".join(found)

def extract_experience(text: str) -> str:
    experience_section = re.search(r"(?i)(experience|expériences).+?(education|formation|skills|compétences)", text, re.DOTALL)
    return experience_section.group(0).strip() if experience_section else ""

def extract_education(text: str) -> str:
    education_section = re.search(r"(?i)(education|formation).+?(experience|expérience|skills|compétences)", text, re.DOTALL)
    return education_section.group(0).strip() if education_section else ""