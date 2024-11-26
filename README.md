# ordi-quantique.exe

### Sujet d'entraînement : **Déploiement d'une Infrastructure Réseau Complète avec Automatisation**

#### **Objectif pédagogique**  
Développer des compétences pratiques en déploiement d’infrastructures réseau, incluant :  
- La configuration matérielle (adressage IP, connexion des switchs/routeurs).  
- L'automatisation des déploiements avec Ansible et Terraform.  
- La création et la gestion d'une infrastructure virtuelle avec VirtualBox/VMware ou un cloud privé.  
- La mise en place de services réseau (Active Directory, serveur de messagerie, etc.).  
- La sécurisation et la gestion des accès utilisateurs.  

---

### **Partie 1 : Préparation de l’environnement**
1. **Matériel et prérequis** :
   - 10 postes physiques ou VM.
   - Un switch manageable et un routeur basique (ou simulateur réseau comme GNS3 ou Packet Tracer).
   - Un serveur hébergeant les scripts Ansible/Terraform.  

2. **Logiciels nécessaires** :
   - Terraform pour provisionner les VMs.  
   - Ansible pour configurer automatiquement les services et applications.  
   - Debian et Kali Linux comme OS pour les VMs.  

3. **Plan d’adressage réseau** :  
   - **Réseau local** : 192.168.100.0/24  
   - **Sous-réseaux** :  
     - 192.168.100.0/28 pour les serveurs.  
     - 192.168.100.16/28 pour les postes utilisateurs.  
   - **IP du routeur** : 192.168.100.1  

---

### **Partie 2 : Déploiement et configuration réseau**
1. **Configuration manuelle initiale** :  
   - Configurez le switch avec VLANs pour isoler le trafic.  
     - VLAN 10 : Serveurs.  
     - VLAN 20 : Postes utilisateurs.  
   - Configurez le routeur pour assurer la connexion entre VLANs et le routage vers l’extérieur.  
   - Assurez la connectivité entre tous les équipements.  

2. **Vérifications** :  
   - Utilisez des outils comme `ping`, `traceroute`, et `nmap` pour vérifier la configuration du réseau.  

---

### **Partie 3 : Automatisation avec Terraform et Ansible**
1. **Provisionnement des VMs avec Terraform** :
   - Écrivez un script Terraform pour déployer :  
     - 2 VMs Debian pour les services.  
     - 8 VMs Kali pour les postes utilisateurs.  

   Exemple de script Terraform pour une VM Debian :  
   ```hcl
   provider "virtualbox" {}

   resource "virtualbox_vm" "debian" {
     name   = "debian-server"
     cpus   = 2
     memory = 2048
     network_adapter {
       type           = "bridged"
       host_interface = "eth0"
     }
     os {
       iso_path = "path/to/debian.iso"
     }
   }
   ```

2. **Automatisation de la configuration avec Ansible** :
   - **Playbook pour les serveurs** :  
     - Installer Active Directory (`samba` pour AD sous Linux).  
     - Configurer un serveur de messagerie (Postfix/Dovecot).  
   - **Playbook pour les clients** :  
     - Configurer l’accès réseau et le client de messagerie.  
     - Ajouter les utilisateurs au domaine AD.  

---

### **Partie 4 : Mise en place des services**
1. **Active Directory (AD)** :  
   - Configurez un serveur Samba comme contrôleur de domaine.  
   - Créez un domaine nommé `lab.local`.  
   - Ajoutez des utilisateurs avec des permissions différentes.

2. **Serveur de messagerie** :  
   - Installez et configurez Postfix pour l'envoi de mails et Dovecot pour l'accès IMAP/POP3.  
   - Ajoutez des boîtes mails pour les utilisateurs du domaine AD.  

3. **Configuration des postes utilisateurs** :  
   - Configurez les postes Kali pour se connecter au domaine AD.  
   - Testez les connexions avec les utilisateurs créés.  

---

### **Partie 5 : Tests et validation**
1. **Tests réseau** :  
   - Vérifiez la connectivité entre tous les éléments du réseau.  
   - Analysez le trafic réseau avec Wireshark pour identifier d’éventuels problèmes.  

2. **Tests des services** :  
   - Authentifiez-vous sur le domaine avec les utilisateurs créés.  
   - Envoyez et recevez des emails entre utilisateurs.  

---

### **Partie 6 : Sécurisation et optimisation**
1. **Sécurisation des services** :  
   - Activez TLS pour les communications du serveur de messagerie.  
   - Configurez un pare-feu avec `ufw` ou `iptables` sur chaque VM.  

2. **Optimisation des performances** :  
   - Implémentez une solution de monitoring réseau comme Nagios ou Zabbix.  

---

### **Livrables attendus** :
1. Documentation des étapes suivies.  
2. Scripts Terraform et Ansible utilisés.  
3. Capture d'écran des tests réalisés (connexion AD, emails envoyés/reçus).  
4. Analyse des logs réseau et des performances.  

---

### Bonus : Scénario avancé
- Ajoutez un serveur Web avec Nginx et un certificat SSL.  
- Configurez un VPN pour permettre des connexions distantes sécurisées au réseau.  


