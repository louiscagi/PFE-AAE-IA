# Guide Installation et Lancement - Application de Génération de Playbook YAML

## Description

Cette application permet de générer dynamiquement des fichiers **playbook YAML** conformes aux normes pour le déploiement et la configuration d'infrastructures réseau. Elle repose sur **Streamlit** pour l'interface utilisateur et utilise des modèles NLP (comme BERT) pour analyser les descriptions des utilisateurs et produire des configurations adaptées.

---

## Fonctionnalités

- **Génération de Playbook YAML :**

  - Analyse des descriptions utilisateur pour configurer automatiquement des PCs, switches, routeurs, etc.
  - Génération de fichiers YAML prêts à être exécutés par Ansible.

- **Traitement de fichiers ZIP :**

  - Upload de fichiers ZIP contenant des descriptions ou configurations réseau.
  - Traitement et génération de playbooks adaptés aux fichiers fournis.

- **Téléchargement des résultats :**
  - Téléchargez le playbook généré ou un fichier ZIP contenant les résultats des traitements.

---

## Prérequis

Avant de commencer, assurez-vous d'avoir :

1. **Python 3.8 ou plus** installé sur votre machine.
2. Les dépendances nécessaires listées dans le fichier `requirements.txt`.

---

## Installation

### Étape 1 : Clonez le repository

```bash
git clone <URL_DU_REPOSITORY>
cd <NOM_DU_REPOSITORY>
```

### Étape 2 : Créez un environnement virtuel

```bash
python -m venv env
source env/bin/activate  # Sur Windows : env\Scripts\activate
```

### Étape 3 : Installez les dépendances

```bash
pip install -r requirements.txt
```

### Étape 4 : Configurez les répertoires nécessaires

Créez les répertoires temporaires nécessaires :

```bash
mkdir temp temp_dir results_dir
```

---

## Lancement de l'application

### Étape 1 : Lancez le serveur Streamlit

```bash
streamlit run main.py
```

### Étape 2 : Accédez à l'application dans le navigateur

Après avoir lancé Streamlit, vous verrez un message comme celui-ci :

```plaintext
  Local URL: http://localhost:8501
  Network URL: http://<IP_DE_VOTRE_MACHINE>:8501
```

Ouvrez l'une des URLs dans votre navigateur pour accéder à l'interface utilisateur.

---

## Utilisation

### 1. Génération de Playbook YAML

- Saisissez une description dans la zone de texte (par exemple : _"Déployez 3 PC avec des IP libres, connectez-les à un switch, configurez un routeur sécurisé."_).
- Cliquez sur **"Générer le Playbook YAML"**.
- Téléchargez le fichier généré.

### 2. Traitement de fichiers ZIP

- Uploadez un fichier ZIP contenant des descriptions ou configurations réseau.
- Cliquez sur **"Télécharger le fichier ZIP avec les résultats"** une fois le traitement terminé.

### 3. Nettoyage des fichiers temporaires

- Cliquez sur **"Nettoyer les fichiers temporaires"** pour supprimer les fichiers générés et libérer de l'espace disque.

---

## Structure du Projet

```plaintext
<NOM_DU_REPOSITORY>/
├── main.py                 # Fichier principal Streamlit
├── utils/                  # Dossier contenant les utilitaires
│   ├── playbook_generator.py  # Génération dynamique des playbooks YAML
│   ├── file_processor.py      # Traitement des fichiers (ZIP, nettoyage, etc.)
│   └── analyze_description.py # Analyse des descriptions utilisateur
├── requirements.txt        # Liste des dépendances
├── temp/                   # Répertoire temporaire pour les fichiers uploadés
├── results_dir/            # Répertoire pour les résultats générés
└── README.md               # Documentation du projet
```

---

## Problèmes Courants

1. **Problème : Module non trouvé (`ModuleNotFoundError`)**

   - Vérifiez que l'environnement virtuel est activé.
   - Réinstallez les dépendances avec :
     ```bash
     pip install -r requirements.txt
     ```

2. **Problème : Port déjà utilisé**

   - Si Streamlit ne peut pas démarrer car le port est occupé, relancez-le sur un autre port :
     ```bash
     streamlit run main.py --server.port=8502
     ```

3. **Erreur d'importation des modules internes**
   - Assurez-vous que le fichier `__init__.py` existe dans le dossier `utils`.

---

## Contribution

Si vous souhaitez contribuer :

1. Forkez le repository.
2. Créez une branche avec votre fonctionnalité : `git checkout -b feature/ma-fonctionnalite`.
3. Faites un commit : `git commit -m "Ajout de ma fonctionnalité"`.
4. Poussez vos modifications : `git push origin feature/ma-fonctionnalite`.
5. Créez une pull request.

---

## Auteurs

- **Nom 1** - Développement principal
- **Nom 2** - Documentation et support
- **Nom 3** - Tests et validation

---

## Licence

Ce projet est sous licence [MIT](https://opensource.org/licenses/MIT).
