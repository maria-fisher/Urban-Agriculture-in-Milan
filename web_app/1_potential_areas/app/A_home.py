import os
import streamlit as st
import base64

def app():
    # Set custom font for the title
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playwrite+US+Modern:wght@100..400&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Playwrite+DE+Grund:wght@100..400&display=swap');

        .custom-title {
            font-family: 'Playwrite US Modern', sans-serif;
            font-size: 2.5em;
            color: #556B2F; /* Change the color to your preference */
            font-weight: bold;
        }
        .custom-subheader {
            font-family: 'Playwrite DE Grund', sans-serif;
            font-size: 1.4em;
            color: #4CAF50; /* Change the color to your preference */
        }

        .custom-text {
            font-family: 'Playwrite DE Grund', sans-serif;
            font-size: 1.1em;
            color: #8B4513; /* Change the color to #8B4513 */
            text-align: justify;
        }

        .custom-text p {
            font-family: 'Playwrite DE Grund', sans-serif;
            font-size: 1em;
            color: #8B4513; /* Change the color to #8B4513 */
            text-align: justify;
        }

        .custom-text h3 {
            font-family: 'Playwrite DE Grund', sans-serif;
            font-size: 1.2em;
            color: #556B2F; /* Change the color to #8B4513 */
            text-align: justify;
        }

        .feature-list {
            font-family: 'Playwrite DE Grund', sans-serif;
            font-size: 1.1em;
            color: #8B4513; /* Change the color to #8B4513 */
        }
        .feature-list h3 {
            color: #800000; /* Change the color of h3 to #800000 */
            font-size: 1.3em;
        }
        .feature-list li {
            margin-bottom: 10px;
        }
        .image-caption {
            font-family: 'Playwrite US Modern', sans-serif;
            font-size: 0.7em;
            color: #E2A76F; /* Change the color to orange */
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<p class="custom-title">Agriculture Suitability Analysis</p>', unsafe_allow_html=True)
    st.markdown('<p class="custom-subheader">Welcome to the Agriculture Suitability Analysis Tool</p>', unsafe_allow_html=True)

    # Ensure the correct path to the image
    image_path = os.path.join(os.path.dirname(__file__), 'Images', 'home_page_gif.gif')
    
    # Add your GIF here with custom caption color
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/gif;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" alt="Agriculture Suitability Analysis" style="width: 100%;">
            <p class="image-caption">Sowing Seeds of Sustainability 🌱</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="custom-text">
        This application helps you analyze and visualize the suitability of different areas for agriculture using latitude and longitude inputs. Our powerful machine learning model predicts the agricultural suitability based on various factors.<br>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="custom-text">
    <h3>Introduction</h3>
        <p>Urban farming plays a crucial role in the fight against climate change by supporting sustainable food production within cities. As urbanization continues to expand, integrating agriculture into urban areas not only strengthens local food security but also reduces transportation emissions and the carbon footprint associated with conventional farming practices.</p>
        <p>Additionally, urban farming contributes to the creation of green spaces, helps mitigate the urban heat island effect, and improves air quality. By connecting communities with locally grown food, it encourages environmental responsibility and raises awareness about the impact of traditional agriculture on climate change. Embracing urban farming is essential for the development of environmentally friendly and resilient cities, while also fostering a sustainable future in the face of global climate challenges.</p>
        <p>Innovative approaches in urban farming utilize space efficiently, often repurposing unused or underutilized urban areas to grow fresh produce. By doing so, urban farming not only enhances food security but also contributes to the aesthetic and environmental quality of urban landscapes.<p>
        <p>Furthermore, urban farming provides significant social benefits. It can create job opportunities, offer educational experiences, and strengthen community bonds by bringing people together around the common goal of cultivating and enjoying fresh, healthy food. Educational programs in urban farming can teach valuable skills in agriculture, sustainability, and nutrition, empowering individuals and communities to make informed choices about their food and its sources.<p>
        <p>Urban farming also plays a vital role in biodiversity conservation. By incorporating a variety of plant species and fostering habitats for pollinators like bees and butterflies, urban farms can help maintain and even enhance local biodiversity. This biodiversity is crucial for resilient ecosystems that can adapt to changing environmental conditions.<p>
        <p>Moreover, urban farming supports mental and physical health. Engaging in gardening activities has been shown to reduce stress, improve mood, and promote physical activity. Access to green spaces and fresh produce contributes to overall well-being, making urban farming a powerful tool for improving public health.<p>
        <p>In summary, urban farming is more than just growing food within city limits; it is a multifaceted approach to creating sustainable, resilient, and vibrant urban environments. By integrating agriculture into urban settings, we can address numerous challenges related to food security, climate change, community well-being, and environmental sustainability. Embracing urban farming is a step towards a greener, healthier, and more sustainable future for our cities and the planet.<p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="custom-text">
        <h3>Project Overview</h3>
        <p>This project was created under <b>Omdena, Milan, Italy Chapter</b>, with the goal of utilizing advanced machine learning techniques to predict suitable areas for urban farming. The project's objectives align with the broader mission of promoting sustainability and combating climate change through innovative urban agricultural practices.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="custom-text">
        <h3>Models Used</h3>
        <p>Two machine learning models have been employed in this project: XGBoostClassifier and KMeansClassifier. The <b>XGBoostClassifier</b> is used for supervised learning, leveraging a wide range of input features to make accurate predictions about the suitability of different areas for urban farming. The <b>KMeansClassifier</b>, on the other hand, is used for unsupervised learning, clustering locations based on their characteristics to identify suitable areas without requiring labeled training data.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="custom-text">
        <h3>Features:</h3>
        <ul class="feature-list">
            <li><b>Exploratory Data Analysis (EDA)</b>: Understand the data through visualizations.</li>
            <li><b>Agricultural Suitability Prediction</b>: Input latitude and longitude to check the suitability of the area for agriculture.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    app()

