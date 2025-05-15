import streamlit as st
import pandas as pd
from utils import parse_pdf, parse_docx, extract_resume_data
from io import BytesIO

st.title("Phase 5 : Génération de base de données structurée à partir des CVs")

uploaded_files = st.file_uploader("Téléversez un ou plusieurs CV (PDF ou DOCX)", type=["pdf", "docx"], accept_multiple_files=True)

if uploaded_files:
    resume_data_list = []
    for file in uploaded_files:
        if file.name.endswith(".pdf"):
            text = parse_pdf(file)
        elif file.name.endswith(".docx"):
            text = parse_docx(file)
        else:
            st.warning(f"Format non pris en charge : {file.name}")
            continue

        data = extract_resume_data(text)
        resume_data_list.append(data)

    if resume_data_list:
        df = pd.DataFrame(resume_data_list)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Résumés')
            writer.save()
        output.seek(0)

        st.success("Extraction terminée. Vous pouvez télécharger le fichier Excel structuré.")
        st.download_button(
            label="📥 Télécharger le fichier .xlsx",
            data=output,
            file_name="parsed_resumes.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )