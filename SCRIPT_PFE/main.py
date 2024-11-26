import streamlit as st
from chatbot import initialize_chat, process_chat
from file_processor import (
    initialize_directories,
    clean_directories,
    extract_zip,
    process_files_with_chatgpt,
    create_result_zip,
)

# Initialiser les répertoires temporaires
initialize_directories()

# Initialiser l'historique des messages
initialize_chat()

# Historique des conversations dans la barre latérale
st.sidebar.header("Historique des conversations")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.sidebar.markdown(f"**Vous** : {message['content']}")
    else:
        st.sidebar.markdown(f"**ChatGPT** : {message['content']}")

# **Section Chatbot**
st.header("Chatbot pour Deploiement SIC")

# Zone d'entrée utilisateur
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Vous :", placeholder="Posez votre question ici...")
    submitted = st.form_submit_button("Envoyer")

# Afficher la réponse en dessous de l'entrée utilisateur
if submitted and user_input:
    # Ajouter l'entrée utilisateur à l'historique et obtenir une réponse
    process_chat(user_input)
    # Obtenir la dernière réponse de l'assistant
    if st.session_state.messages[-1]["role"] == "assistant":
        response = st.session_state.messages[-1]["content"]
        st.write("**Chatbot :")
        st.markdown(response)

# **Section Uploader ZIP**
st.header("Uploader et traiter un fichier ZIP")

uploaded_file = st.file_uploader("Uploader un fichier ZIP", type="zip")

if uploaded_file is not None:
    # Sauvegarder le fichier temporaire
    file_path = f"temp/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    # Décompresser et traiter
    extracted_files = extract_zip(file_path)
    st.success(f"Fichiers extraits : {extracted_files}")

    # Traitement avec ChatGPT
    st.write("Traitement en cours...")
    result_files = process_files_with_chatgpt(extracted_files)
    st.success("Traitement terminé !")

    # Création du ZIP final
    result_zip = create_result_zip(result_files)
    with open(result_zip, "rb") as f:
        st.download_button(
            label="Télécharger le fichier ZIP avec les résultats",
            data=f,
            file_name="results.zip",
            mime="application/zip",
        )

# Nettoyage des fichiers temporaires
if st.button("Nettoyer les fichiers temporaires"):
    clean_directories()
    st.success("Répertoires nettoyés.")
