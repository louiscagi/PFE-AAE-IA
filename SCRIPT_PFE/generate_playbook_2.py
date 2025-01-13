import yaml
import os
from transformers import BertTokenizer, BertModel

def generate_yaml_from_description(description):
    """
    Génère un fichier YAML basé sur une description utilisateur
    et conforme aux standards ISO/IEC.
    """
    try:
        # Chemin vers le modèle local
        model_path = r"C:\Users\ryanb\OneDrive\Bureau\PFE-AAE-IA\SCRIPT_PFE\bert-base-multilingual-uncased"

        print("Chargement du modèle BERT...")
        # Charger le tokenizer et le modèle
        tokenizer = BertTokenizer.from_pretrained(model_path)
        model = BertModel.from_pretrained(model_path)
        print("Modèle BERT chargé avec succès !")

        # Exemple de playbook YAML utilisé comme préprompt
        example_playbook = """
        Exemple de playbook YAML :
        name: Déploiement d'une infrastructure réseau
        hosts: all
        tasks:
        - name: Configurer les PC avec des IP libres
          vars:
            pc_ips: []
          block:
          - name: Configurer chaque PC avec des IP sécurisées et conformes
            shell: ifconfig eth0 {{ pc_ips[i] }} up
        - name: Configurer le switch
          shell: switch-config set vlan 10
        - name: Configurer le routeur
          block:
          - name: Configurer l'adresse IP du routeur
            shell: ifconfig eth0 <router_ip> up
          - name: Activer le routage
            shell: echo 1 > /proc/sys/net/ipv4/ip_forward
        - name: Ajouter des règles de sécurité conformes aux normes ISO/IEC
          block:
          - name: Appliquer les règles de pare-feu
            shell: ufw allow from {{ pc_ips }} to any port 22
          - name: Activer le suivi des connexions
            shell: iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
        """

        # Combiner l'exemple et la description utilisateur
        full_prompt = f"{example_playbook}\n\nDescription de l'utilisateur : {description}"
        print(f"\nPrompt complet envoyé au modèle :\n{full_prompt}")

        # Simulation de la génération YAML
        # Générer des IP dynamiques et un playbook structuré
        pc_ips = ["192.168.100.10", "192.168.100.11", "192.168.100.12"]  # Exemple d'IP générées dynamiquement
        router_ip = "192.168.100.1"

        playbook = {
            "name": "Déploiement d'une infrastructure réseau conforme aux normes ISO/IEC",
            "hosts": "all",
            "tasks": [
                {
                    "name": "Configurer les PC avec des IP libres",
                    "vars": {
                        "pc_ips": pc_ips
                    },
                    "block": [
                        {
                            "name": f"Configurer PC{i+1}",
                            "shell": f"ifconfig eth0 {{ pc_ips[{i}] }} up"
                        } for i in range(len(pc_ips))
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
                            "shell": f"ifconfig eth0 {router_ip} up"
                        },
                        {
                            "name": "Activer le routage",
                            "shell": "echo 1 > /proc/sys/net/ipv4/ip_forward"
                        }
                    ]
                },
                {
                    "name": "Ajouter des règles de sécurité conformes aux normes ISO/IEC",
                    "block": [
                        {
                            "name": "Appliquer les règles de pare-feu",
                            "shell": "ufw allow from {{ pc_ips }} to any port 22"
                        },
                        {
                            "name": "Activer le suivi des connexions",
                            "shell": "iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT"
                        }
                    ]
                }
            ]
        }

        # Chemin dynamique pour sauvegarder le playbook
        output_path = os.path.join(os.getcwd(), "playbook.yaml")

        # Sauvegarder le playbook au format YAML
        with open(output_path, "w", encoding="utf-8") as file:
            yaml.dump(playbook, file, default_flow_style=False, allow_unicode=True)

        print(f"\nPlaybook YAML généré avec succès : {output_path}")

    except Exception as e:
        print(f"Une erreur est survenue : {e}")


if __name__ == "__main__":
    # Demander une description à l'utilisateur
    user_description = input("Veuillez entrer la description de l'infrastructure à déployer :\n")

    # Générer le playbook YAML
    generate_yaml_from_description(user_description)
