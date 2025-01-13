import streamlit as st
from file_processor import (
    initialize_directories,
    clean_directories,
    extract_zip,
    process_files_with_bert,  
    create_result_zip,
)

from generate_playbook_2 import generate_yaml_from_description  
# Initialiser les répertoires temporaires
initialize_directories()

# **Section Génération de playbook YAML**
st.header("Générer un Playbook YAML avec BERT")

# Zone d'entrée pour la description utilisateur
description = st.text_area(
    "Entrez une description pour générer un playbook YAML conforme aux normes ISO/IEC :",
    placeholder="Exemple : Déployez 3 PC avec des IP libres, connectez-les à un switch, et configurez un routeur sécurisé.",
)

# Bouton pour générer le playbook YAML
if st.button("Générer le Playbook YAML"):
    if description.strip():
        try:
            # Appeler la fonction pour générer le fichier YAML
            generate_yaml_from_description(description)
            st.success("Playbook YAML généré avec succès !")

            # Permettre le téléchargement du fichier généré
            with open("playbook.yaml", "rb") as f:
                st.download_button(
                    label="Télécharger le Playbook YAML",
                    data=f,
                    file_name="playbook.yaml",
                    mime="application/x-yaml",
                )
        except Exception as e:
            st.error(f"Une erreur est survenue : {e}")
    else:
        st.warning("Veuillez entrer une description avant de générer le Playbook YAML.")

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

    # Traitement avec BERT (remplacez `process_files_with_chatgpt` si nécessaire)
    st.write("Traitement en cours...")
    result_files = process_files_with_chatgpt(extracted_files)  

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
