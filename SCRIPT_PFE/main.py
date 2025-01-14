import streamlit as st
from utils.file_processor import (
    initialize_directories,
    clean_directories,
    extract_zip,
    create_result_zip,
)
from utils.playbook_generator import generate_yaml_from_description

# **Initialisation des répertoires temporaires**
initialize_directories()

# **Section : Génération de Playbook YAML**
st.header("Générer un Playbook YAML avec BERT")

# Zone de saisie pour la description utilisateur
description = st.text_area(
    "Entrez une description pour générer un playbook YAML conforme aux normes ISO/IEC :",
    placeholder="Exemple : Déployez 3 PC avec des IP libres, connectez-les à un switch, et configurez un routeur sécurisé.",
)

# Bouton pour générer le playbook YAML
if st.button("Générer le Playbook YAML"):
    if description.strip():
        try:
            # Appel à la fonction pour générer le playbook
            playbook = generate_yaml_from_description(description)

            # Afficher un message de succès
            st.success("Playbook YAML généré avec succès !")

            # Sauvegarder et permettre le téléchargement
            with open("playbook.yaml", "w", encoding="utf-8") as file:
                file.write(playbook)
            with open("playbook.yaml", "rb") as file:
                st.download_button(
                    label="Télécharger le Playbook YAML",
                    data=file,
                    file_name="playbook.yaml",
                    mime="application/x-yaml",
                )
        except Exception as e:
            st.error(f"Une erreur est survenue lors de la génération du Playbook : {e}")
    else:
        st.warning("Veuillez entrer une description valide avant de générer le Playbook YAML.")

# **Section : Traitement de fichiers ZIP**
st.header("Uploader et traiter un fichier ZIP")

uploaded_file = st.file_uploader("Uploader un fichier ZIP contenant des descriptions ou fichiers ", type="zip")

if uploaded_file is not None:
    try:
        # Sauvegarder le fichier temporairement
        file_path = f"temp/{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        # Extraire les fichiers
        extracted_files = extract_zip(file_path)
        st.success(f"Fichiers extraits : {extracted_files}")

        # Traitement des fichiers extraits
        st.write("Traitement des fichiers avec BERT en cours...")
        processed_files = process_files_with_bert(extracted_files)

        # Création d'un ZIP contenant les résultats
        result_zip = create_result_zip(processed_files)
        with open(result_zip, "rb") as f:
            st.download_button(
                label="Télécharger le fichier ZIP avec les résultats",
                data=f,
                file_name="results.zip",
                mime="application/zip",
            )
    except Exception as e:
        st.error(f"Une erreur est survenue lors du traitement des fichiers ZIP : {e}")

# **Nettoyage des fichiers temporaires**
if st.button("Nettoyer les fichiers temporaires"):
    clean_directories()
    st.success("Répertoires nettoyés avec succès.")
