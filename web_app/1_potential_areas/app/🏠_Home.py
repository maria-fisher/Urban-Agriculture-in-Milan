import streamlit as st

def introduction_page():
    # st.set_page_config(page_title="Home", page_icon=':house:')
    st.title("Identify Areas for Urban Agriculture in Milan")
    st.header("Introduction")
    st.write("""
    This application is designed to help identify suitable areas for urban farming using a machine learning model.
    Urban farming is the practice of cultivating, processing, and distributing food in or around urban areas. It can help
    in improving food security, reducing carbon footprints, and utilizing vacant land efficiently.
    """)

introduction_page()