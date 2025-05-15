import sqlite3
import re
import fitz  # PyMuPDF

def parse_pdf_resume(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()

    name = re.findall(r"Name[:\s]*(\w+ \w+)", text)
    email = re.findall(r"[\w.-]+@[\w.-]+", text)
    phone = re.findall(r"\+?\d[\d\s.-]{8,}\d", text)
    skills = re.findall(r"Skills[:\s]*(.*)", text)

    return {
        "name": name[0] if name else "N/A",
        "email": email[0] if email else "N/A",
        "phone": phone[0] if phone else "N/A",
        "skills": skills[0] if skills else "N/A"
    }

def init_db():
    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            skills TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_into_db(data):
    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO resumes (name, email, phone, skills)
        VALUES (?, ?, ?, ?)
    ''', (data["name"], data["email"], data["phone"], data["skills"]))
    conn.commit()
    conn.close()
