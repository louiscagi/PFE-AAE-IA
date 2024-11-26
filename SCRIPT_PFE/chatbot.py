import openai
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate

# Initialisation de l'API OpenAI
api_key = st.secrets["OPENAI_API_KEY"]  # Bonne pratique : utiliser Streamlit Secrets
openai.api_key = api_key

def initialize_chat():
    """Initialise l'historique des messages dans la session Streamlit."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

def process_chat(user_input):
    """
    Envoie le message utilisateur à ChatGPT 3.5 Turbo et retourne la réponse.
    """
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
        )
        # Ajouter la réponse au contexte
        st.session_state.messages.append(
            {"role": "assistant", "content": response.choices[0].message["content"]}
        )
    except Exception as e:
        st.error(f"Erreur lors de la communication avec ChatGPT : {e}")

def display_chat_history():
    """Affiche l'historique des messages dans la barre latérale."""
    st.sidebar.header("Historique des conversations")
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.sidebar.markdown(f"**Vous** : {message['content']}")
        else:
            st.sidebar.markdown(f"**ChatGPT** : {message['content']}")

def query_to_yaml(descriptions):
    """
    Génère un fichier YAML basé sur une description en langage naturel.
    Utilise LangChain pour structurer les messages avec OpenAI.
    """
    # Création du modèle OpenAI avec LangChain
    model = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.9,
        max_tokens=2000
    )

    # Création des messages du chat
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "Vous êtes une intelligence artificielle spécialisée dans la génération de fichiers YAML pour l'infrastructure. d'apres le prompt"+
         " donné tu dois faire le fichier playbook.yaml"),
        ("human", "Créez un ou plusieurs codes YAML au style Terraform pour configurer un réseau d'infrastructure incluant:\n{descriptions}")
    ])

    # Génération du prompt à partir des messages avec la description comme paramètre
    prompt_messages = chat_prompt.format_prompt(descriptions=descriptions).to_messages()

    # Appel de l'API OpenAI via le modèle
    ai_response = model.invoke(prompt_messages)
    return ai_response.content
