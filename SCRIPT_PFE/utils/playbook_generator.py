import yaml

def generate_yaml_from_description(description):
    """
    Génère un playbook YAML basé sur la description utilisateur avec des structures
    proches des modules Ansible modernes.
    """
    try:
        # Analyse simplifiée pour extraire les entités (exemple basique)
        entities = {
            "pcs": description.lower().count("pc"),
            "switches": description.lower().count("switch"),
            "routers": description.lower().count("routeur"),
            "stormshields": description.lower().count("stormshield"),
        }

        # Tâches dynamiques en fonction des entités détectées
        tasks = []

        # Mise à jour du système pour routeurs et switches
        tasks.append({
            "name": "Mise à jour du système sur le routeur et les switches",
            "apt": {
                "update_cache": True,
                "upgrade": "yes"
            },
            "when": "ansible_facts['os_family'] == 'Debian'"
        })

        # Configuration des PCs
        if entities["pcs"] > 0:
            pc_ips = [f"192.168.1.{i+2}" for i in range(entities["pcs"])]
            pc_interfaces = [
                {
                    "interface": "eth0",
                    "ip_address": ip,
                    "netmask": "255.255.255.0"
                }
                for ip in pc_ips
            ]
            tasks.append({
                "name": "Configuration des adresses IP sur les interfaces des PC",
                "ansible.builtin.network": {
                    "name": "{{ item.interface }}",
                    "ipv4": "{{ item.ip_address }}",
                    "netmask": "{{ item.netmask }}",
                    "state": "up"
                },
                "with_items": pc_interfaces,
                "when": "inventory_hostname in ['PC1', 'PC2', 'PC3']"
            })

        # Configuration des VLANs et interfaces sur le switch
        if entities["switches"] > 0:
            tasks.append({
                "name": "Configuration des VLANs sur le switch",
                "cisco.ios.ios_vlan": {
                    "vlan_id": 10,
                    "name": "VLAN_10",
                    "state": "present"
                },
                "when": "inventory_hostname == 'switch'"
            })
            tasks.append({
                "name": "Configuration de l'interface VLAN sur le switch",
                "cisco.ios.ios_interface": {
                    "name": "Vlan10",
                    "vlan_id": 10,
                    "ipv4": "192.168.10.1",
                    "netmask": "255.255.255.0",
                    "state": "up"
                },
                "when": "inventory_hostname == 'switch'"
            })

        # Configuration du routeur
        if entities["routers"] > 0:
            tasks.append({
                "name": "Configuration de l'interface du routeur",
                "cisco.ios.ios_interface": {
                    "name": "GigabitEthernet0/0",
                    "ipv4": "192.168.10.254",
                    "netmask": "255.255.255.0",
                    "state": "up"
                },
                "when": "inventory_hostname == 'routeur'"
            })
            tasks.append({
                "name": "Activation du routage sur le routeur",
                "cisco.ios.ios_routing": {
                    "router_bgp": {
                        "asn": 65001,
                        "networks": ["192.168.10.0/24"]
                    }
                },
                "when": "inventory_hostname == 'routeur'"
            })
            tasks.append({
                "name": "Configuration du route statique sur le routeur",
                "cisco.ios.ios_static_route": {
                    "network": "0.0.0.0",
                    "netmask": "0.0.0.0",
                    "next_hop": "192.168.10.254"
                },
                "when": "inventory_hostname == 'routeur'"
            })

        # Configuration du Stormshield
        if entities["stormshields"] > 0:
            tasks.append({
                "name": "Configurer le Stormshield",
                "block": [
                    {
                        "name": "Configurer les règles de pare-feu",
                        "shell": "stormshield set firewall rules"
                    },
                    {
                        "name": "Activer la sécurité avancée",
                        "shell": "stormshield enable advanced-security"
                    }
                ]
            })

        # Création du playbook final
        playbook = {
            "name": "Configuration des équipements réseau",
            "hosts": "all",
            "become": True,
            "tasks": tasks
        }

        # Génération du YAML
        return yaml.dump(playbook, default_flow_style=False, allow_unicode=True)

    except Exception as e:
        raise RuntimeError(f"Erreur lors de la génération du playbook : {e}")
