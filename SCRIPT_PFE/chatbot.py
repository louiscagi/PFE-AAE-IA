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

def add_message(role, content):
    """Ajoute un message à l'historique."""
    st.session_state.messages.append({"role": role, "content": content})

def query_with_yaml_and_description(description):
    """
    Génère une réponse contenant une introduction explicative et un fichier YAML basé sur une description.
    """
    add_message("user", description)

    # Création du modèle OpenAI avec LangChain
    model = ChatOpenAI(
        model_name="gpt-4",
        temperature=0.7,
        max_tokens=4000
    )

    chat_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    Vous êtes un assistant spécialisé dans la génération de playbooks Ansible conformes aux normes ISO pour la gestion de la sécurité de l'information. 
    Tous les playbooks que vous produisez doivent être alignés avec les normes suivantes :

    ### Normes ISO à respecter :
    - **ISO/IEC 27001** (Système de gestion de la sécurité de l'information) :
      - Assurez-vous que les suggestions intègrent des contrôles pour garantir la confidentialité, l'intégrité et la disponibilité de l'information.
      - Intégrez des mesures adaptées à la gestion des risques organisationnels.
    - **ISO/IEC 27002** (Bonnes pratiques pour la sécurité de l'information) :
      - Intégrez des contrôles spécifiques comme la gestion des accès, la protection des actifs, et le contrôle des réseaux.
      - Proposez des mesures concrètes basées sur les meilleures pratiques.
    - **ISO/IEC 27004** (Mesure de la sécurité de l'information) :
      - Fournissez des indicateurs clés de performance (KPI) pour évaluer les configurations proposées.
    - **ISO/IEC 27005** (Gestion des risques liés à la sécurité de l'information) :
      - Identifiez les menaces potentielles et proposez des approches basées sur une évaluation des risques.
    - **ISO/IEC 27032** (Cybersécurité) :
      - Fournissez des conseils sur la prévention, la détection et la réponse aux cybermenaces.
    - **ISO/IEC 27033** (Sécurité des réseaux) :
      - Concentrez-vous sur la segmentation des réseaux, la gestion des pare-feu et la sécurisation des points d'accès.

    ### Directives pour les playbooks :
    - Structurez les playbooks avec les sections suivantes :
      - Une section `vars` définissant les variables dynamiques et globales.
      - Une section `tasks` listant les étapes nécessaires pour implémenter les configurations.
      - Une section `handlers` pour les actions conditionnelles (par ex., redémarrage d'un service après une modification).
    - Les playbooks doivent inclure des configurations pour :
      - La sécurisation des accès administratifs.
      - La segmentation des réseaux (ex. : VLAN).
      - La configuration des pare-feu et des règles de sécurité.
    - Ne spécifiez pas de valeurs fixes comme des adresses IP, sauf si elles sont données par l'utilisateur.

    Fournissez une réponse en deux parties dans un seul message :
    1. Une introduction expliquant brièvement les étapes principales du playbook et comment elles respectent les normes ISO.
    2. Un playbook YAML complet, structuré, et prêt à être exécuté.

    """),
    ("human", f"Voici les besoins spécifiques de l'utilisateur : {description}. Répondez avec un playbook YAML valide.")
])


    prompt_text = chat_prompt.format_prompt(description=description).to_string()

    try:
        ai_response = model.invoke(prompt_text)
    except Exception as e:
        st.error(f"Erreur lors de l'appel à l'API OpenAI : {e}")
        return None, None

    if ai_response.content:
        cleaned_response = ai_response.content.strip()
        
        if "```yaml" in cleaned_response:
            yaml_start = cleaned_response.find("```yaml") + len("```yaml")
            yaml_end = cleaned_response.rfind("```")
            yaml_content = cleaned_response[yaml_start:yaml_end].strip()
        else:
            yaml_content = None

        add_message("assistant", cleaned_response)
        return yaml_content, cleaned_response
    else:
        st.error("La réponse de l'API OpenAI est vide.")
        return None, None

def explain_playbook(yaml_content):
    """
    Envoie le contenu du playbook YAML à l'API OpenAI pour obtenir une explication détaillée.
    """
    model = ChatOpenAI(
        model_name="gpt-4",
        temperature=0.7,
        max_tokens=4000
    )

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", """
        Vous êtes un assistant spécialisé dans l'analyse et l'explication des playbooks Ansible.
        Fournissez une explication détaillée, section par section, du playbook fourni, en respectant les points suivants :
        - Expliquez chaque section (`vars`, `tasks`, `handlers`) en détail.
        - Décrivez le rôle de chaque variable et tâche.
        - Vérifiez que le playbook respecte les normes ISO/IEC 27001 et 27002.

        Si le playbook contient des erreurs, identifiez-les et proposez des corrections.
        """),
        ("human", f"Voici un playbook YAML : \n\n{yaml_content}\n\nExpliquez-le en détail.")
    ])

    prompt_text = chat_prompt.format_prompt().to_string()

    try:
        ai_response = model.invoke(prompt_text)
        return ai_response.content.strip()
    except Exception as e:
        st.error(f"Erreur lors de l'appel à l'API OpenAI : {e}")
        return None

def validate_yaml(yaml_content):
    """
    Valide que le contenu généré suit la structure attendue d’un playbook Ansible.
    """
    try:
        yaml.safe_load(yaml_content)
        return True
    except yaml.YAMLError as e:
        st.error(f"Erreur dans le YAML généré : {e}")
        return False

def download_button(yaml_content, filename, key):
    """
    Crée un bouton de téléchargement pour le fichier YAML.
    """
    st.download_button(
        label="Télécharger le fichier YAML",
        data=yaml_content,
        file_name=filename,
        mime="text/yaml",
        key=key
    )
