import re
import docx2txt
from PyPDF2 import PdfReader

def convert_pdf_or_docx_to_text(file):
    if file.name.endswith(".pdf"):
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    elif file.name.endswith(".docx"):
        return docx2txt.process(file)
    return ""

def extract_info_from_text(text):
    email = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    phone = re.findall(r'\+?\d[\d\s\-()]{8,}\d', text)
    name = re.findall(r'Name[:\s]+([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)', text)
    skills = re.findall(r'Skills[:\s]+(.+)', text)
    experience = re.findall(r'Experience[:\s]+(.+)', text)
    education = re.findall(r'Education[:\s]+(.+)', text)

    return {
        "name": name[0] if name else "",
        "email": email[0] if email else "",
        "phone": phone[0] if phone else "",
        "skills": skills[0] if skills else "",
        "experience": experience[0] if experience else "",
        "education": education[0] if education else ""
    }