# network-monitoring-tcp
## Description:
 Application de monitoring réseau distribuée basée sur une architecture client–serveur TCP. Chaque agent collecte périodiquement les métriques système (CPU, RAM) et les envoie à un serveur central. 
## Prérequis :
- Python 3.x 
- pip install psutil 
## Fichiers :
serveur.py → collecteur central TCP 
client.py → agent qui envoie CPU et RAM 
test_malformed.py → test messages mal formés (test 4)
 test_stats.py → test calcul statistiques (test 5) 
stats.csv → export automatique des statistiques (généré automatiquement) 
## Comment lancer le projet:
 ### 1. Installer les dépendances pip install psutil
### 2. Lancer le serveur (terminal 1) python serveur.py 
### 3. Lancer un agent (terminal 2) python client.py 
### 4. Lancer plusieurs agents simultanément
 # terminal 2 python client.py 
# terminal 3 python client.py
 # terminal 4 python client.py
 ## Protocole de communication :
HELLO <agent_id> <hostname> → enregistrement
 REPORT <agent_id> <timestamp> <cpu> <ram> → envoi métriques BYE <agent_id> → déconnexion 
Réponses serveur : OK ou ERROR
 ## Extensions implémentées 
- Détection agents inactifs (timeout 3 x T secondes) 
- Export automatique CSV (stats.csv) 
- Identifiant unique UUID par agent ## Arrêter les programmes Ctrl+C dans chaque terminal
