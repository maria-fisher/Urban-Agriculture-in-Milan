import base64
import streamlit as st
from pathlib import Path

root_path = Path(__file__).parent.parent
media_path = root_path.joinpath("media")

# Function to add a background image from a file
def set_custom_bg(image_file=str(media_path.joinpath("bg_17.jpeg"))):
    with open(image_file, "rb") as image:
        encoded_image = base64.b64encode(image.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded_image}");
            background-size: cover;
        }}
        .stApp > header {{
        background-color: transparent; /* Make header background transparent */
        box-shadow: none; /* Remove box-shadow */
        }}
        .css-18e3th9 {{
            background-color: rgba(240, 240, 240, 0.8);
        }}
        .css-1d391kg {{
            background-color: rgba(240, 240, 240, 0.8);
        }}
        .stButton>button {{
            color: white;
            background-color: #4CAF50;
        }}
        .st-c5 {{
            padding-top: 0rem;
            padding-right: 2rem;
            padding-bottom: 2rem;
            padding-left: 2rem;
        }}
        .nav {{
            background-color: #fdf2df;
            padding: 10px;
            font-size: 18px;
        }}
        .big-font {{
            font-size: 24px !important;
        }},
        </style>
        """,
        unsafe_allow_html=True
    )

# Customizing the navigation bar
def custom_navbar():
    st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #fdf2df;
    </style>
    """,
    unsafe_allow_html=True,
    )


if __name__ == "__main__":
    # Add the background image
    set_custom_bg(str(media_path.joinpath('bg_16.png')))