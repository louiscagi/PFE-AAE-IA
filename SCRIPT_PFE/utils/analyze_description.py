from transformers import pipeline

# Chargement d'un pipeline NLP
nlp = pipeline("text-classification", model="bert-base-multilingual-uncased", tokenizer="bert-base-multilingual-uncased")

def parse_request(description):
    """
    Analyse la description utilisateur pour extraire les entités clés.
    """
    # Exemple simplifié d'analyse des données
    # Vous pouvez utiliser une extraction de motifs ou un modèle plus avancé
    entities = {
        "pcs": description.count("PC") or 0,
        "switches": description.count("switch") or 0,
        "routers": description.count("routeur") or 0,
        "stormshields": description.count("stormshield") or 0,
    }
    return entities
