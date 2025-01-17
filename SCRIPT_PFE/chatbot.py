import openai
import streamlit as st
from langchain.chat_models import ChatOpenAI
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

    # Création du prompt structuré
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", """
        Vous êtes un assistant spécialisé dans la génération de playbooks Ansible adaptés à des besoins variés en déploiement de ressources informatiques.
        Votre objectif est de générer des playbooks Ansible bien structurés et respectant les bonnes pratiques.

        ### Standards à respecter
        - Utilisez des variables globales définies dans une section `vars`.
        - Assurez-vous que le playbook soit modulaire et facilement compréhensible.
        - Privilégiez les modules Ansible natifs lorsque cela est possible, mais utilisez des commandes `shell` ou `command` uniquement si nécessaire.
        - Incluez des `handlers` pour redémarrer les services ou appliquer des changements conditionnels.
        - Fournissez une description claire pour chaque tâche avec un champ `name`.
        - Générez des playbooks pouvant être exécutés directement avec Ansible.

        ### Structure minimale attendue
        - Le playbook doit contenir des sections claires :
          - `vars`: Variables globales pour les adresses IP, VLANs, mots de passe, etc.
          - `tasks`: Tâches organisées par objectif (ex. configuration réseau, déploiement de logiciels).
          - `handlers`: Actions déclenchées conditionnellement.

        ### Rappel
        - Le contenu doit être adapté à la demande utilisateur.
        - Soyez précis dans les configurations et veillez à inclure toutes les étapes nécessaires pour une exécution réussie.
        """),
        ("human", f"Générez un playbook YAML basé sur cette demande : {description}")
    ])

    # Conversion des messages en un texte brut pour le modèle
    prompt_text = chat_prompt.format_prompt(descriptions=description).to_string()

    # Appel de l'API OpenAI via le modèle
    ai_response = model.predict(prompt_text)

    # Nettoyage des balises Markdown
    cleaned_yaml = ai_response.strip().strip("```yaml").strip("```")

    return cleaned_yaml

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
