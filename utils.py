import re
import docx
import spacy
import pandas as pd
from PyPDF2 import PdfReader
from io import BytesIO

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(content):
    reader = PdfReader(BytesIO(content))
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

def extract_text_from_docx(content):
    document = docx.Document(BytesIO(content))
    return "\n".join([para.text for para in document.paragraphs])

def extract_resume_data(filename, content):
    text = ""
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(content)
    elif filename.endswith(".docx"):
        text = extract_text_from_docx(content)

    doc = nlp(text)

    name = ""
    email = ""
    phone = ""
    skills = []
    experiences = []
    education = []

    for ent in doc.ents:
        if ent.label_ == "PERSON" and not name:
            name = ent.text
        elif ent.label_ == "ORG":
            education.append(ent.text)

    email_match = re.search(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', text)
    phone_match = re.search(r'\b(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{4}\b', text)

    if email_match:
        email = email_match.group()
    if phone_match:
        phone = phone_match.group()

    return {
        "Nom": name,
        "Email": email,
        "Téléphone": phone,
        "Éducation": ", ".join(set(education))
    }

def save_data_to_excel(data, path):
    df = pd.DataFrame(data)
    df.to_excel(path, index=False)