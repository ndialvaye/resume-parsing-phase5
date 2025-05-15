import streamlit as st
import pandas as pd
from utils import extract_resume_data, parse_pdf, parse_docx
from pathlib import Path

st.title("Phase 5 - Structuration et Analyse des CVs")

uploaded_files = st.file_uploader("Téléverser des fichiers .pdf ou .docx", type=["pdf", "docx"], accept_multiple_files=True)

if uploaded_files:
    all_data = []
    for file in uploaded_files:
        file_extension = Path(file.name).suffix.lower()
        if file_extension == ".pdf":
            text = parse_pdf(file)
        elif file_extension == ".docx":
            text = parse_docx(file)
        else:
            st.warning(f"Format non supporté : {file.name}")
            continue

        data = extract_resume_data(text)
        data["filename"] = file.name
        all_data.append(data)

    df = pd.DataFrame(all_data)
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Télécharger les données en CSV", data=csv, file_name="parsed_resumes.csv", mime="text/csv")