from transformers import BertTokenizer, BertModel
import torch

def test_bert():
    try:
        # Chemin du modèle (local ou distant)
        model_path = r"C:\Users\ryanb\OneDrive\Bureau\PFE-AAE-IA\SCRIPT_PFE\bert-base-multilingual-uncased"

        
        print("Test : Chargement du tokenizer et du modèle BERT...")
        # Charger le tokenizer et le modèle
        tokenizer = BertTokenizer.from_pretrained(model_path)
        model = BertModel.from_pretrained(model_path)
        print("Modèle et tokenizer chargés avec succès !")

        # Exemple de texte à traiter
        text = "Bonjour, je teste BERT en français et en d'autres langues !"
        print(f"\nTexte d'entrée : {text}")

        # Tokenisation
        print("\nTest : Tokenisation...")
        inputs = tokenizer(text, return_tensors="pt")
        print(f"Tokens générés : {tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])}")
        
        # Passage dans le modèle
        print("\nTest : Passage dans le modèle BERT...")
        outputs = model(**inputs)

        # Afficher les dimensions des résultats
        print("\nRésultats générés par le modèle :")
        print(f"Forme du tenseur : {outputs.last_hidden_state.shape}")
        print(f"Représentation [CLS] : {outputs.last_hidden_state[:, 0, :].shape}")
        print("Test réussi !")

    except Exception as e:
        print(f"\nUne erreur est survenue : {e}")

if __name__ == "__main__":
    test_bert()
