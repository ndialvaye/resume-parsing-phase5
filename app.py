import streamlit as st
import pandas as pd
from utils import extract_info_from_text, convert_pdf_or_docx_to_text

st.title("Phase 5: Resume Data Structuring and Analysis")

uploaded_files = st.file_uploader("Upload PDF or DOCX resumes", accept_multiple_files=True, type=["pdf", "docx"])

if uploaded_files:
    all_data = []
    for uploaded_file in uploaded_files:
        text = convert_pdf_or_docx_to_text(uploaded_file)
        data = extract_info_from_text(text)
        all_data.append(data)

    df = pd.DataFrame(all_data)
    st.dataframe(df)

    # Download as CSV
    csv = df.to_csv(index=False)
    st.download_button("Download CSV", csv, "parsed_resumes.csv", "text/csv")