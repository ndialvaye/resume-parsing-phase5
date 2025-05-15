import fitz  # PyMuPDF
import docx2txt
import re

def parse_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def parse_docx(file):
    return docx2txt.process(file)

def extract_resume_data(text):
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)
    education = extract_education(text)
    experience = extract_experience(text)
    return {
        "Name": name,
        "Email": email,
        "Phone": phone,
        "Skills": skills,
        "Education": education,
        "Experience": experience
    }

def extract_name(text):
    lines = text.strip().split('
')
    return lines[0] if lines else ""

def extract_email(text):
    match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    return match.group(0) if match else ""

def extract_phone(text):
    match = re.search(r"(\+?\d{1,3})?[\s.-]?(\d{2}[\s.-]?){4,5}", text)
    return match.group(0) if match else ""

def extract_skills(text):
    keywords = ["Python", "SQL", "Excel", "Data", "Machine Learning", "Communication"]
    found = [kw for kw in keywords if kw.lower() in text.lower()]
    return ", ".join(found)

def extract_education(text):
    education_keywords = ["Bac", "Licence", "Master", "Doctorat", "École", "Université"]
    found = [line for line in text.split('\n') if any(word in line for word in education_keywords)]
    return "; ".join(found)

def extract_experience(text):
    experience_keywords = ["stage", "expérience", "travail", "CDD", "CDI", "freelance"]
    found = [line for line in text.split('\n') if any(word in line.lower() for word in experience_keywords)]
    return "; ".join(found)