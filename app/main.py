import streamlit as st

st.set_page_config(
    page_title="F1 Prediction System",
    layout="wide"
)

st.title("F1 Prediction System")

st.write("""
This application demonstrates three machine learning problems:

1. Driver points prediction
2. Position change prediction
3. Next lap time prediction
""")

st.info("Choose a page from the sidebar.")