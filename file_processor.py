import zipfile
import os
import shutil
import openai

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
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(TEMP_DIR)
    return os.listdir(TEMP_DIR)

def process_files_with_chatgpt(files):
    """
    Traite chaque fichier texte avec ChatGPT et retourne les chemins des résultats.
    """
    results = []
    for file_name in files:
        file_path = os.path.join(TEMP_DIR, file_name)
        if os.path.isfile(file_path):
            with open(file_path, "r") as file_content:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": file_content.read()}],
                )
                result_file_path = os.path.join(RESULTS_DIR, f"result_{file_name}")
                with open(result_file_path, "w") as result_file:
                    result_file.write(response.choices[0].message["content"])
                results.append(result_file_path)
    return results

def create_result_zip(result_files):
    """
    Crée un fichier ZIP contenant tous les résultats et retourne son chemin.
    """
    result_zip_path = os.path.join(TEMP_DIR, "results.zip")
    with zipfile.ZipFile(result_zip_path, "w") as result_zip:
        for result_file in result_files:
            result_zip.write(result_file, os.path.basename(result_file))
    return result_zip_path
