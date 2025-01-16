import yaml
from langchain_core.prompts import ChatPromptTemplate
from transformers import AutoModel, AutoTokenizer
#from langchain_core.output_parsers import YamlOutputParser

#output_parser = YamlOutputParser()


def generate_yaml_from_description(description):
    
    # Téléchargez le modèle et sauvegardez-le dans un répertoire local
    model_name = "bert-base-multilingual-uncased"
    save_directory = "../bert-base-multilingual-uncased"

    # Téléchargement du tokenizer et du modèle
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    # Sauvegarde du tokenizer et du modèle en local
    tokenizer.save_pretrained(save_directory)
    model.save_pretrained(save_directory)
    # Création des messages du chat
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system","""Générez un playbook YAML conforme aux meilleures pratiques en matière de sécurité et de gestion des infrastructures réseau. Le playbook doit respecter les normes ISO suivantes et inclure les structures obligatoires d’un playbook Ansible :

    ---

    ### Normes ISO à Respecter

    #### ISO/IEC 27001 : Gestion des systèmes de sécurité de l'information (SMSI).
    - Implémentez un système de gestion pour protéger les informations sensibles.
    - Configurez des VLANs pour isoler les segments réseau.
    - Activez des mécanismes de chiffrement (SSH, TLS) pour sécuriser les communications.
    - Configurez les accès utilisateur avec des mots de passe robustes ou des clés SSH.

    #### ISO/IEC 27002 : Code de bonnes pratiques pour les contrôles de sécurité.
    - Sécurisez les équipements réseau avec des pare-feu, des règles de contrôle d'accès et le chiffrement des données en transit.
    - Ajoutez des mécanismes de sauvegarde et de restauration pour garantir la résilience du système.

    ---

    ### Structure Requise pour un Playbook Ansible

    - Chaque play doit contenir :
    - `name` : Une description claire de ce que fait le play.
    - `hosts` : Les hôtes cibles (`all` ou spécifiques comme `switch`, `router`).
    - `tasks` : Une liste d’actions à exécuter.

    - Exemple minimal :
    ```yaml
    - name: Configuration des équipements réseau
        hosts: all
        become: true
        tasks:
        - name: Mise à jour des paquets sur les hôtes
            apt:
            update_cache: yes
            upgrade: yes"""),
        ("human", "Voici la demande de l'utilsateur et tu dois générer un fichier .yaml: \n{description}")
    ])
    
    # Création de la chaîne de traitement
    chain = chat_prompt | model 

    # Appel de la chaîne de traitement
    return chain.invoke(description)



