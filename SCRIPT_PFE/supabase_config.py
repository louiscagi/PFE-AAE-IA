from supabase import create_client
import os

# Configuration Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "votre_url_supabase")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "votre_service_role_key")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
