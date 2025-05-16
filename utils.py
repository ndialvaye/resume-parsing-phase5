import spacy
import pandas as pd
import docx
import io
from PyPDF2 import PdfReader

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_data):
    reader = PdfReader(io.BytesIO(file_data))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file_data):
    doc = docx.Document(io.BytesIO(file_data))
    return "\n".join([para.text for para in doc.paragraphs])

def extract_resume_data(file_data, filename):
    text = ""
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_data)
    elif filename.endswith(".docx"):
        text = extract_text_from_docx(file_data)
    else:
        return {"Filename": filename, "Name": "", "Email": "", "Phone": "", "Skills": ""}

    doc = nlp(text)
    name = ""
    email = ""
    phone = ""
    skills = []

    for ent in doc.ents:
        if ent.label_ == "PERSON" and not name:
            name = ent.text
        elif ent.label_ == "EMAIL" and not email:
            email = ent.text
        elif ent.label_ == "PHONE" and not phone:
            phone = ent.text

    for token in doc:
        if token.pos_ == "NOUN" and token.text.lower() not in skills:
            skills.append(token.text.lower())

    return {
        "Filename": filename,
        "Name": name,
        "Email": email,
        "Phone": phone,
        "Skills": ", ".join(skills)
    }

def save_data_to_excel(data_list, filename):
    df = pd.DataFrame(data_list)
    df.to_excel(filename, index=False)