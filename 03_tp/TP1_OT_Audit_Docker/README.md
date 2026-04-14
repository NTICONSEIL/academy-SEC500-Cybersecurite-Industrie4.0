# TP1 — Audit cybersécurité OT avec lab Docker

## Objectifs
- découvrir un réseau OT
- identifier les services exposés
- analyser Modbus/TCP et MQTT non sécurisés
- construire un diagnostic de sécurité
- proposer une architecture cible sécurisée

## Dossiers
- `01_enonce/` : sujet étudiant
- `02_ressources/` : contexte et annexes
- `03_lab/` : environnement Docker
- `04_docs_tech/` : commandes et aide
- `05_correction/` : corrigés
- `06_enseignant/` : guide enseignant

## Lancement rapide
```bash
cd 03_lab
docker compose up -d --build
docker exec -it sec500-analyst bash
```
