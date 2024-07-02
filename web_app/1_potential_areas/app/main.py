import streamlit as st
from streamlit_option_menu import option_menu
import base64
import A_home as A_home
from B_eda import eda_page as eda
from C_agricultural_suitability import app as suitability
from D_contact import contact_page as Contacts
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

# Set page configuration
st.set_page_config(
    page_title="Agriculture Suitability Analysis",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="expanded"
)

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background_and_text_color(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background-image: url("data:image/png;base64,%s");
        background-size: 100vw 100vh;
        background-position: center;
        background-repeat: no-repeat;
    }
    .stApp, p, h1, h2, h3, h4, h5, h6 {
        color: #404040;
    }
    [data-testid="stSidebar"] {
        background-color: #254117;
    }
    .stApp > header {
        background-color: transparent; /* Make header background transparent */
        box-shadow: none; /* Remove box-shadow */
    }
    .stButton > button {
        background-color: #FFBD59 !important;
        color: #404040 !important;
        border: 1px solid rgba(0,0,0,0.2);
    }
    .stSlider > div > div > div > div {
        background-color: rgb(100,152,71) !important;
    }
    .stSlider > div > div > div > div > div {
        color: black !important;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Example usage with your background image
set_background_and_text_color('Images/bg_img1.png')

# Load the logo
st.image('Images/omdenalogo.png', width=130)  # Adjust width as per your logo size

# Sidebar navigation
with st.sidebar:
    sidebar_selected1 = option_menu(
        menu_title='Navigation',
        options=['Home','Check Suitable Areas', 'EDA Dashboard', 'Contacts'],
        icons=['house-fill', 'rocket-fill', 'bar-chart-fill', 'phone-fill'],
        menu_icon='book-fill',
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": '#FFBD59'},
            "icon": {"color": "#001f54", "font-size": "20px"},
            "nav-link": {"color":"#001f54", "font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#71A75E"},
            "nav-link-selected": {"background-color": "#71A75E"},
            "menu-title": {"color": "#540b0e"},
            "menu-icon": {"color": "#540b0e"}
        }
    )

# Function to load the selected page
def load_page(page):
    if page == "Home":
        A_home.app()
    elif page == "Check Suitable Areas":
        suitability()
    elif page == "EDA Dashboard":
        eda()
    elif page == "Contacts":
        Contacts()

if __name__ == "__main__":
    load_page(sidebar_selected1)
