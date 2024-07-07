import os 
import torch
import glob
import numpy as np
import streamlit as st
import numpy as np 
from PIL import Image
from src.constants import STATE_DICT_DIR, GUIDELINES_PATH,  INSIGHTS_PATH
from src.prediction.model_selection import load_model
from src.prediction.prediction_utils import predict_single_image
from src.prediction.pred_configs import get_crop_configs, read_yaml

torch.set_float32_matmul_precision('high')
device = "cuda" if torch.cuda.is_available() else "cpu"
# path to trained model / state_dict#
#STATE_DICT_DIR = "prediction_artifacts/trained_weights"


# Define global CSS styles
st.markdown("""
<style>
.title {
        font-size: 40px;
        background: -webkit-linear-gradient(45deg, #007BFF, #4285F4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        font-family: 'Helvetica', sans-serif;
        margin-bottom: 30px;
        border-bottom: 4px solid #162a3a; /* Secondary background color */
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2); /* Soft text shadow */
    }
    .subheader {
        font-size: 26px;
        color: #95D2B3;
        margin-top: 25px;
        font-weight: bold;
        font-family: 'Helvetica', sans-serif;
        border-bottom: 2px solid #162a3a; /* Secondary background color */
        padding-bottom: 5px;
    }
    h4 {
    font-size: 20px;
    color: #F4A261; /* Dark text color for h4 */
    font-weight: bold;
    font-family: 'Helvetica', sans-serif;
    border-bottom: 2px solid #C80036;
    margin-top: 15px;
    margin-bottom: 10px;
    }              
    .body-text {
        font-size: 18px;
        color: #333333; /* Dark text color for readability */
        font-family: 'Helvetica', sans-serif;
        line-height: 1.6; /* Improved line spacing */
    }
.prediction-green {
    color: #41B06E;
    font-size: 24px;
    font-weight: bold;
    font-family: 'Arial', sans-serif;
}
.prediction-red {
    color: #FF204E;
    font-size: 24px;
    font-weight: bold;
    font-family: 'Arial', sans-serif;
}
.confidence-green {
    color: #41B06E;
    font-size: 24px;
    font-weight: bold;
    font-family: 'Arial', sans-serif;
}
.confidence-yellow {
    color: yellow;
    font-size: 24px;
    font-weight: bold;
    font-family: 'Arial', sans-serif;
}
.confidence-red {
    color: #FF204E;
    font-size: 24px;
    font-weight: bold;
    font-family: 'Arial', sans-serif;
}
</style>
""", unsafe_allow_html=True)




# Function to get list of image files from a directory (case insensitive)
def get_image_options(path):
    image_extensions = ['jpg', 'jpeg', 'png']
    image_files = [f for f in os.listdir(path) if f.split('.')[-1].lower() in image_extensions]
    return image_files

def display_image(image):

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if image is not None:
            st.image(image, caption="Selected Image", use_column_width=True)

def display_prediction(prediction, confidence):
    col1, col2, col3, col4 = st.columns([2, 3,  2, 2])
    with col2:
        st.write("###### **Prediction:**")
        if "healthy" in prediction.lower():
            st.markdown(f"<p class='prediction-green'>{prediction.replace('_', ' ').title()}</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p class='prediction-red'>{prediction.replace('_', ' ').title()}</p>", unsafe_allow_html=True)

    with col3:
        st.write("###### **Confidence:**")
        if confidence > 85:
            st.markdown(f"<p class='confidence-green'>{confidence}%</p>", unsafe_allow_html=True)
        elif 65 <= confidence <= 85:
            st.markdown(f"<p class='confidence-yellow'>{confidence}%</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p class='confidence-red'>{confidence}%</p>", unsafe_allow_html=True)

# Function to display actionable insights on Streamlit
def display_actionable_insights(selected_crop, predicted_disease):
    data = read_yaml(INSIGHTS_PATH)
    predicted_disease = predicted_disease.lower().replace(' ', '_')
    if selected_crop in data and predicted_disease in data[selected_crop]:
        disease_info = data[selected_crop][predicted_disease]
        
        st.markdown('<h4>Actionable Insights</h4>', unsafe_allow_html=True)
        # Display description
        st.write("**Description:**")
        st.write(disease_info.get("description", "No description available."))
        
        # Display control measures
        st.write("\n**Control Measures:**")
        for measure in disease_info.get("control_measures", []):
            st.write(f"- {measure}")
        
        # Display preventive measures
        st.write("\n**Preventive Measures:**")
        for measure in disease_info.get("preventive_measures", []):
            st.write(f"- {measure}")
    else:
        st.warning("No information available for the selected crop and predicted disease.")
def display_guidelines(crop_name):
    crop_name_lower = crop_name.lower().replace(' ', '_')
    crop_guidelines = read_yaml(GUIDELINES_PATH)
    if 'strawberry' in crop_name_lower:
        st.markdown(f'<h4>General guidelines for Growing Strawberry:</h4>', unsafe_allow_html=True)
    else : 
        st.markdown(f'<h4>General guidelines for Growing {crop_name}:</h4>', unsafe_allow_html=True)
    for point in crop_guidelines['crops'][crop_name_lower]:
        st.write(f'- {point}')

def main():
    st.markdown('<p class="title">Diagnostics Application</p>', unsafe_allow_html=True)

    crops_list = os.listdir(STATE_DICT_DIR)
    crop_names = [crop_name.replace('_', ' ').title() for crop_name in crops_list]
    crop_name = st.selectbox("Select Crop for Disease Identification", crop_names, index=0)

    # Process the crop name for convenience.
    crop_name_lower = crop_name.lower().replace(' ', '_')

    # Get configuration for a crop
    config = get_crop_configs(crop_name_lower)
    # Get class names for the crop
    class_map = config['class_map']

    with st.expander("Information about the disease Identification"):
        st.write(f"**This model is trained to predict these diseases in {crop_name} :**")
        # Print class names as bullet points
        for class_id, class_name in class_map.items():
            st.write(f"- **{class_name.replace('_', ' ').title()}**")

    st.markdown('<p class="subheader">Upload Image</p>', unsafe_allow_html=True)
    st.text("ℹ️ Focus on diseased leaves/fruit, keep the area of interest at the center of the image for better results")

    # Create a container for the "Upload Image" section
    with st.container(border=True):
        col1, col2 = st.columns(2)

        # Column 1: File uploader
        with col1:
            uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

        # Column 2: Select image from selectbox and checkbox for camera input
        with col2:
            example_images_path = os.path.join('examples', crop_name_lower)
            image_options = get_image_options(example_images_path)
            if len(image_options) > 0:
                selected_image = st.selectbox("Select an Image", image_options, index=None)
            has_camera = st.checkbox("Use Camera Input")

    # Get the image
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
    elif selected_image is not None:
        image_path = os.path.join(example_images_path, selected_image)
        image = Image.open(image_path)
    elif has_camera and st.camera_input("Take a Picture") is not None:
        image = Image.open(st.camera_input("Take a Picture"))
    else:
        st.write("No image available.")
        return
    # dispaly input image 
    with st.container(border=True):
        display_image(image)
    
    # Define prediction variables globally
    global prediction, prediction_probability
    prediction = None
    prediction_probability = None

    if st.button("Predict"):
        # Construct path to the selected crop's model state_dict
        crop_dir = os.path.join(STATE_DICT_DIR, crop_name_lower)
        file_path = glob.glob(os.path.join(crop_dir, "*.pth"))[0]

        # Load the model with state_dict
        model = load_model(file_path=file_path, config=config)
        model.to(device)

        # Predict disease and prediction probability
        prediction, prediction_probability = predict_single_image(image=image, model=model, config=config, device=device)
        if prediction == 'Unknown':
            st.error(" ⚠️ Unable to identify, Please upload another image ")
            prediction = None

        with st.container(border=True):
            if prediction is not None and prediction_probability is not None:
                display_prediction(prediction, int(prediction_probability * 100))
            else:
                st.write("No prediction available.")

        # Update the prediction variable globally
        prediction = prediction
        prediction_probability = prediction_probability

    if prediction is not None:
        with st.container(border=True):
            display_actionable_insights(selected_crop=crop_name_lower, predicted_disease=prediction)

        with st.container(border=True):
            display_guidelines(crop_name=crop_name)

          
# if __name__ == "__main__":
main()
