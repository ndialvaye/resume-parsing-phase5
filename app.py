import streamlit as st
from utils import extract_resume_data, save_data_to_excel
import os

st.set_page_config(page_title="Phase 5 - Structuration Base de Données")
st.title("Phase 5 : Création d'une base de données structurée à partir des CVs")

uploaded_files = st.file_uploader("Téléversez un ou plusieurs fichiers PDF ou DOCX", type=["pdf", "docx"], accept_multiple_files=True)

if uploaded_files:
    all_data = []

    for uploaded_file in uploaded_files:
        with st.spinner(f"Traitement du fichier {uploaded_file.name}..."):
            content = uploaded_file.read()
            resume_data = extract_resume_data(uploaded_file.name, content)
            all_data.append(resume_data)

    if all_data:
        output_path = "parsed_resumes.xlsx"
        save_data_to_excel(all_data, output_path)
        st.success("Extraction terminée avec succès.")
        with open(output_path, "rb") as f:
            st.download_button(
                label="📥 Télécharger le fichier Excel structuré",
                data=f,
                file_name="parsed_resumes.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )