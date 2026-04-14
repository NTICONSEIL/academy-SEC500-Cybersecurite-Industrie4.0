# 🔐 SEC500 — Cybersécurité appliquée à l'Industrie 4.0

📍 Mastère Chef de Projet Industrie 4.0 — JUNIA XP  
📅 Année académique : 2025 / 2026  
👨‍🏫 Formateur : Christophe Croisant  

---

## 🎯 Objectifs du module

Ce module vise à former des experts capables de :

- Identifier les risques cyber dans les environnements industriels (OT)
- Réaliser un audit de sécurité sur une architecture Industrie 4.0
- Concevoir des architectures sécurisées (defense-in-depth)
- Mettre en œuvre des solutions de supervision et de détection
- Réagir à un incident de cybersécurité industriel

👉 Conformément au syllabus officiel SEC500 :contentReference[oaicite:0]{index=0}

---

## 🏭 Contexte pédagogique

Les travaux pratiques s'appuient sur des environnements simulés reproduisant :

- des réseaux industriels (OT)
- des automates (PLC)
- des protocoles industriels (Modbus, MQTT…)
- des scénarios d’attaque réalistes (ransomware, falsification)

---

## 🧱 Structure du dépôt

```bash
SEC500/
│
├── 00_module/                # Présentation du module
├── 01_positionnement/        # Évaluation initiale
├── 02_supports_cours/        # Slides et contenus pédagogiques
│
├── 03_tp/
│   ├── TP1_OT_Audit_Docker/  # Audit cybersécurité OT (lab Docker)
│   ├── TP2_Securisation_Architecture/
│   └── TP3_Incident_Response_OT/
│
├── 04_evaluations/           # QCM, études de cas
├── 05_annexes/               # Ressources complémentaires
│
└── README.md