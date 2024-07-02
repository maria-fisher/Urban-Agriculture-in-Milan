import streamlit as st
import pandas as pd

# Function to display local chapter leads
def display_local_chapter_leads():
    st.write("""
    ## Local Chapter Leads
    """)
    st.markdown("""
    - **Maria Fisher**
    - **Bernardino Sassoli**
    - **Mulugheta Solomon**
    """)

# Function to load references
def load_references():
    return pd.read_csv("dataset/Datasets_references.csv")

# Function to display references
def display_references(df):
    st.subheader("References")
    for _, row in df.iterrows():
        st.write(f"""- [{row['Data source']}]({row['Link']}) - {row['Description']}""")

# Function to load collaborators
def load_collaborators():
    df = pd.read_csv("dataset/Contributors.csv")
    return df

# Function to display collaborators by phase
def display_collaborators_by_phase(df):
    phases = df['Phase'].unique()
    for phase in phases:
        st.header(phase)
        phase_df = df[df['Phase'] == phase]
        contributions = phase_df['Contribution'].unique()
        
        if phase == "Data Collection":
            # Special layout for Data Collection
            # First row with one column
            st.subheader(contributions[0])
            contrib_df = phase_df[phase_df['Contribution'] == contributions[0]]
            for _, row in contrib_df.iterrows():
                st.write(f"**{row['Name']}** - *{row['Position']}*")
            
            # Second row with two columns
            cols = st.columns(2)
            for idx, contribution in enumerate(contributions[1:3]):
                with cols[idx]:
                    st.subheader(contribution)
                    contrib_df = phase_df[phase_df['Contribution'] == contribution]
                    for _, row in contrib_df.iterrows():
                        st.write(f"**{row['Name']}** - *{row['Position']}*")
            
            # Third row with three columns
            cols = st.columns(3)
            for idx, contribution in enumerate(contributions[3:6]):
                with cols[idx]:
                    st.subheader(contribution)
                    contrib_df = phase_df[phase_df['Contribution'] == contribution]
                    for _, row in contrib_df.iterrows():
                        st.write(f"**{row['Name']}** - *{row['Position']}*")
        else:
            # Original layout for other phases
            cols = st.columns(len(contributions))
            for idx, contribution in enumerate(contributions):
                with cols[idx]:
                    st.subheader(contribution)
                    contrib_df = phase_df[phase_df['Contribution'] == contribution]
                    for _, row in contrib_df.iterrows():
                        st.write(f"**{row['Name']}** - *{row['Position']}*")
        
        st.write("")  # Add a blank line between phases

# Function for Contact/Contributors/References/License Page
def contact_page():
    # Custom CSS for title
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playwrite+DE+Grund:wght@100..400&display=swap');
        .custom-title {
            font-family: 'Playwrite DE Grund', sans-serif;
            font-size: 2em;
            color: #556B2F; /* Olive green color */
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<p class="custom-title">Contact and Contributors</p>', unsafe_allow_html=True)

    display_local_chapter_leads()

    collaborators = load_collaborators()
    display_collaborators_by_phase(collaborators)

    references = load_references()
    display_references(references)

    st.subheader("Contact") 
    st.write("""For any inquiries, please contact us at [contact@omdena.com](mailto:contact@omdena.com) """)

if __name__ == "__main__":
    contact_page()
