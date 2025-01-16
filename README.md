# PFE-AAE-IA

# README - Projet PFE24-T-409

## Introduction

Le projet PFE24-T-409, réalisé en partenariat avec l’EAC2P et l’Armée de l’Air et de l’Espace (AAE), s’inscrit dans une démarche d’innovation en exploitant les potentialités des intelligences artificielles (IA) génératives.

Ce projet, initié suite à des travaux de stage menés par Marc-Antoine et Louis à l’EAC2P, vise à automatiser et optimiser les processus de configuration des infrastructures SIC (« Systèmes d’Information et de Communication ») pour les opérations aériennes grâce à des modèles d’IA performants et adaptés.

## Objectifs du projet

Le projet, planifié d’août 2024 à février 2025, poursuit les objectifs suivants :

IA générative : Concevoir et implémenter une IA capable de produire automatiquement des scripts de configuration Ansible pour des infrastructures SIC en respectant les besoins opérationnels et les standards de sécurité.

Benchmark IA : Évaluer les performances des modèles d’IA à travers un benchmarking rigoureux basé sur des indicateurs clés (KPI).

Interface utilisateur (MVP) : Développer une interface intuitive permettant une exploitation directe des sorties IA et une interaction utilisateur simplifiée.

## Structure du projet

### 1. Contexte et bénéficiaires

EAC2P : Chargée du déploiement des infrastructures SIC pour les opérations aériennes, avec le support du BCSIT pour les projets techniques et innovants.

Client : L’EAC2P, représentée par le CNE Adrien et le LTN Matthieu.

Equipe projet : Une équipe de six étudiants ingénieurs de l’ECE dirigée par Marc-Antoine Grabey.

### 2. Périmètre technique

Le projet se concentre sur trois volets :

IA générative : Prise en charge de multiples types d’entrées (texte, images, fichiers ZIP) pour générer des scripts conformes aux besoins opérationnels.

Benchmark IA : Fine-tuning et tests des modèles IA pour garantir qualité et conformité aux normes.

Interface utilisateur : Création d’un outil front-end connecté à l’IA pour visualiser et interagir avec les résultats.

### 3. Technologies utilisées

IA

Mistral AI : Modèle français garantissant souveraineté et conformité aux besoins nationaux.

LLaMA 2 : Modèle performant pour les tâches complexes.

GPT-3 : Modèle de référence pour la génération de code et la compréhension du langage naturel.

Interface utilisateur

Streamlit : Framework pour développer une interface web interactive et intuitive.

Normes de sécurité

ISO 27XXX : Gestion sécurisée des systèmes d’information.

### 4. Fonctionnalités principales

IA générative

Normalisation des entrées pour garantir des résultats précis.

Production de fichiers Ansible ou Terraform.

Visualisation d’architectures et explications des résultats.

Benchmark IA

Constitution d’un dataset pour le fine-tuning.

Tests sur des scénarios représentatifs (ex. : déploiement de 10 VM avec routeurs et pare-feu).

Analyse basée sur des KPI tels que temps, qualité et sécurité.

Interface utilisateur

Prise en charge d’entrées multiples (texte, images, fichiers ZIP).

Visualisation des entrées et sorties (code, fichiers, diagrammes).

Historique des interactions avec l’IA.

## Contraintes

Souveraineté : Priorisation des modèles IA français pour garantir l’indépendance technologique.

Calendrier : Remise des livrables entre octobre 2024 et février 2025.

Sécurité : Respect des normes ISO 27XXX et garantie de conformité des scripts aux standards de l’ANSSI.

## Livrables

Modèle d’IA générative : Fonctionnel, capable de produire des configurations qualitatives et sécurisées.

Module de benchmark : Évaluation rigoureuse des performances IA.

Interface utilisateur : Intuitive, connectée et dotée d’un suivi des interactions.

## Équipe projet

Chef de projet : Marc-Antoine Grabey

Membres : Louis Cagi Nicolau, Aymeric Moulet, Ryan Bagot, Adrien Beuve, Sébastien Baranger.

Pour toute question ou contribution, veuillez contacter l'équipe projet via leurs canaux de communication ou consulter la documentation complète disponible dans ce dépôt.


# Manuel D'Utilisation


## PFE-AAE-IA: Plateforme d'Intelligence Artificielle pour le Déploiement SIC

## Description du Projet
Ce projet est une application permettant de simplifier la gestion et le déploiement d’infrastructures SIC (Systèmes d'Information et de Communication) dans un contexte militaire.

L'application combine un chatbot alimenté par l'API OpenAI et des outils de traitement de fichiers pour automatiser des processus clés tels que :
- Génération de fichiers YAML pour des infrastructures.
- Analyse et traitement de fichiers ZIP via des modèles d'intelligence artificielle.

## Fonctionnalités
1. **Chatbot interactif** :
   - Capable de répondre à des questions et de traiter des requêtes complexes.
   - Historique des conversations accessible via une barre latérale.

2. **Générateur de fichiers YAML** :
   - Produit des fichiers YAML basés sur des descriptions en langage naturel.
   - Prend en charge des cas d’usage avancés, tels que la configuration d'infrastructures complètes.

3. **Traitement des fichiers ZIP** :
   - Extraction de fichiers contenus dans un ZIP.
   - Analyse des fichiers via des modèles d'intelligence artificielle (ChatGPT et Mistral AI).
   - Génération d'un ZIP contenant les résultats du traitement.

4. **Nettoyage des fichiers temporaires** :
   - Suppression des fichiers et répertoires intermédiaires pour maintenir un espace de travail propre.

---

## Guide d'Installation

### Prérequis
- Python 3.8 ou version supérieure.
- Une clé API OpenAI et/ou Mistral AI.
- Les outils suivants doivent être installés sur votre système :
  - pip (gestionnaire de paquets Python).

### Installation
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/louiscagi/PFE-AAE-IA.git
   cd PFE-AAE-IA
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Configurez vos clés API :
   - Ajoutez vos clés OpenAI et Mistral AI dans le fichier `Secrets` de Streamlit ou comme variables d'environnement :
     ```bash
     export OPENAI_API_KEY=your_openai_api_key
     export MISTRAL_API_KEY=your_mistral_api_key
     ```

4. Lancez l'application :
   ```bash
   streamlit run main.py
   ```

---

## Utilisation

### 1. Chatbot
- Une fois l'application lancée, accédez à la section **Chatbot pour Déploiement SIC**.
- Saisissez votre question ou description dans le champ de texte et cliquez sur « Envoyer ».
- Consultez les réponses dans la fenêtre principale et l’historique des conversations dans la barre latérale.

### 2. Génération de YAML
- Accédez à la section **Générateur YAML avec ChatGPT**.
- Fournissez une description textuelle de l’infrastructure souhaitée.
- Cliquez sur « Générer YAML » pour afficher le fichier YAML produit.
- Vous pouvez copier ou télécharger ce fichier directement.

### 3. Traitement des fichiers ZIP
- Accédez à la section **Uploader et traiter un fichier ZIP**.
- Chargez un fichier ZIP contenant les données à analyser.
- Les fichiers extraits seront traités par les modèles d'intelligence artificielle.
- Une fois le traitement terminé, téléchargez un ZIP contenant les résultats.

### 4. Nettoyage des fichiers temporaires
- Cliquez sur le bouton **Nettoyer les fichiers temporaires** pour libérer l’espace occupé par les répertoires temporaires.

---

## Structure des Fichiers

### Dossiers Principaux
- **`temp/`** : Contient les fichiers temporaires lors des traitements.
- **`results/`** : Contient les résultats produits par les modèles d'IA.

### Scripts Principaux
- **`main.py`** : Point d'entrée de l'application.
- **`chatbot.py`** : Implémentation du chatbot basé sur OpenAI.
- **`draft.py`** : Gère le traitement des fichiers ZIP et leur analyse via Mistral AI.
- **`file_processor.py`** : Outils pour manipuler et analyser des fichiers.
- **`utils.py`** : Fonctions utilitaires pour la gestion des répertoires.
- **`query_yaml.py`** : Génération de fichiers YAML à partir de descriptions textuelles.

### Fichier de Configuration
- **`requirements.txt`** : Liste des dépendances nécessaires.

---

## Dépendances
- `streamlit` : Pour l’interface utilisateur.
- `openai` : Interaction avec l'API OpenAI.
- `langchain` et `langchain_community` : Gestion avancée des modèles et prompts.
- `PyYAML` : Manipulation des fichiers YAML.
- `SQLAlchemy` : Gestion des bases de données pour LangChain.
- `anyio` : Entrées/sorties asynchrones.
- `requests` : Gestion des requêtes HTTP.

---

## Contributeurs
- **Louis Cagi Nicolau** (Auteur Principal)
- Pour toute question ou suggestion, veuillez créer une « issue » sur ce dépôt.

---

## Licence
Ce projet est sous licence MIT. Consultez le fichier `LICENSE` pour plus d’informations.

---

## Améliorations Futures
- Intégration de nouveaux modèles pour améliorer la précision des analyses.
- Support multi-langue pour le chatbot.
- Optimisation des performances pour le traitement de fichiers volumineux.


