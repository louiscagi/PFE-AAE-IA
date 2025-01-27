from supabase import create_client
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

# Récupérer les variables depuis le fichier .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Les variables SUPABASE_URL ou SUPABASE_KEY sont manquantes. Vérifiez votre fichier .env.")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
