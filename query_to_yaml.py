import streamlit as st
from chatbot import query_to_yaml

st.title("Générateur YAML avec ChatGPT")

descriptions = st.text_area("Entrez une description de l'infrastructure :")

if st.button("Générer YAML"):
    if descriptions:
        with st.spinner("Génération en cours..."):
            yaml_output = query_to_yaml(descriptions)
        st.code(yaml_output, language="yaml")
    else:
        st.error("Veuillez entrer une description.")
