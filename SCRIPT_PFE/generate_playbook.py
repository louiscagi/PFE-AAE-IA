import yaml
from transformers import BertTokenizer, BertModel
import torch

def generate_playbook():
    try:
        # Chemin vers le modèle local
        model_path = r"C:\Users\ryanb\OneDrive\Bureau\PFE-AAE-IA\SCRIPT_PFE\bert-base-multilingual-uncased"

        print("Chargement du modèle BERT pour générer un playbook YAML...")
        # Charger le tokenizer et le modèle
        tokenizer = BertTokenizer.from_pretrained(model_path)
        model = BertModel.from_pretrained(model_path)
        print("Modèle chargé avec succès !")

        # Description en langage naturel pour générer le playbook
        description = """
        Déployez une infrastructure réseau avec :
        - 3 PC (PC1, PC2, PC3) avec des adresses IP libres.
        - 1 switch pour connecter les PC.
        - 1 routeur pour gérer la communication avec un réseau externe.
        
        Le playbook.yaml doit ressembler à ça:
        {
            "name": "Déploiement de l'infrastructure réseau",
            "hosts": "all",
            "tasks": [
                {
                    "name": "Configurer les 3 PC avec des IP libres",
                    "vars": {
                        "pc_ips": [...]
                    },
                    "block": [
                        {
                            "name": "Configurer PC1",
                            "shell": "ifconfig eth0 {{ pc_ips[0] }} up"
                        },
                        {
                            "name": "Configurer PC2",
                            "shell": "ifconfig eth0 {{ pc_ips[1] }} up"
                        },
                        {
                            "name": "Configurer PC3",
                            "shell": "ifconfig eth0 {{ pc_ips[2] }} up"
                        }
                    ]
                },
                {
                    "name": "Configurer le switch",
                    "shell": "switch-config set vlan 10"
                },
                {
                    "name": "Configurer le routeur",
                    "block": [
                        {
                            "name": "Configurer l'adresse IP du routeur",
                            "shell": "ifconfig eth0 192.168.1.1 up"
                        },
                        {
                            "name": "Activer le routage",
                            "shell": "echo 1 > /proc/sys/net/ipv4/ip_forward"
                        }
                    ]
                }
            ]
        } 
        """

        print("\nDescription utilisée pour générer le playbook :")
        print(description)

        # Tokenisation de la description
        inputs = tokenizer(description, return_tensors="pt")
        outputs = model(**inputs)

        '''
        # Structure YAML du playbook
        playbook = {
            "name": "Déploiement de l'infrastructure réseau",
            "hosts": "all",
            "tasks": [
                {
                    "name": "Configurer les 3 PC avec des IP libres",
                    "vars": {
                        "pc_ips": ["192.168.1.10", "192.168.1.11", "192.168.1.12"]
                    },
                    "block": [
                        {
                            "name": "Configurer PC1",
                            "shell": "ifconfig eth0 {{ pc_ips[0] }} up"
                        },
                        {
                            "name": "Configurer PC2",
                            "shell": "ifconfig eth0 {{ pc_ips[1] }} up"
                        },
                        {
                            "name": "Configurer PC3",
                            "shell": "ifconfig eth0 {{ pc_ips[2] }} up"
                        }
                    ]
                },
                {
                    "name": "Configurer le switch",
                    "shell": "switch-config set vlan 10"
                },
                {
                    "name": "Configurer le routeur",
                    "block": [
                        {
                            "name": "Configurer l'adresse IP du routeur",
                            "shell": "ifconfig eth0 192.168.1.1 up"
                        },
                        {
                            "name": "Activer le routage",
                            "shell": "echo 1 > /proc/sys/net/ipv4/ip_forward"
                        }
                    ]
                }
            ]
        }
            '''
        # Sauvegarder le playbook au format YAML
        with open("playbook.yaml", "w") as file:
            yaml.dump(playbook, file, default_flow_style=False, allow_unicode=True)

        print("\nPlaybook YAML généré avec succès : playbook.yaml")

    except Exception as e:
        print(f"\nUne erreur est survenue : {e}")

if __name__ == "__main__":
    generate_playbook()
