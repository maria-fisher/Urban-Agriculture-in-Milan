import streamlit as st
from C1_predict import run_app as predict_using_all
from C2_predict import app as predict_using_latlong

def apply_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playwrite+DE+Grund:wght@100..400&display=swap');
        
        .custom-title {
            font-family: 'Playwrite DE Grund', sans-serif;
            font-size: 2.2em;
            color: #665D1E; /* Change to the desired color */
            font-weight: bold;
        }
        .custom-text {
            # font-family: 'Playwrite DE Grund', sans-serif;
            font-size: 1.8em;
            font-weight: 400;
            color: #622F22; /* Change to the desired color */
        }

        .custom-text p{
            font-family: "Playwrite DE Grund", sans-serif;
            font-size: 0.5em;
            color: #622F22; /* Change the color to #8B4513 */
            text-align: justify;
        }

        .custom-text h3{
            font-family: 'Playwrite DE Grund', sans-serif;
            font-size: 0.8em;
            font-weight: 400;
            color: #4CAF50; /* Change to the desired color */
        }

        </style>
        """,
        unsafe_allow_html=True
    )

def show_main_page():
    apply_custom_css()
    st.markdown('<p class="custom-title">Agriculture Suitability Prediction</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="custom-text">
    <h3>Predict using all the parameters</h3>
    <p>This feature can be used to predict the agricultural suitability of any location. By utilizing a comprehensive set of input data, including social, climatic, and infrastructural factors, the models provide accurate predictions to support urban farming initiatives in diverse regions. This capability allows for the assessment and optimization of urban agriculture globally, contributing to sustainable development and food security.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Predict using All the Values"):
        st.session_state.page = "supervised"
        st.experimental_rerun()
    
    st.markdown("""
    <div class="custom-text">
    <h3>Predict using only the Latitude and Longitude</h3>
    <p>Currently, this feature is limited to Zone 4 and Zone 9 of Milan, Italy, providing focused analysis and predictions tailored to these specific geographical areas.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Predict using only Latitude and Longitude"):
        st.session_state.page = "unsupervised"
        st.experimental_rerun()

def app():
    apply_custom_css()
    if 'page' not in st.session_state:
        st.session_state.page = "main"

    if st.session_state.page == "supervised":
        predict_using_all()
    elif st.session_state.page == "unsupervised":
        predict_using_latlong()
    else:
        show_main_page()

if __name__ == "__main__":
    app()

def predict_using_all():
    import  C1_predict as C1_predict
    C1_predict.run_app()

def predict_using_latlong():
    import C2_predict as C2_predict
    C2_predict.app()

def app():
    apply_custom_css()
    if 'page' not in st.session_state:
        st.session_state.page = "main"

    if st.session_state.page == "supervised":
        predict_using_all()
    elif st.session_state.page == "unsupervised":
        predict_using_latlong()
    else:
        show_main_page()

if __name__ == "__main__":
    app()
