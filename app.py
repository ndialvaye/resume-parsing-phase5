import streamlit as st
from utils import extract_resume_data, save_data_to_excel

st.title("Phase 5: Structured Resume Data to Excel")

uploaded_files = st.file_uploader("Upload resumes (PDF or DOCX)", accept_multiple_files=True, type=['pdf', 'docx'])

if uploaded_files:
    all_data = []
    for uploaded_file in uploaded_files:
        file_data = uploaded_file.read()
        filename = uploaded_file.name
        st.success(f"Parsing: {filename}")
        resume_data = extract_resume_data(file_data, filename)
        all_data.append(resume_data)

    if all_data:
        save_data_to_excel(all_data, "parsed_resumes.xlsx")
        with open("parsed_resumes.xlsx", "rb") as f:
            st.download_button("Download Structured Excel", f, file_name="parsed_resumes.xlsx")