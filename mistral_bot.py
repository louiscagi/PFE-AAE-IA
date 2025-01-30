import os
import yaml
import re
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

# Charger la clé API Mistral depuis l'environnement
api_key_mistral = os.getenv("MISTRAL_API_KEY")
if not api_key_mistral:
    raise ValueError("La clé API MISTRAL_API_KEY n'est pas définie dans .env.")

# Initialisation du modèle Mistral
llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0,
    max_retries=2,
)

def get_prompt(description):
    return ChatPromptTemplate.from_messages([
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
    ("human", f"Voici les besoins spécifiques de l'utilisateur : {description}. Répondez avec un playbook YAML valide."),
    ]
)

# Fonction principale pour interroger Mistral
def query_mistral(description):
    chat_prompt = get_prompt(description)
    prompt_text = chat_prompt.format_prompt(description=description).to_string()

    try:
        ai_response = llm.invoke(prompt_text)
        cleaned_response = ai_response.content.strip()

        # Extraire la partie YAML
        yaml_content = None
        if "```yaml" in cleaned_response:
            yaml_start = cleaned_response.find("```yaml") + len("```yaml")
            yaml_end = cleaned_response.rfind("```")
            yaml_content = cleaned_response[yaml_start:yaml_end].strip()

        return yaml_content, cleaned_response
    except Exception as e:
        return None, f"Erreur avec Mistral : {e}"

# Fonction pour expliquer un playbook avec Mistral
def explain_playbook_mistral(yaml_content):
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "Expliquez ce playbook Ansible section par section."),
        ("human", f"Voici un playbook YAML : \n\n{yaml_content}\n\nExpliquez-le en détail."),
    ])

    try:
        ai_response = llm.invoke(chat_prompt.format_prompt().to_string())
        return ai_response.content.strip()
    except Exception as e:
        return f"Erreur avec Mistral : {e}"