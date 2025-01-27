import os
import shutil

def delete_directory(directory_path):
    """Supprime un répertoire et tout son contenu."""
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
