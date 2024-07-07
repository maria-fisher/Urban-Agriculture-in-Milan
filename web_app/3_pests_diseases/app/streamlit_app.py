import streamlit as st


st.set_page_config(page_title="Crop Disease Diagnostics", 
                   page_icon=":material/potted_plant:", 
                   layout="wide",
                   initial_sidebar_state="expanded",)



about_page = st.Page("about.py", title="About", icon=":material/info:")
app_page = st.Page("application.py", title="Application", icon=":material/image_search:")

pg = st.navigation([about_page, app_page])

pg.run()
