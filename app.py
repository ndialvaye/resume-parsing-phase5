import streamlit as st
from utils import extract_resume_data, save_data_to_excel
import os

st.title("Phase 5 : Structuration et Analyse des CVs")

uploaded_files = st.file_uploader("Uploader les CVs (PDF ou DOCX)", type=["pdf", "docx"], accept_multiple_files=True)

if uploaded_files:
    resume_data = []
    for file in uploaded_files:
        text = extract_resume_data(file)
        resume_data.append(text)
    
    xls_file = save_data_to_excel(resume_data)
    st.success("Données extraites avec succès !")
    with open(xls_file, "rb") as f:
        st.download_button("Télécharger les données (XLS)", f, file_name="parsed_resumes.xls")