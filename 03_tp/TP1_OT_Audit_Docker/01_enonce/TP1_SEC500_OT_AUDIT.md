# TP1 — Audit cybersécurité OT avec lab Docker

## Durée
3h30

## Contexte
Vous intervenez après un incident de sécurité sur un atelier connecté. Votre mission consiste à :
1. cartographier le segment OT,
2. identifier les vulnérabilités exposées,
3. observer des flux industriels non sécurisés,
4. proposer une architecture sécurisée.

## Réseau du lab
- Analyste : `192.168.10.50`
- PLC1 : `192.168.10.110`
- PLC2 : `192.168.10.111`
- HMI : `192.168.10.120`
- Legacy file server : `192.168.10.130`
- MQTT broker : `192.168.10.200`
- MQTT publisher : `192.168.10.201`

## Travail demandé

### Partie 1 — Reconnaissance
- découvrir les hôtes actifs du réseau
- identifier les ports et services exposés
- repérer les ports OT et les services legacy

### Partie 2 — Analyse protocolaire
- interroger les PLC via `modbus-discover`
- lire puis écrire un registre Modbus dans le lab
- observer les échanges avec `tshark` ou `tcpdump`
- écouter les messages MQTT en clair

### Partie 3 — Diagnostic sécurité
- lister les vulnérabilités principales
- qualifier les risques
- distinguer les impacts IT et OT

### Partie 4 — Architecture cible
- proposer un schéma IT / DMZ / OT
- définir les flux autorisés et interdits
- recommander des contre-mesures prioritaires

## Livrables
- tableau d'inventaire
- tableau de vulnérabilités
- extraits de commandes / captures
- schéma d'architecture sécurisée
- plan d'action priorisé
