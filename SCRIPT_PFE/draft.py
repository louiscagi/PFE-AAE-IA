import streamlit as st
import zipfile
import os
from mistralai import Mistral
import shutil
from io import BytesIO

# Configuration du client Mistral
api_key = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=api_key)

# Répertoires temporaires
TEMP_DIR = "temp_dir"
RESULTS_DIR = "results_dir"
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# Titre de l'application
st.title("Chatbot et Traitement ZIP avec Mistral AI")

# Historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# **Section : Sidebar pour l'historique des conversations**
with st.sidebar:
    st.header("Historique des conversations")
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"**Vous** : {message['content']}")
        else:
            st.markdown(f"**Chatbot** : {message['content']}")

# **Section 1 : Chatbot**
st.header("Chatbot avec Mistral AI")

# Formulaire d'entrée utilisateur
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Vous :", placeholder="Posez votre question ici...")
    submitted = st.form_submit_button("Envoyer")

# Gérer la soumission au chatbot
if submitted and user_input:
    # Ajouter l'entrée utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Appeler le modèle Mistral
    with st.spinner("Le chatbot réfléchit..."):
        try:
            response = client.chat.complete(
                model="mistral-large-latest",
                messages=st.session_state.messages,
            )
            # Ajouter la réponse du chatbot à l'historique
            st.session_state.messages.append(
                {"role": "assistant", "content": response.choices[0].message.content}
            )
        except Exception as e:
            st.error(f"Une erreur s'est produite : {e}")

# **Section 2 : Gestion des fichiers ZIP**
st.header("Uploader et traiter un fichier ZIP")

# Upload du fichier ZIP
uploaded_file = st.file_uploader("Uploader un fichier ZIP", type="zip")

if uploaded_file is not None:
    # Sauvegarder temporairement le fichier ZIP
    with open(os.path.join(TEMP_DIR, "uploaded.zip"), "wb") as f:
        f.write(uploaded_file.read())

    # Décompresser le fichier ZIP
    with zipfile.ZipFile(os.path.join(TEMP_DIR, "uploaded.zip"), "r") as zip_ref:
        zip_ref.extractall(TEMP_DIR)

    st.success("Fichiers décompressés avec succès !")
    st.write("Voici les fichiers extraits :")
    extracted_files = os.listdir(TEMP_DIR)
    st.write(extracted_files)

    # Traitement avec le modèle Mistral
    st.write("Traitement des fichiers avec Mistral AI...")
    mistral_results = []
    for file_name in extracted_files:
        file_path = os.path.join(TEMP_DIR, file_name)
        if os.path.isfile(file_path):
            with open(file_path, "r") as file_content:
                try:
                    # Envoi du contenu au modèle
                    response = client.chat.complete(
                        model="mistral-large-latest",
                        messages=[{"role": "user", "content": file_content.read()}],
                    )
                    # Sauvegarder le résultat dans le répertoire de résultats
                    result_file_path = os.path.join(
                        RESULTS_DIR, f"result_{file_name}"
                    )
                    with open(result_file_path, "w") as result_file:
                        result_file.write(response.choices[0].message.content)
                    mistral_results.append(result_file_path)
                except Exception as e:
                    st.error(f"Erreur lors du traitement de {file_name} : {e}")

    st.success("Traitement terminé !")

    # Création d'un ZIP avec les fichiers résultats
    result_zip_path = os.path.join(TEMP_DIR, "results.zip")
    with zipfile.ZipFile(result_zip_path, "w") as result_zip:
        for result_file in mistral_results:
            result_zip.write(result_file, os.path.basename(result_file))

    # Téléchargement du ZIP
    with open(result_zip_path, "rb") as f:
        st.download_button(
            label="Télécharger le fichier ZIP avec les résultats",
            data=f,
            file_name="results.zip",
            mime="application/zip",
        )

# Nettoyage des répertoires temporaires
if st.button("Nettoyer les fichiers temporaires"):
    shutil.rmtree(TEMP_DIR)
    shutil.rmtree(RESULTS_DIR)
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    st.success("Répertoires temporaires nettoyés.")
