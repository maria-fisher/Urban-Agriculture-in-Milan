import streamlit as st

# Function for Contact/Contributors/References/License Page
def contact_page():

    st.title("Contact and Contributors")

    st.write("""
    ### Contributors
    - **John Doe** - Data Scientist
    - **Jane Smith** - Environmental Engineer
    - **Alice Johnson** - GIS Specialist

    ### References
    - [Urban Farming Research Paper 1](https://example.com)
    - [Urban Farming Research Paper 2](https://example.com)

    ### License
    This project is licensed under the MIT License. See the [LICENSE](https://example.com) file for details.

    ### Contact
    For any inquiries, please contact us at [email@example.com](mailto:email@example.com).
    """)

if __name__ == "__main__":
    contact_page()