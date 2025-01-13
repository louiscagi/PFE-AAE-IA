import zipfile
import os
import shutil
from transformers import BertTokenizer, BertModel

# Chemin vers le modèle BERT local
MODEL_PATH = r"C:\Users\ryanb\OneDrive\Bureau\PFE-AAE-IA\SCRIPT_PFE\bert-base-multilingual-uncased"


# Répertoires temporaires
TEMP_DIR = "temp/"
RESULTS_DIR = "temp/results/"

def initialize_directories():
    """Crée les répertoires temporaires nécessaires."""
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)

def clean_directories():
    """Supprime les répertoires temporaires pour le nettoyage."""
    shutil.rmtree(TEMP_DIR, ignore_errors=True)

def extract_zip(file_path):
    """
    Extrait un fichier ZIP dans le répertoire temporaire.
    Retourne la liste des fichiers extraits.
    """
    try:
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(TEMP_DIR)
        print(f"Fichiers extraits avec succès dans {TEMP_DIR}.")
        return os.listdir(TEMP_DIR)
    except zipfile.BadZipFile:
        print("Erreur : Le fichier uploadé n'est pas un fichier ZIP valide.")
        return []

def process_files_with_bert(files):
    """
    Traite chaque fichier texte avec le modèle BERT local et retourne les chemins des résultats.
    """
    print("Chargement du modèle BERT...")
    tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
    model = BertModel.from_pretrained(MODEL_PATH)
    print("Modèle BERT chargé avec succès !")

    results = []
    for file_name in files:
        file_path = os.path.join(TEMP_DIR, file_name)
        if os.path.isfile(file_path):
            try:
                print(f"Traitement du fichier : {file_name}")
                with open(file_path, "r", encoding="utf-8") as file_content:
                    text = file_content.read()
                    # Tokenisation et traitement avec BERT
                    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
                    outputs = model(**inputs)

                    # Génération du résultat simulé
                    result_content = (
                        f"Fichier traité : {file_name}\n"
                        f"Taille de la représentation BERT : {outputs.last_hidden_state.shape}\n"
                        f"Contenu du fichier :\n{text[:500]}...\n"  # Limité à 500 caractères pour l'aperçu
                    )

                    # Sauvegarder le résultat
                    result_file_path = os.path.join(RESULTS_DIR, f"result_{file_name}")
                    with open(result_file_path, "w", encoding="utf-8") as result_file:
                        result_file.write(result_content)

                    results.append(result_file_path)
            except Exception as e:
                print(f"Erreur lors du traitement du fichier {file_name} : {e}")
    return results

def create_result_zip(result_files):
    """
    Crée un fichier ZIP contenant tous les résultats et retourne son chemin.
    """
    try:
        result_zip_path = os.path.join(TEMP_DIR, "results.zip")
        with zipfile.ZipFile(result_zip_path, "w") as result_zip:
            for result_file in result_files:
                result_zip.write(result_file, os.path.basename(result_file))
        print(f"Fichier ZIP créé avec succès : {result_zip_path}")
        return result_zip_path
    except Exception as e:
        print(f"Erreur lors de la création du fichier ZIP : {e}")
        return None
