import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
            /* Changer la couleur de fond */
            body {
                background-color: #f4f4f4;
            }
            /* Centrer le titre */
            .stTitle {
                text-align: center;
                font-size: 30px;
                color: #333;
                font-weight: bold;
            }
            /* Style des boutons */
            .stButton>button {
                border-radius: 8px;
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 10px;
                border: none;
                transition: 0.3s;
            }
            .stButton>button:hover {
                background-color: #45a049;
            }
            /* Alignement des images */
            .stImage {
                display: block;
                margin-left: auto;
                margin-right: auto;
            }
        </style>
    """, unsafe_allow_html=True)
