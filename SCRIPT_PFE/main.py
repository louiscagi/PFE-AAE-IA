import streamlit as st
from chatbot import initialize_chat, query_to_yaml, validate_yaml, download_button

# Initialiser l'historique des messages
initialize_chat()

# Titre de l'application
st.title("Générateur de Playbook Ansible")
st.subheader("Entrez une description pour générer un playbook YAML adapté")

# Zone de saisie pour la description
description = st.text_area(
    "Description",
    placeholder="Exemple : Configurer un serveur avec SSH, activer le pare-feu, configurer un VLAN, etc."
)

# Bouton pour générer le YAML
if st.button("Générer"):
    if not description.strip():
        st.error("Veuillez fournir une description valide avant de générer le playbook.")
    else:
        # Appeler la fonction pour générer le YAML
        yaml_content = query_to_yaml(description)

        if yaml_content:
            # Valider et afficher le YAML
            if validate_yaml(yaml_content):
                st.success("Playbook YAML généré avec succès !")
                st.code(yaml_content, language="yaml")

                # Ajouter un bouton de téléchargement
                download_button(yaml_content, "playbook.yaml")
            else:
                st.error("Le YAML généré contient des erreurs.")
        else:
            st.error("Aucun contenu YAML n'a été généré. Veuillez réessayer.")

# Section pour réinitialiser l'historique
st.header("Réinitialisation")
if st.button("Réinitialiser l'historique"):
    st.session_state.messages = []
    st.success("Historique des messages réinitialisé.")
