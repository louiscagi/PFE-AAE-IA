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
from mistral_bot import query_mistral, explain_playbook_mistral

# Initialiser l'historique des messages
initialize_chat()

# Page de connexion
def login_page():
    st.title("🔐 Connexion")
    email = st.text_input("📧 Email")
    password = st.text_input("🔑 Mot de passe", type="password")
    if st.button("Se connecter"):
        user = authenticate_user(email, password)
        if user:
            st.success("✅ Connexion réussie !")
            st.session_state["user"] = user
        else:
            st.error("❌ Identifiants incorrects.")

if "user" not in st.session_state:
    login_page()
else:
    # Interface principale
    st.title("🤖 Chatbot Ansible - OpenAI & Mistral")

    # Sélection du modèle avec logos
    st.markdown("### 🌟 Choisissez le modèle d'IA :")

    col1, col2 = st.columns(2)

    # Chemins des images (Assurez-vous qu'elles existent dans "assets/")
    openai_logo = "assets/openai_logo.png"
    mistral_logo = "assets/mistral_logo.png"

    with col1:
        st.image(openai_logo, width=150)
        if st.button("Utiliser OpenAI (GPT-4)"):
            st.session_state["model_choice"] = "OpenAI (GPT-4)"

    with col2:
        st.image(mistral_logo, width=150)
        if st.button("Utiliser Mistral"):
            st.session_state["model_choice"] = "Mistral"

    # Vérification du modèle sélectionné
    if "model_choice" not in st.session_state:
        st.warning("⚠️ Veuillez sélectionner un modèle.")
        st.stop()

    model_choice = st.session_state["model_choice"]
    st.success(f"✅ Modèle sélectionné : {model_choice}")

    # Onglets
    tab1, tab2 = st.tabs(["📜 Générer un Playbook", "🔍 Analyser un Playbook"])

    with tab1:
        st.markdown("### 📝 Posez votre question ou décrivez votre besoin")
        user_input = st.text_area("Votre demande", placeholder="Décrivez vos besoins ici...")

        if st.button("🚀 Générer Playbook"):
            if not user_input.strip():
                st.error("⚠️ Veuillez entrer une description.")
            else:
                if model_choice == "OpenAI (GPT-4)":
                    yaml_content, response = query_with_yaml_and_description(user_input)
                else:
                    yaml_content, response = query_mistral(user_input)

                if response:
                    st.markdown(f"**💬 Assistant :** {response}")
                    if yaml_content and validate_yaml(yaml_content):
                        download_button(yaml_content, "playbook.yaml", key="download_button")
                else:
                    st.error("❌ Une erreur est survenue.")

    with tab2:
        st.markdown("### 📂 Déposez un fichier playbook.yaml à analyser")
        uploaded_file = st.file_uploader("📤 Uploader un fichier YAML", type=["yaml", "yml"])

        if uploaded_file is not None:
            try:
                yaml_content = uploaded_file.read().decode("utf-8")
                st.code(yaml_content, language="yaml")

                if model_choice == "OpenAI (GPT-4)":
                    explanation = explain_playbook(yaml_content)
                else:
                    explanation = explain_playbook_mistral(yaml_content)

                if explanation:
                    st.markdown("#### 🧐 Explication du Playbook")
                    st.write(explanation)
            except Exception as e:
                st.error(f"❌ Erreur lors du traitement du fichier : {e}")
