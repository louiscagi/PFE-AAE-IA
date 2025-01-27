import streamlit as st
from chatbot import (
    initialize_chat,
    query_with_yaml_and_description,
    validate_yaml,
    download_button,
    add_message,
    explain_playbook,
    authenticate_user
)

# Initialiser l'historique des messages
initialize_chat()

# Page de connexion
def login_page():
    st.title("Connexion")
    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        user = authenticate_user(email, password)
        if user:
            st.success("Connexion réussie !")
            st.session_state["user"] = user
        else:
            st.error("Identifiants incorrects.")

if "user" not in st.session_state:
    login_page()
else:
    # Titre de l'application
    st.title("Chatbot Ansible - YAML et Explications")

    # Onglets pour basculer entre génération et analyse
    tab1, tab2 = st.tabs(["Générer un Playbook", "Analyser un Playbook"])

    with tab1:
        st.markdown("### Posez votre question ou décrivez votre besoin")
        user_input = st.text_area("Votre demande", placeholder="Décrivez vos besoins ici.")

        if st.button("Générer Playbook", key="generate_button"):
            if not user_input.strip():
                st.error("Veuillez entrer une description avant de générer.")
            else:
                yaml_content, response = query_with_yaml_and_description(user_input)

                if response:
                    st.markdown(f"**Assistant :** {response}")
                    if yaml_content and validate_yaml(yaml_content):
                        download_button(yaml_content, "playbook.yaml", key="download_button")
                else:
                    st.error("Une erreur est survenue lors de la génération du playbook.")

    with tab2:
        st.markdown("### Déposez un fichier playbook.yaml à analyser")
        uploaded_file = st.file_uploader("Uploader un fichier YAML", type=["yaml", "yml"])

        if uploaded_file is not None:
            try:
                yaml_content = uploaded_file.read().decode("utf-8")
                st.markdown("#### Contenu du Playbook")
                st.code(yaml_content, language="yaml")

                explanation = explain_playbook(yaml_content)
                if explanation:
                    st.markdown("#### Explication du Playbook")
                    st.write(explanation)
            except Exception as e:
                st.error(f"Erreur lors du traitement du fichier : {e}")
