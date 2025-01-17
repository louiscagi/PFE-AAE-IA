import streamlit as st
from chatbot import initialize_chat, query_to_yaml, validate_yaml, download_button

# Initialiser l'historique des messages
initialize_chat()

# Titre de l'application
st.title("Générateur de Playbook Ansible en YAML")
st.subheader("Entrez une description et générez un fichier YAML adapté")

# Zone de saisie pour la description
description = st.text_area(
    "Description",
    placeholder="Exemple : Configurer un serveur avec SSH, activer le pare-feu, etc."
)

# Bouton pour générer le YAML
if st.button("Générer"):
    if description:
        # Appeler la fonction pour générer le YAML
        yaml_content = query_to_yaml(description)

        # Valider et afficher le YAML
        if validate_yaml(yaml_content):
            st.success("Playbook YAML généré avec succès !")
            st.code(yaml_content, language="yaml")

            # Ajouter le bouton de téléchargement
            download_button(yaml_content, "playbook.yaml")
        else:
            st.error("Le YAML généré contient des erreurs.")
    else:
        st.warning("Veuillez entrer une description avant de générer.")

# Section pour réinitialiser l'historique
st.header("Réinitialisation")
if st.button("Réinitialiser l'historique"):
    st.session_state.messages = []
    st.success("Historique des messages réinitialisé.")
