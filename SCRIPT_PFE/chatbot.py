import openai
import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
import yaml

# Initialisation de l'API OpenAI
api_key = st.secrets["OPENAI_API_KEY"]
openai.api_key = api_key

def initialize_chat():
    """Initialise l'historique des messages dans la session Streamlit."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

def query_to_yaml(description):
    """
    Génére un fichier YAML basé sur une description en langage naturel.
    """
    # Création du modèle OpenAI avec LangChain
    model = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=3000
    )

    # Prompt structuré pour guider l'API
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", """
        Vous êtes un assistant spécialisé dans la génération de playbooks Ansible conformes aux normes ISO/IEC 27001 et 27002.
        Vous devez générer uniquement un playbook YAML complet et bien structuré, sans explications ni commentaires supplémentaires.
        
        ### Normes à respecter :
        - Confidentialité : Utilisez des connexions sécurisées (SSH, TLS).
        - Contrôle d'accès : Limitez les accès administratifs avec des identifiants sécurisés ou des clés SSH.
        - Journalisation : Ajoutez des étapes pour enregistrer les modifications sur les équipements.
        - Sécurité réseau : Configurez des règles de pare-feu pour filtrer le trafic non autorisé.

        ### Structure attendue :
        - Une section `vars` définissant les variables globales.
        - Une section `tasks` listant les étapes à exécuter.
        - Une section `handlers` pour les actions conditionnelles.
        """),
        ("human", f"Voici les besoins spécifiques de l'utilisateur : {description}. Générez un playbook YAML complet basé sur cette demande.")
    ])

    # Conversion du prompt en texte
    prompt_text = chat_prompt.format_prompt(description=description).to_string()

    # Appel de l'API OpenAI via le modèle
    try:
        ai_response = model.invoke(prompt_text)  # Utilisation de invoke au lieu de predict
    except Exception as e:
        st.error(f"Erreur lors de l'appel à l'API OpenAI : {e}")
        return None

    # Récupérer le contenu texte de la réponse
    if ai_response.content:
        cleaned_yaml = ai_response.content.strip().strip("```yaml").strip("```")
        return cleaned_yaml
    else:
        st.error("La réponse de l'API OpenAI est vide.")
        return None

def validate_yaml(yaml_content):
    """
    Valide que le contenu généré est bien en YAML.
    """
    try:
        yaml.safe_load(yaml_content)
        return True
    except yaml.YAMLError as e:
        st.error(f"Erreur dans le YAML généré : {e}")
        return False

def download_button(yaml_content, filename="playbook.yaml"):
    """
    Crée un bouton de téléchargement pour le fichier YAML.
    """
    st.download_button(
        label="Télécharger le fichier YAML",
        data=yaml_content,
        file_name=filename,
        mime="text/yaml"
    )
