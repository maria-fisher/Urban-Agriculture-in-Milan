import streamlit as st

def intorduction_page():

    col1, col2, col3, col4 = st.columns([1,1,3,1], gap='medium')
    with col1:
        st.page_link(r"pages/1_home.py", label="Home", icon="🏠")
    with col2:
        st.page_link(r"pages/2_eda.py", label="EDA", icon="📶")
    with col3:
        st.page_link(r"pages/3_prediction.py", label="Find Suitable Area for Uraban Farming", icon="🤖")
    with col4:
        st.page_link(r"pages/4_contact.py", label="Contact Us", icon="📧")

    # st.set_page_config(page_title="Home", page_icon=':house:')
    st.title("Identify Areas for Urban Agriculture in Milan")
    st.header("Introduction")
    st.write("""
    This application is designed to help identify suitable areas for urban farming using a machine learning model.
    Urban farming is the practice of cultivating, processing, and distributing food in or around urban areas. It can help
    in improving food security, reducing carbon footprints, and utilizing vacant land efficiently.
    """)

if __name__ == "__main__":
    intorduction_page()