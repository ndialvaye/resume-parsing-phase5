import spacy
import subprocess
import sys
import pandas as pd
import re
from io import BytesIO
import docx2txt
from PyPDF2 import PdfReader

# Charger SpaCy avec gestion de l'absence de modèle
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

def extract_text_from_file(file):
    if file.name.endswith(".pdf"):
        reader = PdfReader(file)
        text = "".join([page.extract_text() or "" for page in reader.pages])
    elif file.name.endswith(".docx"):
        text = docx2txt.process(file)
    else:
        text = ""
    return text

def extract_resume_data(file):
    text = extract_text_from_file(file)
    doc = nlp(text)
    name = email = phone = ""
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not name:
            name = ent.text
        if ent.label_ == "EMAIL" or re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", ent.text):
            email = ent.text
        if not phone and re.search(r"(\+?\d{1,3})?[\s.-]?\(?\d{2,4}\)?[\s.-]?\d{3,4}[\s.-]?\d{3,4}", ent.text):
            phone = ent.text
    return {"Nom": name, "Email": email, "Téléphone": phone}

def save_data_to_excel(data):
    df = pd.DataFrame(data)
    output_path = "parsed_resumes.xls"
    df.to_excel(output_path, index=False)
    return output_path