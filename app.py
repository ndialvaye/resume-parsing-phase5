import streamlit as st
from utils import parse_pdf_resume, insert_into_db, init_db
import sqlite3
import os
import pandas as pd

st.title("Phase 5 : Base de données structurée à partir de CVs")

st.markdown("Téléversez un fichier PDF de CV pour extraction et insertion en base de données.")

uploaded_file = st.file_uploader("Téléverser un CV (format PDF uniquement)", type=["pdf"])

if uploaded_file is not None:
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("Fichier reçu. Extraction en cours...")

    extracted_data = parse_pdf_resume("temp_resume.pdf")
    st.write("Résultat de l'extraction :", extracted_data)

    init_db()
    insert_into_db(extracted_data)

    st.success("Données insérées dans la base de données.")

    if st.button("Afficher toutes les données enregistrées"):
        conn = sqlite3.connect("resumes.db")
        df = pd.read_sql_query("SELECT * FROM resumes", conn)
        st.dataframe(df)
        conn.close()
