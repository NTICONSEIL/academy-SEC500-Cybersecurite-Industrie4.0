# Annexe contexte métier — MecaProd

MecaProd est une PME industrielle exploitant un atelier de production semi-automatisé.
Un incident récent a conduit à un arrêt partiel de production et à une suspicion de compromission d'un poste exposé.

## Problèmes observés
- absence de segmentation claire IT / OT
- services legacy encore accessibles
- protocole Modbus utilisé sans contrôle d'accès au niveau réseau
- broker MQTT anonyme
- supervision non cloisonnée

## Objectif du TP
Réaliser un audit technique initial puis proposer un redesign sécurisé.
