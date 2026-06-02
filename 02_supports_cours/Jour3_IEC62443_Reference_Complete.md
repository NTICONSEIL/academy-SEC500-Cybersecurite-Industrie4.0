# IEC 62443 — Référence complète
### Cybersécurité des systèmes d'automatisation et de contrôle industriels (IACS)
> Document de référence pédagogique — SEC500 · JUNIA XP 2025/2026 · Formateur : Christophe CROISANT

---

## Table des matières

1. [Introduction et contexte](#1-introduction-et-contexte)
2. [Structure de la norme](#2-structure-de-la-norme)
3. [Concepts fondamentaux](#3-concepts-fondamentaux)
4. [Modèle de maturité CSMS](#4-modèle-de-maturité-csms)
5. [Zones, conduits et niveaux de sécurité (SL)](#5-zones-conduits-et-niveaux-de-sécurité-sl)
6. [Les 7 familles d'exigences fondamentales (FR)](#6-les-7-familles-dexigences-fondamentales-fr)
7. [Exigences par niveau SL — détail FR1 à FR7](#7-exigences-par-niveau-sl--détail-fr1-à-fr7)
8. [Rôles et responsabilités](#8-rôles-et-responsabilités)
9. [Processus d'évaluation des risques (Risk Assessment)](#9-processus-dévaluation-des-risques-risk-assessment)
10. [Relation avec les autres normes](#10-relation-avec-les-autres-normes)
11. [Mise en œuvre pratique](#11-mise-en-œuvre-pratique)
12. [Certification et conformité](#12-certification-et-conformité)
13. [Cas d'usage et exemples industriels](#13-cas-dusage-et-exemples-industriels)
14. [Lexique complet IEC 62443](#14-lexique-complet-iec-62443)
15. [Références et ressources](#15-références-et-ressources)

---

## 1. Introduction et contexte

### 1.1 Origine et historique

La norme IEC 62443 est née de la convergence de deux initiatives parallèles :

- **ISA-99** (International Society of Automation) : groupe de travail lancé en 2002 par l'ISA pour répondre à l'absence de standards de cybersécurité dédiés aux systèmes industriels.
- **IEC TC65/WG10** : comité technique de l'IEC (International Electrotechnical Commission) chargé de transformer les travaux ISA-99 en standard international.

La première publication officielle sous le numéro IEC 62443 date de **2009** (partie 2-1). La norme est en évolution permanente : plusieurs parties ont été révisées ou sont en cours de révision en 2024-2025.

**Chronologie clé :**

| Année | Événement |
|-------|-----------|
| 2002 | Création du comité ISA-99 |
| 2007 | Publication des premiers documents ISA-99 |
| 2009 | Première publication IEC 62443-2-1 |
| 2013 | Publication IEC 62443-3-3 (exigences système) |
| 2016 | Publication IEC 62443-4-2 (exigences composants) |
| 2018 | Publication IEC 62443-4-1 (cycle de développement sécurisé) |
| 2020 | Révision IEC 62443-2-1 en cours (CSMS) |
| 2023 | Reconnaissance par l'UE dans le cadre de la directive NIS2 |
| 2024 | Référence dans le Cyber Resilience Act (CRA) européen |

### 1.2 Pourquoi une norme spécifique pour l'OT ?

Les systèmes informatiques industriels (OT — Operational Technology) présentent des caractéristiques fondamentalement différentes des systèmes IT classiques, qui rendent inapplicables les approches de sécurité traditionnelles :

| Critère | Environnement IT | Environnement OT |
|---------|-----------------|-----------------|
| **Priorité sécurité** | Confidentialité > Intégrité > Disponibilité | **Disponibilité > Intégrité > Confidentialité** |
| **Tolérance aux pannes** | Redémarrage acceptable | Arrêt = risque physique + pertes financières |
| **Cycle de vie** | 3–5 ans | **10–30 ans** (automates en production depuis 1995) |
| **Patch management** | Mise à jour rapide | Validation constructeur requise (délai 6–36 mois) |
| **Protocoles** | TCP/IP, TLS, SSH | Modbus, S7comm, DNP3, PROFINET (sans auth.) |
| **Temps réel** | Non critique | **Contraintes temps réel dures** (ms) |
| **Impact d'une attaque** | Perte de données | **Blessures physiques, explosion, pollution** |
| **Antivirus** | Standard | Souvent incompatible avec les systèmes legacy |
| **Chiffrement** | Systématique | Latence inacceptable sur équipements anciens |

### 1.3 Périmètre d'application

La norme IEC 62443 s'applique aux **IACS** (Industrial Automation and Control Systems), terme générique désignant :

- Les systèmes SCADA (Supervisory Control and Data Acquisition)
- Les systèmes DCS (Distributed Control Systems)
- Les systèmes PLC/API (Programmable Logic Controllers)
- Les systèmes de sécurité instrumentée (SIS — Safety Instrumented Systems)
- Les systèmes HMI (Human-Machine Interface)
- Les réseaux industriels et protocoles de communication OT
- Les systèmes IIoT (Industrial Internet of Things)
- Les équipements embarqués industriels

**Secteurs concernés :**
Énergie (oil & gas, électricité), eau et assainissement, chimie, pharmaceutique, agroalimentaire, automobile, aéronautique, transport, bâtiments intelligents (BMS/BAS), infrastructures critiques.

---

## 2. Structure de la norme

### 2.1 Organisation en 4 séries

La norme IEC 62443 est organisée en **4 séries** (General, Policies & Procedures, System, Component), chacune divisée en plusieurs parties. C'est un corpus normatif complet, pas un document unique.

```
IEC 62443
│
├── Série 1 — GÉNÉRAL (Concepts, terminologie, métriques)
│   ├── 1-1  Terminologie, concepts et modèles
│   ├── 1-2  Glossaire et abréviations (en cours)
│   ├── 1-3  Métriques de conformité (en cours)
│   └── 1-4  Cycle de vie IACS et cas d'utilisation (en cours)
│
├── Série 2 — POLITIQUES & PROCÉDURES (Organisation, processus)
│   ├── 2-1  Exigences pour un CSMS (Cybersecurity Management System)
│   ├── 2-2  Mise en œuvre du CSMS (en cours)
│   ├── 2-3  Gestion des patches
│   ├── 2-4  Exigences pour les prestataires de services IACS
│   └── 2-5  Guide d'installation et maintenance (en cours)
│
├── Série 3 — SYSTÈME (Architecture, exigences système)
│   ├── 3-1  Technologies de sécurité pour IACS
│   ├── 3-2  Évaluation des risques et conception du système de sécurité
│   └── 3-3  Exigences de sécurité système et niveaux de sécurité (SL)
│
└── Série 4 — COMPOSANT (Développement sécurisé, exigences composants)
    ├── 4-1  Exigences pour le cycle de développement sécurisé (SDL)
    └── 4-2  Exigences de sécurité technique pour les composants IACS
```

### 2.2 Description détaillée de chaque partie

#### IEC 62443-1-1 — Terminologie, concepts et modèles
Document fondateur. Définit le vocabulaire normatif (zone, conduit, SL, IACS…), introduit les modèles conceptuels (zones/conduits, niveaux de sécurité cible vs atteint) et établit le cadre général de la norme.

#### IEC 62443-2-1 — Exigences pour un CSMS
Définit les éléments d'un **Cybersecurity Management System** pour un asset owner (opérateur). S'inspire fortement d'ISO/IEC 27001 mais adapté au contexte OT. Couvre : la politique de sécurité, l'organisation, la gestion des risques, la continuité.

#### IEC 62443-2-3 — Gestion des patches
Traite spécifiquement du problème du patch management en environnement OT. Définit les responsabilités entre asset owner et product supplier pour la publication, le test et le déploiement des correctifs de sécurité.

#### IEC 62443-2-4 — Exigences pour les prestataires de services
Définit les exigences de sécurité applicables aux **intégrateurs système et prestataires de maintenance** intervenant sur des IACS. Très importante pour la gestion des risques fournisseurs (supply chain).

#### IEC 62443-3-2 — Évaluation des risques
Définit le processus d'**évaluation des risques de sécurité** pour les IACS, notamment la méthode pour déterminer le SL cible (SL-T) de chaque zone à partir de l'analyse de risques.

#### IEC 62443-3-3 — Exigences système et niveaux de sécurité
**Document central de la norme.** Définit les 7 familles d'exigences fondamentales (FR) et les 51 exigences système (SR) déclinées sur 4 niveaux de sécurité (SL-1 à SL-4). C'est le document le plus fréquemment cité en audit.

#### IEC 62443-4-1 — Cycle de développement sécurisé (SDL)
Définit les exigences applicables aux **fabricants de produits et composants** IACS pour intégrer la sécurité dès la conception (Security by Design). Couvre : gestion des vulnérabilités, test de sécurité, documentation sécurité.

#### IEC 62443-4-2 — Exigences techniques pour les composants
Décline les exigences de la série 3-3 au niveau des **composants individuels** (automates, switches industriels, logiciels embarqués). C'est la référence pour évaluer si un équipement est conforme IEC 62443.

### 2.3 Relation entre les parties

```
Asset Owner / Opérateur          Intégrateur Système          Fabricant de composants
        │                               │                              │
   IEC 62443-2-1                  IEC 62443-2-4                IEC 62443-4-1
   (CSMS – politique)           (exigences prestataires)      (SDL – dev. sécurisé)
        │                               │                              │
   IEC 62443-3-2                  IEC 62443-3-3                IEC 62443-4-2
   (risk assessment)             (exigences système)          (exigences composants)
        │                               │                              │
        └───────────────────────────────┴──────────────────────────────┘
                                        │
                               IEC 62443-1-1
                          (terminologie commune)
```

---

## 3. Concepts fondamentaux

### 3.1 IACS — Industrial Automation and Control System

Ensemble des équipements, réseaux, logiciels et personnes impliqués dans le contrôle automatisé des processus industriels. L'IACS inclut non seulement les automates et les capteurs, mais aussi les logiciels de supervision, les réseaux de communication, les opérateurs et les procédures d'exploitation.

### 3.2 Le modèle Zone / Conduit

Le concept de **zone** et **conduit** est l'apport architectural le plus important d'IEC 62443.

#### Zone (Security Zone)
> *"Regroupement d'actifs physiques ou logiques qui partagent des exigences de sécurité communes."* — IEC 62443-1-1

Une zone regroupe des équipements ayant :
- Le même niveau de criticité
- Les mêmes politiques d'accès
- Les mêmes exigences de disponibilité

**Règles de définition d'une zone :**
1. Tous les actifs d'une zone partagent le même niveau de sécurité cible (SL-T)
2. Une zone doit avoir une frontière clairement définie
3. Chaque zone doit avoir un responsable (zone owner)
4. Les communications entre zones passent obligatoirement par un conduit

**Exemples de zones typiques :**

| Zone | Contenu typique | SL cible typique |
|------|----------------|-----------------|
| Zone Entreprise (IT) | ERP, messagerie, postes bureautiques | SL-1 |
| Zone DMZ industrielle | Serveurs d'historisation, passerelles, proxies | SL-1 à SL-2 |
| Zone Supervision | SCADA, HMI, MES, serveurs de données OT | SL-2 |
| Zone Contrôle | PLC, DCS, variateurs, actionneurs | SL-2 à SL-3 |
| Zone Terrain | Capteurs, transmetteurs, actionneurs simples | SL-1 |
| Zone Sécurité (SIS) | Systèmes de sécurité instrumentée (ESD) | SL-3 à SL-4 |
| Zone Maintenance | Accès temporaire fournisseurs, laptops maintenance | SL-2 |

#### Conduit (Communication Channel / Conduit)
> *"Regroupement logique de ressources de communication qui partagent les mêmes exigences de sécurité et protègent les assets des zones qu'il relie."* — IEC 62443-1-1

Un conduit est le canal de communication **contrôlé** entre deux zones. Tout flux entre deux zones doit passer par un conduit explicitement défini et sécurisé.

**Caractéristiques d'un conduit :**
- Filtrage du trafic (firewall, liste blanche)
- Authentification des extrémités (si applicable)
- Chiffrement du canal (selon le SL requis)
- Journalisation des échanges
- Niveau de sécurité propre (pouvant différer des zones qu'il relie)

**Types de conduits :**
- Conduit réseau (firewall OT, routeur filtrant)
- Conduit applicatif (passerelle de données, data diode)
- Conduit VPN (accès distants sécurisés)
- Conduit sans fil (réseau Wi-Fi industriel sécurisé)

### 3.3 Les niveaux de sécurité (Security Levels — SL)

IEC 62443 définit **4 niveaux de sécurité** progressifs, caractérisant la résistance d'un système ou composant face à des attaquants de niveau de sophistication croissant.

| Niveau | Intitulé | Profil de l'attaquant | Description |
|--------|----------|----------------------|-------------|
| **SL-1** | Protection contre les violations non intentionnelles | Utilisateur interne maladroit, erreur de manipulation | Mesures de base : authentification simple, journalisation, mises à jour. |
| **SL-2** | Protection contre les attaquants intentionnels avec moyens simples | Script kiddie, employé malveillant peu technique | Authentification forte, segmentation réseau, chiffrement basique, IDS. |
| **SL-3** | Protection contre les attaquants sophistiqués avec moyens importants | Groupe cybercriminel, concurrent hostile, hacktiviste avancé | Auth multifacteur, chiffrement fort, tests d'intrusion réguliers, supervision avancée. |
| **SL-4** | Protection contre des attaques étatiques | Service de renseignement, acteur étatique hostile | Niveau militaire / infrastructures critiques nationales. Data diodes, air gap, audit permanent. |

**Note importante :** La majorité des installations industrielles cible **SL-2** comme niveau de protection raisonnable. SL-3 est recommandé pour les infrastructures critiques. SL-4 est réservé aux systèmes de défense nationale et aux infrastructures vitales stratégiques.

#### Distinction SL-T / SL-A / SL-C

| Notation | Nom | Définition |
|----------|-----|------------|
| **SL-T** | Target Security Level | Niveau de sécurité **cible** défini par l'analyse de risques pour une zone |
| **SL-A** | Achieved Security Level | Niveau de sécurité **effectivement atteint** après mise en œuvre des mesures |
| **SL-C** | Capability Security Level | Niveau de sécurité **capable** d'être atteint par un produit (selon 62443-4-2) |

L'objectif est que `SL-A ≥ SL-T` pour chaque zone. L'écart `SL-T − SL-A` représente le risque résiduel à traiter.

### 3.4 Le modèle de référence IACS

IEC 62443-3-2 s'appuie sur le **modèle de Purdue** (Purdue Enterprise Reference Architecture — PERA) pour structurer les niveaux fonctionnels d'un système industriel :

```
Niveau 4 — Réseau d'entreprise (IT)
           ERP, messagerie, BI, RH
              │
           ═══════ Frontière IT/OT ═══════
              │
Niveau 3 — Réseau de supervision usine
           MES, historisation, planification production
              │
Niveau 2 — Réseau de contrôle
           SCADA, HMI, serveurs de données OT
              │
Niveau 1 — Réseau de contrôle des processus
           PLC, DCS, contrôleurs
              │
Niveau 0 — Terrain
           Capteurs, actionneurs, transmetteurs
```

La DMZ industrielle se positionne entre les niveaux 3 et 4 pour médiatiser les échanges IT/OT.

---

## 4. Modèle de maturité CSMS

### 4.1 Qu'est-ce que le CSMS ?

Le **CSMS** (Cybersecurity Management System) est l'ensemble des politiques, procédures, pratiques et ressources qu'un asset owner met en place pour gérer la cybersécurité de ses IACS de façon continue et structurée.

IEC 62443-2-1 définit les éléments obligatoires d'un CSMS. Il n'est pas certifiant en lui-même, mais constitue la base organisationnelle sur laquelle s'appuient les exigences techniques des séries 3 et 4.

### 4.2 Éléments du CSMS (IEC 62443-2-1)

**Élément 1 — Périmètre et planification**
- Définition du périmètre IACS couvert par le CSMS
- Inventaire et classification des actifs
- Analyse des risques initiale
- Définition des objectifs de sécurité

**Élément 2 — Évaluation et catégorisation des risques**
- Identification des menaces et vulnérabilités
- Évaluation de la vraisemblance et de l'impact
- Détermination des SL cibles par zone
- Priorisation des risques

**Élément 3 — Politiques et procédures de sécurité**
- Politique de sécurité IACS documentée et approuvée par la direction
- Procédures opérationnelles de sécurité
- Gestion des incidents
- Gestion des changements (MOC — Management of Change)

**Élément 4 — Mise en œuvre des mesures**
- Contrôles techniques (segmentation, IAM, chiffrement…)
- Contrôles organisationnels (formation, sensibilisation)
- Contrôles physiques (accès aux locaux, câblage)

**Élément 5 — Formation et compétences**
- Programme de formation cybersécurité OT
- Évaluation des compétences du personnel
- Formation spécifique pour les intervenants externes

**Élément 6 — Surveillance et amélioration continue**
- Surveillance continue des systèmes (SIEM, IDS)
- Audits internes réguliers
- Revue de direction annuelle
- Gestion des incidents et retour d'expérience
- Mise à jour de l'analyse de risques

### 4.3 Niveaux de maturité du CSMS

Bien qu'IEC 62443 ne définisse pas formellement un modèle de maturité à proprement parler, la pratique industrielle utilise une échelle en 4 niveaux inspirée du CMMI :

| Niveau | Nom | Description |
|--------|-----|-------------|
| **Niveau 0** | Inexistant | Aucune démarche de cybersécurité OT. Pas d'inventaire, pas de politique. |
| **Niveau 1** | Initial | Actions ponctuelles et réactives. Pas de processus formalisés. |
| **Niveau 2** | Défini | Politiques et procédures documentées. Mise en œuvre partielle et non cohérente. |
| **Niveau 3** | Géré | Processus mis en œuvre et mesurés. Surveillance continue. Revue régulière. |
| **Niveau 4** | Optimisé | Amélioration continue proactive. CSMS intégré dans le management global. |

---

## 5. Zones, conduits et niveaux de sécurité (SL)

### 5.1 Processus de définition des zones (IEC 62443-3-2)

La définition des zones n'est pas arbitraire. IEC 62443-3-2 définit un processus en 6 étapes :

**Étape 1 — Inventaire des actifs**
Identifier exhaustivement tous les composants de l'IACS : matériel, logiciel, réseau, données, personnes, processus.

**Étape 2 — Regroupement initial**
Proposer un découpage en zones selon les critères : criticité fonctionnelle, localisation physique, profil de menace, niveau de confiance requis.

**Étape 3 — Analyse des risques par zone**
Pour chaque zone candidate, évaluer les risques associés à partir des menaces identifiées.

**Étape 4 — Détermination des SL cibles**
À partir de l'analyse de risques, définir le SL-T requis pour chaque zone.

**Étape 5 — Définition des conduits**
Pour chaque flux de communication entre zones, définir le conduit associé et ses exigences de sécurité.

**Étape 6 — Validation et documentation**
Documenter l'architecture de zones/conduits, la faire valider par les parties prenantes (production, IT, sécurité, direction).

### 5.2 Exigences de sécurité par niveau SL — Vue synthétique

#### SL-1 — Exigences minimales

| Domaine | Mesure obligatoire |
|---------|-------------------|
| Authentification | Mot de passe unique par utilisateur (pas de comptes partagés) |
| Accès | Contrôle d'accès physique aux équipements critiques |
| Réseau | Aucune connexion directe Internet vers les zones OT |
| Journalisation | Logs des accès aux systèmes critiques |
| Mise à jour | Processus documenté de gestion des patches |
| Sauvegarde | Sauvegarde régulière des configurations et programmes |
| Sensibilisation | Formation de base à la cybersécurité pour le personnel OT |

#### SL-2 — Protection contre les attaquants intentionnels simples

| Domaine | Mesure obligatoire |
|---------|-------------------|
| Authentification | Authentification multifacteur pour les accès à distance |
| Réseau | Segmentation IT/OT avec firewall dédié |
| Réseau | DMZ industrielle pour les échanges IT/OT |
| Chiffrement | Chiffrement des communications à distance (VPN) |
| Détection | IDS/IPS ou surveillance du trafic réseau OT |
| Accès fournisseurs | Bastion / PAM pour les accès de maintenance |
| Gestion des comptes | Revue trimestrielle des habilitations |
| Vulnérabilités | Scan de vulnérabilités régulier |

#### SL-3 — Protection contre les attaquants sophistiqués

| Domaine | Mesure obligatoire |
|---------|-------------------|
| Authentification | MFA pour tous les accès humains, y compris locaux |
| Protocoles | Chiffrement des communications OT (TLS, OPC-UA sécurisé) |
| Tests | Tests d'intrusion annuels par un tiers |
| Détection | SIEM avec corrélation IT+OT et SOC opérationnel |
| Intégrité | Contrôle d'intégrité des firmwares et programmes PLC |
| Isolation | Micro-segmentation des zones critiques |
| Approvisionnement | Vérification de la sécurité de la chaîne d'approvisionnement |

#### SL-4 — Protection contre les acteurs étatiques

| Domaine | Mesure obligatoire |
|---------|-------------------|
| Isolation | Air gap physique ou data diodes unidirectionnelles |
| Authentification | Authentification cryptographique forte (PKI, HSM) |
| Surveillance | Surveillance 24/7 par SOC dédié |
| Personnel | Habilitation et contrôle d'antécédents du personnel |
| Tests | Red team exercises permanents |
| Redondance | Redondance totale des systèmes critiques |

### 5.3 Exemple d'architecture zonée conforme IEC 62443

```
┌─────────────────────────────────────────────────────────────────┐
│  ZONE ENTREPRISE (IT) — SL-1                                   │
│  ERP · Messagerie · Bureautique · Reporting                     │
└────────────────────┬────────────────────────────────────────────┘
                     │
              [CONDUIT IT/OT]
         Firewall périmétrique + IPS
                     │
┌─────────────────────────────────────────────────────────────────┐
│  ZONE DMZ INDUSTRIELLE — SL-2                                  │
│  Serveur d'historisation · Passerelle · Proxy applicatif        │
│  Serveur de sauvegarde · Bastion accès fournisseurs             │
└────────────────────┬────────────────────────────────────────────┘
                     │
           [CONDUIT DMZ/SUPERVISION]
          Firewall OT DPI (Modbus, S7comm)
                     │
┌─────────────────────────────────────────────────────────────────┐
│  ZONE SUPERVISION — SL-2                                       │
│  SCADA · HMI · MES · Serveurs de données OT                    │
└────────────────────┬────────────────────────────────────────────┘
                     │
           [CONDUIT SUPERVISION/CONTRÔLE]
         Firewall OT + whitelist protocoles
                     │
        ┌────────────┴────────────┐
        │                        │
┌───────┴────────┐    ┌──────────┴─────────┐
│  ZONE CONTRÔLE │    │  ZONE SÉCURITÉ SIS │
│  SL-2          │    │  SL-3              │
│  PLC · DCS     │    │  Contrôleurs SIS   │
│  Variateurs    │    │  (isolation forte) │
└───────┬────────┘    └────────────────────┘
        │
┌───────┴────────────────────────────────────┐
│  ZONE TERRAIN — SL-1                       │
│  Capteurs · Actionneurs · Transmetteurs    │
└────────────────────────────────────────────┘
```

---

## 6. Les 7 familles d'exigences fondamentales (FR)

IEC 62443-3-3 organise toutes les exigences de sécurité en **7 Fundamental Requirements (FR)**. Chaque FR regroupe plusieurs System Requirements (SR) déclinés sur les 4 niveaux SL.

### FR 1 — Identification et authentification (IAC)
**Identification and Authentication Control**

> Assurer que tous les utilisateurs (humains et machines) accédant à l'IACS sont correctement identifiés et authentifiés avant tout accès.

**Périmètre :** Utilisateurs humains, processus logiciels, équipements, connexions réseau.

**Sous-exigences notables (SR) :**
- SR 1.1 : Authentification des utilisateurs humains
- SR 1.2 : Authentification des processus logiciels et équipements
- SR 1.3 : Gestion des comptes
- SR 1.4 : Identifiants uniques
- SR 1.5 : Authentification avec authenticateurs (mots de passe, certificats, tokens)
- SR 1.6 : Authenticateurs sans fil
- SR 1.7 : Sécurité des mots de passe
- SR 1.8 : Infrastructure à clé publique (PKI)
- SR 1.9 : Authenticateurs physiques (badges, tokens)
- SR 1.10 : Tentatives d'authentification échouées
- SR 1.11 : Session d'authentification (timeout, verrouillage)
- SR 1.12 : Accès distant (remote access)
- SR 1.13 : Accès par des tiers (vendors, maintenance)

### FR 2 — Contrôle d'utilisation (UC)
**Use Control**

> S'assurer que les droits d'accès sont accordés selon le principe du moindre privilège et que leur utilisation est contrôlée et auditée.

**Sous-exigences notables :**
- SR 2.1 : Autorisation (gestion des habilitations)
- SR 2.2 : Authentification par liaison sans fil
- SR 2.3 : Utilisation des appareils mobiles
- SR 2.4 : Responsabilité des utilisateurs
- SR 2.5 : Gestion des sessions (timeout)
- SR 2.6 : Accès distant (contrôle de session)
- SR 2.7 : Contrôle des entrées (interfaces physiques USB, SD…)
- SR 2.8 : Audit des événements liés à la sécurité
- SR 2.9 : Capacité d'audit (suffisamment de stockage pour les logs)
- SR 2.10 : Réponse aux violations d'audit
- SR 2.11 : Timestamps (horloge synchronisée NTP)
- SR 2.12 : Gestion des rôles et séparation des tâches

### FR 3 — Intégrité du système (SI)
**System Integrity**

> Garantir l'intégrité du système IACS en empêchant les modifications non autorisées des ressources (logiciels, firmwares, données, configurations).

**Sous-exigences notables :**
- SR 3.1 : Communication integrity (protection contre les modifications de trafic)
- SR 3.2 : Protection contre les codes malveillants (antimalware)
- SR 3.3 : Mécanismes de vérification de la sécurité (security patching)
- SR 3.4 : Vérification du logiciel et des informations
- SR 3.5 : Vérification de l'intégrité des entrées
- SR 3.6 : Sortie de déterminisme (output determinism)
- SR 3.7 : Gestion des erreurs (error handling)
- SR 3.8 : Intégrité des sessions
- SR 3.9 : Protection des fonctions de sécurité

### FR 4 — Confidentialité des données (DC)
**Data Confidentiality**

> Protéger la confidentialité des informations en transit ou stockées dans le système IACS contre les accès non autorisés.

**Sous-exigences notables :**
- SR 4.1 : Confidentialité des informations (classification et protection)
- SR 4.2 : Persistance des informations (protection après effacement)
- SR 4.3 : Cryptographie (chiffrement des données sensibles)

### FR 5 — Flux de données restreint (RDF)
**Restricted Data Flow**

> Contrôler et restreindre les flux d'information entre les différentes zones de l'IACS en implémentant des frontières de réseau et des mécanismes de contrôle des communications.

**Sous-exigences notables :**
- SR 5.1 : Segmentation du réseau (zones et conduits)
- SR 5.2 : Zones de protection (protection contre les attaques réseau)
- SR 5.3 : Communications sans fil générales
- SR 5.4 : Communication de données des applications (contrôle des applications)

### FR 6 — Réponse aux événements en temps opportun (TRE)
**Timely Response to Events**

> Détecter, enregistrer, signaler et répondre aux incidents de sécurité en temps opportun.

**Sous-exigences notables :**
- SR 6.1 : Détection des événements liés à la sécurité
- SR 6.2 : Surveillance continue des communications (IDS, monitoring)

### FR 7 — Disponibilité des ressources (RA)
**Resource Availability**

> Assurer la disponibilité de l'IACS face aux conditions dégradées, incluant les attaques par déni de service, les pannes et les catastrophes.

**Sous-exigences notables :**
- SR 7.1 : Protection contre les attaques DoS
- SR 7.2 : Gestion de la capacité des ressources
- SR 7.3 : Continuité des fonctions de contrôle
- SR 7.4 : Contrôle de l'environnement (température, humidité)
- SR 7.5 : Sauvegarde et restauration des données
- SR 7.6 : Gestion des réponses aux urgences
- SR 7.7 : Contrôle du mode d'urgence

---

## 7. Exigences par niveau SL — détail FR1 à FR7

Le tableau suivant résume les **51 exigences système (SR)** de la norme 62443-3-3 et leur applicabilité par niveau de sécurité. RE = Requirement Enhancement (renforcement).

### 7.1 FR 1 — Identification et authentification

| SR | Description | SL-1 | SL-2 | SL-3 | SL-4 |
|----|-------------|:----:|:----:|:----:|:----:|
| 1.1 | Auth. utilisateurs humains | ✓ base | + RE1 (méc. unique) | + RE2 (MFA) | + RE3 (MFA physique) |
| 1.2 | Auth. logiciels et devices | ✓ | + RE1 (PKI) | + RE2 (mutuelle) | + RE3 |
| 1.3 | Gestion des comptes | ✓ | + RE1 (audit) | + RE2 (dynamisque) | + RE3 |
| 1.4 | Identifiants uniques | ✓ | ✓ | ✓ | ✓ |
| 1.5 | Gestion des authentifiants | ✓ | + RE1 (complexité) | + RE2 (durée courte) | + RE3 |
| 1.6 | Auth. sans fil | ✓ | + RE1 | + RE2 | + RE3 |
| 1.7 | Durée de force des mots de passe | ✓ | + RE1 | ✓ | ✓ |
| 1.8 | PKI | — | ✓ | + RE1 | + RE2 |
| 1.9 | Auth. physiques | ✓ | + RE1 | + RE2 | + RE3 |
| 1.10 | Tentatives échouées | ✓ | ✓ | ✓ | ✓ |
| 1.11 | Durée de session | ✓ | + RE1 | ✓ | ✓ |
| 1.12 | Accès distant | ✓ | + RE1 (MFA) | + RE2 (monitoring) | + RE3 |
| 1.13 | Accès tiers | ✓ | + RE1 | ✓ | ✓ |

### 7.2 FR 2 — Contrôle d'utilisation

| SR | Description | SL-1 | SL-2 | SL-3 | SL-4 |
|----|-------------|:----:|:----:|:----:|:----:|
| 2.1 | Autorisation et moindre privilège | ✓ | + RE1 (audit access) | + RE2 | + RE3 |
| 2.2 | Auth. sans fil | — | ✓ | ✓ | ✓ |
| 2.3 | Dispositifs mobiles | ✓ | + RE1 | + RE2 | + RE3 |
| 2.4 | Traçabilité utilisateurs | ✓ | + RE1 | ✓ | ✓ |
| 2.5 | Verrouillage de session | ✓ | ✓ | ✓ | ✓ |
| 2.6 | Accès distant — contrôle | ✓ | + RE1 | + RE2 | + RE3 |
| 2.7 | Périphériques externes (USB) | ✓ | + RE1 | + RE2 | ✓ |
| 2.8 | Journalisation événements sécurité | ✓ | + RE1 | + RE2 | + RE3 |
| 2.9 | Capacité d'audit | ✓ | ✓ | ✓ | ✓ |
| 2.10 | Réponse aux alertes d'audit | ✓ | ✓ | ✓ | ✓ |
| 2.11 | Timestamps | ✓ | ✓ | ✓ | ✓ |
| 2.12 | Séparation des tâches | — | ✓ | + RE1 | + RE2 |

### 7.3 FR 3 — Intégrité du système

| SR | Description | SL-1 | SL-2 | SL-3 | SL-4 |
|----|-------------|:----:|:----:|:----:|:----:|
| 3.1 | Intégrité des communications | ✓ | + RE1 (CRC/hash) | + RE2 (crypto) | + RE3 |
| 3.2 | Protection contre malwares | ✓ | + RE1 (heuristique) | + RE2 (monitoring) | + RE3 |
| 3.3 | Correctifs de sécurité | ✓ | + RE1 (délai) | + RE2 (auto-patch) | + RE3 |
| 3.4 | Vérification logicielle | ✓ | + RE1 | + RE2 | + RE3 |
| 3.5 | Validation des entrées | ✓ | ✓ | ✓ | ✓ |
| 3.6 | Déterminisme des sorties | ✓ | ✓ | ✓ | ✓ |
| 3.7 | Gestion des erreurs | ✓ | ✓ | ✓ | ✓ |
| 3.8 | Intégrité des sessions | — | ✓ | + RE1 | + RE2 |
| 3.9 | Protection des fonctions sécurité | ✓ | + RE1 | + RE2 | + RE3 |

### 7.4 FR 4 — Confidentialité

| SR | Description | SL-1 | SL-2 | SL-3 | SL-4 |
|----|-------------|:----:|:----:|:----:|:----:|
| 4.1 | Classification et protection des données | ✓ | + RE1 | + RE2 | + RE3 |
| 4.2 | Persistance des informations | — | ✓ | + RE1 | + RE2 |
| 4.3 | Chiffrement | — | ✓ | + RE1 (AES-256) | + RE2 |

### 7.5 FR 5 — Flux de données restreint

| SR | Description | SL-1 | SL-2 | SL-3 | SL-4 |
|----|-------------|:----:|:----:|:----:|:----:|
| 5.1 | Segmentation réseau | ✓ | + RE1 (zones formelles) | + RE2 (micro-seg.) | + RE3 |
| 5.2 | Zones de protection | ✓ | + RE1 (DPI) | + RE2 | + RE3 |
| 5.3 | Communications sans fil | ✓ | + RE1 | + RE2 | + RE3 |
| 5.4 | Contrôle applicatif | ✓ | + RE1 | + RE2 | + RE3 |

### 7.6 FR 6 — Réponse aux événements

| SR | Description | SL-1 | SL-2 | SL-3 | SL-4 |
|----|-------------|:----:|:----:|:----:|:----:|
| 6.1 | Détection des événements sécurité | ✓ | + RE1 (alerte auto) | + RE2 (IDS continu) | + RE3 (SOC) |
| 6.2 | Surveillance continue | — | ✓ | + RE1 (corrélation) | + RE2 (temps réel) |

### 7.7 FR 7 — Disponibilité

| SR | Description | SL-1 | SL-2 | SL-3 | SL-4 |
|----|-------------|:----:|:----:|:----:|:----:|
| 7.1 | Protection DoS | ✓ | + RE1 (limitation) | + RE2 (détection) | + RE3 |
| 7.2 | Gestion des ressources | ✓ | ✓ | ✓ | ✓ |
| 7.3 | Continuité des fonctions | ✓ | + RE1 | + RE2 (auto-failover) | + RE3 |
| 7.4 | Contrôle environnemental | ✓ | ✓ | ✓ | ✓ |
| 7.5 | Sauvegarde et restauration | ✓ | + RE1 (testée) | + RE2 (RPO/RTO) | + RE3 |
| 7.6 | Réponse aux urgences | ✓ | + RE1 | + RE2 | + RE3 |
| 7.7 | Mode d'urgence | ✓ | ✓ | ✓ | ✓ |

---

## 8. Rôles et responsabilités

### 8.1 Les trois rôles fondamentaux

IEC 62443 distingue trois rôles avec des obligations distinctes :

#### Asset Owner (Propriétaire / Opérateur)
L'organisation qui exploite l'IACS (l'industriel).

**Responsabilités selon IEC 62443-2-1 :**
- Définir et maintenir le CSMS
- Réaliser l'analyse de risques et définir les SL cibles
- Définir les zones et conduits
- Sélectionner et déployer les mesures de sécurité
- Gérer les incidents de sécurité
- Assurer la formation du personnel
- Surveiller et améliorer en continu

**Responsabilités selon IEC 62443-3-2 :**
- Documenter l'architecture de zones/conduits
- Vérifier que le SL atteint (SL-A) ≥ SL cible (SL-T)
- Mettre à jour l'analyse de risques à chaque changement majeur

#### System Integrator (Intégrateur système)
L'organisation qui conçoit et déploie les systèmes IACS (ESN, intégrateur, maîtrise d'œuvre).

**Responsabilités selon IEC 62443-2-4 :**
- Concevoir les architectures de sécurité conformes aux SL définis
- Sélectionner des composants conformes IEC 62443-4-2
- Réaliser les tests de sécurité avant livraison
- Documenter la sécurité de la solution (dossier de sécurité)
- Former l'asset owner à l'exploitation sécurisée
- Gérer sa propre chaîne d'approvisionnement de manière sécurisée

#### Product Supplier (Fabricant de composants)
L'organisation qui fabrique les équipements (Siemens, Rockwell, Schneider, Emerson…).

**Responsabilités selon IEC 62443-4-1 :**
- Intégrer la sécurité dès la conception (Security by Design)
- Publier les correctifs de sécurité en temps opportun
- Documenter les vulnérabilités connues
- Fournir des guides de durcissement (hardening guides)
- Notifier les clients en cas de CVE critiques

**Responsabilités selon IEC 62443-4-2 :**
- Déclarer le SL-C (Capability Security Level) de leurs produits
- Fournir les preuves de conformité aux SR applicables

### 8.2 Matrice de responsabilité RACI

| Activité | Asset Owner | Intégrateur | Fabricant |
|----------|:-----------:|:-----------:|:---------:|
| Définir le périmètre IACS | **R** | C | — |
| Réaliser l'analyse de risques | **R** | A | — |
| Définir les SL cibles | **R** | C | — |
| Concevoir l'architecture de sécurité | A | **R** | C |
| Choisir les composants | A | **R** | C |
| Déclarer la conformité composant (SL-C) | — | I | **R** |
| Déployer les mesures | C | **R** | — |
| Tester la sécurité du système | A | **R** | C |
| Gérer les patches du système | **R** | C | — |
| Publier les patches du composant | — | — | **R** |
| Gérer les incidents opérationnels | **R** | C | — |
| Former le personnel | **R** | A | — |

*R=Responsible, A=Accountable, C=Consulted, I=Informed*

---

## 9. Processus d'évaluation des risques (Risk Assessment)

### 9.1 Méthode IEC 62443-3-2

La norme 62443-3-2 définit une méthode d'évaluation des risques adaptée aux IACS. Elle n'impose pas une méthode unique mais requiert que la méthode retenue couvre les éléments suivants :

**Étape 1 — Établir le contexte**
- Définir le périmètre d'évaluation
- Identifier les objectifs de sécurité (intégrité du processus, sûreté des personnes, continuité de production)
- Identifier les parties prenantes et leur tolérance au risque

**Étape 2 — Identification des actifs**
- Inventaire exhaustif des composants IACS
- Identification des fonctions critiques (processus, données, communications)
- Classification selon la criticité

**Étape 3 — Identification des menaces**
- Catalogue des menaces spécifiques à l'OT industriel
- Sources de menaces : internes (opérateurs, maintenance), externes (cybercriminels, concurrents, États), environnementales (pannes, catastrophes)
- Scénarios d'attaque pertinents (kill chain)

**Étape 4 — Identification des vulnérabilités**
- Audit de l'architecture existante
- Scan de vulnérabilités (Nmap, Tenable OT, Claroty)
- Analyse des CVE sur les composants inventoriés

**Étape 5 — Évaluation des risques**
Pour chaque combinaison menace × vulnérabilité × actif :

```
Risque = Vraisemblance × Impact

Vraisemblance : 1 (Très rare) → 4 (Très probable)
Impact        : 1 (Négligeable) → 4 (Catastrophique)
Criticité     : 1–4 (Acceptable) / 5–9 (À surveiller) / 10–16 (Inacceptable)
```

**Étape 6 — Détermination des SL cibles**
À partir de l'évaluation des risques, déterminer le SL-T requis pour chaque zone :
- Risques inacceptables → SL-T élevé (SL-3 ou SL-4)
- Risques à surveiller → SL-T moyen (SL-2)
- Risques acceptables → SL-T minimal (SL-1)

**Étape 7 — Traitement des risques**
- Accepter (si risque résiduel acceptable)
- Éviter (supprimer la connexion, l'équipement)
- Transférer (assurance, sous-traitance)
- Réduire (mesures techniques et organisationnelles)

### 9.2 Tableau de risques OT typiques

| Scénario | Actif | Probabilité | Impact | Criticité | SL-T suggéré |
|----------|-------|:-----------:|:------:|:---------:|:------------:|
| Ransomware via RDP exposé | SCADA | 4 | 4 | 16 | SL-3 |
| Modification programme PLC (Modbus sans auth) | PLC | 3 | 4 | 12 | SL-2/3 |
| Compromission compte fournisseur VPN | Réseau OT | 3 | 3 | 9 | SL-2 |
| Windows EOS exploité (HMI) | HMI | 3 | 3 | 9 | SL-2 |
| Attaque DoS sur réseau OT | Tous | 2 | 4 | 8 | SL-2 |
| Espionnage industriel (écoute réseau) | Données | 2 | 3 | 6 | SL-2 |
| Erreur de manipulation opérateur | Automates | 3 | 2 | 6 | SL-1 |
| Panne physique d'un PLC | Ligne prod. | 2 | 3 | 6 | SL-1 |

### 9.3 Lien avec EBIOS Risk Manager

La méthode française EBIOS Risk Manager (ANSSI, 2018) est compatible et complémentaire avec IEC 62443-3-2 :

| EBIOS RM | IEC 62443-3-2 | Correspondance |
|----------|---------------|----------------|
| Périmètre et objectifs | Établir le contexte | Directe |
| Sources de risque | Identification des menaces | Directe |
| Scénarios stratégiques | Scénarios d'attaque | Directe |
| Scénarios opérationnels | Analyse des vulnérabilités | Directe |
| Traitement du risque | Traitement des risques | Directe |
| Tableau de risques | Évaluation des risques | Directe |

---

## 10. Relation avec les autres normes

### 10.1 IEC 62443 vs ISO/IEC 27001

| Critère | IEC 62443 | ISO/IEC 27001 |
|---------|-----------|---------------|
| **Domaine** | Cybersécurité IACS (OT) | SMSI pour toute organisation (IT) |
| **Périmètre** | Systèmes industriels uniquement | Tout système d'information |
| **Approche** | Technique (zones, SL, FR/SR) + organisationnelle | Organisationnelle + processus (Annexe A) |
| **Certifiabilité** | Oui (composant, système, processus) | Oui (organisation) |
| **Contraintes OT** | Intégrées nativement | Non prises en compte |
| **Compatibilité** | Complémentaire avec ISO 27001 | Complémentaire avec IEC 62443 |

**Bonne pratique :** Un industriel peut certifier son SMSI selon ISO 27001 (pour le périmètre IT) et sa sécurité OT selon IEC 62443 (pour le périmètre IACS). Les deux démarches se renforcent mutuellement.

### 10.2 IEC 62443 vs NIST Cybersecurity Framework

| Fonction NIST CSF | Correspondance IEC 62443 |
|------------------|------------------------|
| **IDENTIFY** | IEC 62443-3-2 (risk assessment) + 2-1 (inventaire) |
| **PROTECT** | IEC 62443-3-3 FR1, FR2, FR3, FR4, FR5 |
| **DETECT** | IEC 62443-3-3 FR6 |
| **RESPOND** | IEC 62443-2-1 (gestion des incidents) |
| **RECOVER** | IEC 62443-3-3 FR7 + 2-1 (continuité) |

Le NIST CSF offre un cadre de pilotage et de communication, IEC 62443 fournit les exigences techniques et organisationnelles détaillées.

### 10.3 IEC 62443 vs NIST SP 800-82

Le NIST SP 800-82 (Guide to ICS Security) est le pendant américain d'IEC 62443. Moins prescriptif, il fournit des recommandations et bonnes pratiques pour les systèmes de contrôle industriel. IEC 62443 est plus structuré et certifiable. Les deux documents se complètent ; IEC 62443 est le standard international de référence reconnu.

### 10.4 IEC 62443 et la directive NIS2

La directive européenne NIS2 (Network and Information Security 2, 2022/2555) est entrée en application en octobre 2024. Elle impose des obligations de cybersécurité aux entités essentielles et importantes.

**Lien avec IEC 62443 :**
- NIS2 n'impose pas explicitement IEC 62443 mais la reconnaît comme standard approprié pour les secteurs industriels
- Les mesures NIS2 (Art. 21) sont largement couvertes par IEC 62443-2-1 et 3-3
- La Commission européenne travaille à la création de schémas de certification basés sur IEC 62443

**Obligations NIS2 couvertes par IEC 62443 :**

| Obligation NIS2 (Art. 21) | Partie IEC 62443 |
|--------------------------|-----------------|
| Politiques de sécurité | IEC 62443-2-1 |
| Gestion des incidents | IEC 62443-2-1 + FR6 |
| Continuité des activités | IEC 62443-3-3 FR7 |
| Sécurité chaîne approvisionnement | IEC 62443-2-4 |
| Authentification et contrôle d'accès | IEC 62443-3-3 FR1, FR2 |
| Chiffrement | IEC 62443-3-3 FR4 |

### 10.5 IEC 62443 et le Cyber Resilience Act (CRA)

Le CRA européen (2024) impose des exigences de cybersécurité aux fabricants de produits numériques connectés. Pour les composants IACS :
- **IEC 62443-4-1** (SDL) est directement aligné avec les obligations de développement sécurisé du CRA
- **IEC 62443-4-2** (SL-C des composants) correspond aux exigences de sécurité produit du CRA
- La conformité IEC 62443-4-1/4-2 sera probablement reconnue comme présomption de conformité au CRA pour les composants industriels

### 10.6 IEC 62443 et la sûreté fonctionnelle (IEC 61511 / IEC 61508)

La frontière entre **sécurité** (security — cybersécurité) et **sûreté** (safety — sécurité fonctionnelle) est critique en environnement industriel.

**IEC 61511** (Functional Safety for Process Industry) et **IEC 62443** sont complémentaires :
- Un cybersécurité insuffisant peut compromettre la sûreté fonctionnelle (ex : manipulation des SIS via réseau)
- Triton/TRISIS (2017) est le premier malware connu ayant ciblé les SIS dans le but de désactiver les protections de sûreté
- IEC 62443 recommande d'appliquer des SL élevés (SL-3/4) aux systèmes SIS pour protéger leur intégrité

---

## 11. Mise en œuvre pratique

### 11.1 Démarche de mise en conformité recommandée

#### Phase 0 — Cadrage et gouvernance (1–2 mois)
- Nommer un responsable cybersécurité OT (RSSI ou coordinateur)
- Définir le périmètre IACS à sécuriser
- Engager la direction (budget, politique de sécurité)
- Sélectionner la méthode d'évaluation des risques

#### Phase 1 — Inventaire et diagnostic (2–3 mois)
- Réaliser l'inventaire exhaustif des actifs IACS (CMDB OT)
- Identifier les versions de firmware, OS, applicatifs
- Cartographier les flux réseau (schéma de l'architecture existante)
- Audit de sécurité baseline (scan de vulnérabilités, revue de configuration)
- Évaluation du niveau de maturité CSMS actuel

#### Phase 2 — Analyse de risques (2–3 mois)
- Identifier les menaces pertinentes (catalogue de menaces OT)
- Évaluer les risques (matrice probabilité × impact)
- Définir les zones de sécurité et conduits
- Déterminer les SL cibles (SL-T) par zone
- Comparer SL-T avec le SL actuel (SL-A) → écarts = plan d'actions

#### Phase 3 — Définition et mise en œuvre des mesures (6–12 mois)
- Prioriser les mesures selon le risque résiduel
- **Actions immédiates (J+30) :** Quick wins — fermeture des accès non nécessaires, changement des mots de passe par défaut, segmentation réseau minimale
- **Court terme (J+90) :** Déploiement du firewall OT, bastion fournisseurs, MFA
- **Moyen terme (J+180) :** IDS OT, SIEM, mise à jour des firmwares, formation
- **Long terme (J+365) :** CSMS complet, tests d'intrusion, exercices de simulation

#### Phase 4 — Vérification et certification (2–3 mois)
- Vérification que le SL atteint (SL-A) ≥ SL cible (SL-T)
- Tests d'intrusion (pentest OT) par un tiers
- Audit tiers pour la certification (si requise)
- Documentation du dossier de sécurité

#### Phase 5 — Surveillance et amélioration continue (permanente)
- Supervision continue (SIEM, IDS OT)
- Revue annuelle de l'analyse de risques
- Gestion des incidents et retour d'expérience
- Mise à jour du CSMS en cas de changement majeur

### 11.2 Checklist rapide de conformité SL-1

Vérifications minimales pour atteindre SL-1 :

- [ ] Inventaire des actifs IACS documenté et maintenu à jour
- [ ] Aucun mot de passe constructeur par défaut sur les équipements
- [ ] Comptes utilisateurs nominatifs (pas de comptes partagés génériques)
- [ ] Accès physiques aux équipements critiques contrôlés
- [ ] Aucune connexion directe Internet → réseau OT
- [ ] Logs d'accès aux systèmes critiques activés et conservés
- [ ] Politique de sauvegardes documentée et testée (configs + programmes PLC)
- [ ] Processus de gestion des patches documenté (même si délai long)
- [ ] Formation de base à la cybersécurité pour le personnel OT
- [ ] Politique de sécurité IACS approuvée par la direction

### 11.3 Checklist supplémentaire pour SL-2

- [ ] Segmentation réseau IT/OT formelle (VLAN + firewall dédié)
- [ ] DMZ industrielle pour les échanges IT/OT
- [ ] Authentification multifacteur (MFA) pour les accès distants
- [ ] Bastion / PAM pour les accès fournisseurs et maintenance
- [ ] VPN chiffré (pas de RDP ou SSH direct depuis Internet)
- [ ] IDS OT en écoute passive sur le réseau de contrôle
- [ ] Revue trimestrielle des habilitations
- [ ] Scan de vulnérabilités semestriel
- [ ] Plan de réponse aux incidents OT documenté
- [ ] Exercice de simulation annuel (tabletop exercise)

### 11.4 Équipements et solutions du marché

#### Firewalls OT (Deep Packet Inspection des protocoles industriels)
| Produit | Fabricant | Protocoles supportés |
|---------|-----------|---------------------|
| FortiGate Rugged 70F | Fortinet | Modbus, DNP3, S7comm, IEC 104, PROFINET |
| PA-220R | Palo Alto Networks | Modbus, DNP3, OPC-DA, BACnet |
| Cisco IR1101 | Cisco | Modbus, DNP3, EtherNet/IP |
| Tofino Xenon | Belden | Modbus, S7comm, EtherNet/IP, OPC |

#### IDS OT (Détection d'intrusion industrielle)
| Produit | Fabricant | Points forts |
|---------|-----------|--------------|
| Claroty Platform | Claroty | Découverte passive, détection anomalies comportementales |
| Nozomi Networks Guardian | Nozomi | IA, compatibilité large protocoles OT |
| Dragos Platform | Dragos | Threat intelligence OT, ICS-specific TTPs |
| Tenable OT Security | Tenable | CVE OT, intégration SIEM, inventaire actifs |
| Microsoft Defender for IoT | Microsoft | Intégration Azure Sentinel, OT/IoT |

#### PAM / Bastion (Accès privilégiés)
| Produit | Fabricant | Points forts |
|---------|-----------|--------------|
| Wallix Bastion | Wallix | Français, certifié CSPN, sessions OT |
| CyberArk PAM | CyberArk | Leader marché IT, module OT |
| BeyondTrust Privilege | BeyondTrust | Remote support OT, enregistrement sessions |

#### SIEM (Gestion des logs et corrélation)
| Produit | Fabricant | Points forts |
|---------|-----------|--------------|
| Splunk Enterprise | Splunk | Corrélation IT+OT, connecteurs Claroty |
| IBM QRadar | IBM | SIEM mature, règles OT disponibles |
| Microsoft Sentinel | Microsoft | Cloud, intégration Defender for IoT |
| Elastic SIEM | Elastic | Open source, flexible |

---

## 12. Certification et conformité

### 12.1 Schémas de certification existants

IEC 62443 prévoit trois types de certification distincts, correspondant aux trois rôles de la norme :

#### Certification Composant (IEC 62443-4-2)
**Objet :** Certifier qu'un produit (automate, switch, logiciel) atteint un SL-C donné.

**Organismes certificateurs reconnus :**
- TÜV Rheinland (Allemagne)
- TÜV SÜD (Allemagne)
- Exida (États-Unis)
- DNV (Norvège)
- Bureau Veritas (France)
- SGS (Suisse)

**Processus :**
1. Dossier technique fourni par le fabricant (documentation sécurité, SDL)
2. Tests en laboratoire (tests d'intrusion, analyse de code)
3. Revue documentaire (conformité 62443-4-1 et 4-2)
4. Décision de certification + certificat SL-C

**Durée de validité :** 3 à 5 ans (re-certification périodique).

#### Certification Système (IEC 62443-3-3)
**Objet :** Certifier qu'un système IACS déployé atteint un SL donné pour chaque zone définie.

**Processus :**
1. Revue de l'analyse de risques et de la définition des zones/conduits
2. Vérification du déploiement des mesures (audit de configuration)
3. Tests d'intrusion en conditions réelles
4. Vérification que SL-A ≥ SL-T pour chaque zone
5. Certificat de conformité système

#### Certification Processus (IEC 62443-2-4 / 4-1)
**Objet :** Certifier que l'organisation (intégrateur ou fabricant) dispose des processus conformes.

- **IEC 62443-2-4** : certification des processus de l'intégrateur système
- **IEC 62443-4-1** : certification du cycle de développement sécurisé (SDL) du fabricant

### 12.2 Relation avec les certifications existantes

| Certification IEC 62443 | Équivalent ou complémentaire |
|------------------------|------------------------------|
| 62443-4-1 (SDL fabricant) | ISO/IEC 27034 (sécurité des applications) |
| 62443-2-1 (CSMS) | ISO/IEC 27001 (SMSI) |
| 62443-2-4 (prestataires) | ISO/IEC 27001 + ISO/IEC 20000 |
| Certification composant SL-C | Common Criteria (CSPN en France) |

### 12.3 Poids réglementaire et reconnaissance officielle

| Contexte | Statut IEC 62443 |
|----------|-----------------|
| Union européenne — Directive NIS2 | Standard reconnu (non obligatoire mais référence) |
| Union européenne — Cyber Resilience Act | Schéma de certification en cours de développement |
| France — ANSSI | Recommandé dans les guides sectoriels |
| Allemagne — BSI | Standard de référence pour les infrastructures critiques |
| États-Unis — CISA | Recommandé pour l'ICS (aux côtés de NIST SP 800-82) |
| Secteur Oil & Gas | Requis par de nombreux opérateurs majeurs (Total, Shell, BP) |
| Secteur aéronautique | Aligné avec les exigences DO-326A (cybersécurité avionique) |

---

## 13. Cas d'usage et exemples industriels

### 13.1 Stuxnet (2010) — L'absence de segmentation

**Contexte :** Attaque contre les centrifugeuses d'enrichissement d'uranium iraniennes (Natanz).

**Violation IEC 62443 :**
- FR 5 (RDF) : réseau de contrôle des centrifugeuses accessible depuis des réseaux non sécurisés via clé USB
- FR 3 (SI) : aucune vérification d'intégrité des programmes automates Siemens S7-315
- FR 1 (IAC) : accès aux automates sans authentification

**Leçon :** La segmentation physique et logique des zones contrôle est indispensable, y compris contre les vecteurs physiques (USB). SL-3 minimum requis pour les systèmes de cette criticité.

### 13.2 Triton / TRISIS (2017) — Attaque sur les SIS

**Contexte :** Attaque contre les SIS Triconex (Schneider Electric) d'une installation pétrolifère au Moyen-Orient (identifiée plus tard : SABIC, Arabie Saoudite).

**Violation IEC 62443 :**
- FR 5 (RDF) : absence de zone dédiée SIS isolée des réseaux IT/OT généraux
- FR 1 (IAC) : accès réseau direct aux contrôleurs SIS sans authentification forte
- FR 6 (TRE) : absence de détection des comportements anormaux sur les communications SIS

**Leçon :** Les SIS doivent être dans une zone à SL-3 minimum, physiquement isolée. Aucune communication non planifiée vers les SIS ne doit être possible.

### 13.3 Colonial Pipeline (2021) — Ransomware via accès VPN

**Contexte :** Ransomware DarkSide ayant paralysé le plus grand oléoduc des États-Unis. Vecteur : accès VPN sans MFA avec des identifiants compromis.

**Violation IEC 62443 :**
- FR 1 SR 1.12 (Accès distant) : VPN sans authentification multifacteur
- FR 2 SR 2.4 (Traçabilité) : absence de surveillance des sessions VPN
- FR 6 (TRE) : détection tardive du mouvement latéral

**Leçon :** Tout accès distant à un réseau OT doit être protégé par MFA. La traçabilité des sessions est obligatoire (IEC 62443 SR 2.4).

### 13.4 EKANS / Snake (2020) — Ransomware OT ciblé

**Contexte :** Ransomware visant spécifiquement les systèmes industriels. A affecté Honda, Enel, Fresenius. Embarque une liste de ~64 processus industriels à terminer avant chiffrement.

**Violation IEC 62443 :**
- FR 5 (RDF) : absence de segmentation permettant la propagation depuis l'IT vers l'OT
- FR 7 SR 7.5 (Sauvegarde) : absence de sauvegardes testées des configurations OT
- FR 3 SR 3.2 (Protection malware) : antivirus absent ou non mis à jour sur les postes OT

**Leçon :** La segmentation IT/OT est la mesure la plus efficace contre les ransomwares industriels. Les sauvegardes OT testées permettent un RTO acceptable.

### 13.5 Application pratique : mise en conformité d'une PME industrielle

**Profil :** PME de 150 personnes, secteur agroalimentaire, ligne de production automatisée avec 4 PLC Siemens S7-1200 et une supervision Wonderware.

**Étape 1 — Diagnostic initial :**
- Architecture réseau plate (IT/OT sur même switch)
- HMI sous Windows 7 EOS
- Accès fournisseurs via RDP direct sans MFA
- Aucun log OT
- Résultat : SL-A ≈ 0 pour toutes les zones

**SL cibles définis :**
- Zone Supervision (SCADA/HMI) : SL-T = 2
- Zone Contrôle (PLC) : SL-T = 2
- Zone Terrain (capteurs) : SL-T = 1

**Mesures déployées sur 6 mois :**

| Priorité | Mesure | FR couverte | Coût estimé |
|----------|--------|-------------|-------------|
| 1 | Firewall IT/OT (Fortinet 40F) + 3 VLAN | FR5 | 3 000 € |
| 1 | Changement MDP automates + désactivation services | FR1 | 0 € |
| 1 | Fermeture RDP + VPN avec MFA (OpenVPN+TOTP) | FR1 SR1.12 | 500 € |
| 2 | Migration HMI vers Windows 10 LTSC | FR3 | 4 000 € |
| 2 | Bastion Wallix pour fournisseurs (SaaS) | FR1 SR1.13 | 3 600 €/an |
| 2 | Sauvegardes PLC mensuelles testées | FR7 SR7.5 | 0 € (proc.) |
| 3 | Nozomi Vantage (IDS OT SaaS) | FR6 | 8 000 €/an |
| 3 | Splunk Free + collecteurs logs | FR6 SR6.2 | 0–5 000 € |

**Résultat après 6 mois :**
- Zone Supervision : SL-A ≈ 1.8 (objectif SL-T 2 partiellement atteint)
- Zone Contrôle : SL-A ≈ 2.0 ✓
- Zone Terrain : SL-A ≈ 1.0 ✓

---

## 14. Lexique complet IEC 62443

| Terme | Définition |
|-------|------------|
| **IACS** | Industrial Automation and Control System — Ensemble des équipements et systèmes utilisés pour automatiser les processus industriels. |
| **Asset Owner** | Propriétaire / opérateur de l'IACS. Responsable du CSMS et de la définition des zones/conduits. |
| **System Integrator** | Intégrateur système qui conçoit et déploie les solutions IACS. Soumis à IEC 62443-2-4. |
| **Product Supplier** | Fabricant de composants IACS. Soumis à IEC 62443-4-1 et 4-2. |
| **Zone** | Regroupement logique d'actifs partageant les mêmes exigences de sécurité. |
| **Conduit** | Canal de communication contrôlé entre deux zones, gérant les flux autorisés. |
| **SL (Security Level)** | Niveau de sécurité de 1 à 4 caractérisant la résistance aux attaques. |
| **SL-T** | Security Level Target — Niveau de sécurité cible défini par l'analyse de risques. |
| **SL-A** | Security Level Achieved — Niveau de sécurité effectivement atteint. |
| **SL-C** | Security Level Capability — Niveau de sécurité que peut atteindre un produit. |
| **FR (Fundamental Requirement)** | L'une des 7 familles d'exigences fondamentales de la norme 62443-3-3. |
| **SR (System Requirement)** | Exigence système spécifique au sein d'une FR, déclinée sur les 4 niveaux SL. |
| **RE (Requirement Enhancement)** | Renforcement d'une SR pour un niveau SL supérieur. |
| **CSMS** | Cybersecurity Management System — Système de management de la cybersécurité OT. |
| **IAC** | Identification and Authentication Control — FR1 d'IEC 62443-3-3. |
| **UC** | Use Control — FR2 d'IEC 62443-3-3. |
| **SI** | System Integrity — FR3 d'IEC 62443-3-3. |
| **DC** | Data Confidentiality — FR4 d'IEC 62443-3-3. |
| **RDF** | Restricted Data Flow — FR5 d'IEC 62443-3-3. |
| **TRE** | Timely Response to Events — FR6 d'IEC 62443-3-3. |
| **RA** | Resource Availability — FR7 d'IEC 62443-3-3. |
| **PERA** | Purdue Enterprise Reference Architecture — Modèle de référence en 5 niveaux (0 à 4). |
| **DMZ industrielle** | Zone de démilitarisation entre le réseau IT et le réseau OT, hébergeant les services d'échange. |
| **DPI** | Deep Packet Inspection — Analyse du contenu applicatif des paquets réseau par le firewall. |
| **SDL** | Secure Development Lifecycle — Cycle de développement sécurisé (IEC 62443-4-1). |
| **SIS** | Safety Instrumented System — Système de sécurité instrumentée (arrêt d'urgence, ESD). |
| **PLC / API** | Programmable Logic Controller / Automate Programmable Industriel. |
| **DCS** | Distributed Control System — Système de contrôle distribué. |
| **SCADA** | Supervisory Control and Data Acquisition — Supervision et acquisition de données. |
| **HMI** | Human-Machine Interface — Interface opérateur. |
| **MES** | Manufacturing Execution System — Système d'exécution de la fabrication. |
| **ERP** | Enterprise Resource Planning — Planification des ressources de l'entreprise. |
| **IIoT** | Industrial Internet of Things — Internet des objets industriels. |
| **OT** | Operational Technology — Technologies opérationnelles (automatismes, SCADA, PLC…). |
| **PAM** | Privileged Access Management — Gestion des accès à privilèges (bastion). |
| **CVE** | Common Vulnerabilities and Exposures — Identifiant standardisé de vulnérabilité. |
| **CVSS** | Common Vulnerability Scoring System — Score de criticité d'une vulnérabilité (0–10). |
| **MFA** | Multi-Factor Authentication — Authentification multifacteur. |
| **VPN** | Virtual Private Network — Réseau privé virtuel chiffré. |
| **SIEM** | Security Information and Event Management — Corrélation et gestion des événements de sécurité. |
| **IDS / IPS** | Intrusion Detection/Prevention System — Système de détection/prévention d'intrusion. |
| **PKI** | Public Key Infrastructure — Infrastructure à clé publique (certificats X.509). |
| **NTP** | Network Time Protocol — Synchronisation d'horloge (obligatoire pour les logs). |
| **RPO** | Recovery Point Objective — Perte de données maximale acceptable (en temps). |
| **RTO** | Recovery Time Objective — Durée maximale acceptable d'indisponibilité. |
| **MOC** | Management of Change — Gestion des modifications (obligatoire pour les changements OT). |
| **PASSI** | Prestataire d'Audit de la Sécurité des Systèmes d'Information — Qualification ANSSI (France). |
| **NIS2** | Network and Information Security directive 2 — Directive européenne cybersécurité (2022/2555). |
| **CRA** | Cyber Resilience Act — Règlement européen cybersécurité pour les produits connectés (2024). |
| **Air gap** | Isolation physique totale d'un réseau (aucune connexion réseau physique). |
| **Data diode** | Équipement permettant un flux réseau unidirectionnel (lecture seule). |
| **Whitelist** | Liste blanche — Seuls les éléments listés sont autorisés (approche recommandée OT). |
| **Kill chain** | Séquence des étapes d'une cyberattaque (reconnaissance → impact). |
| **APT** | Advanced Persistent Threat — Menace persistante avancée (acteur étatique ou groupe sophistiqué). |

---

## 15. Références et ressources

### 15.1 Documents normatifs officiels

| Référence | Titre | Statut |
|-----------|-------|--------|
| IEC 62443-1-1:2009 | Terminologie, concepts et modèles | Publié |
| IEC 62443-2-1:2010 | Exigences pour un CSMS | Publié (révision en cours) |
| IEC 62443-2-3:2015 | Gestion des patches | Publié |
| IEC 62443-2-4:2015/AMD1:2017 | Exigences pour les prestataires | Publié |
| IEC 62443-3-2:2020 | Évaluation des risques | Publié |
| IEC 62443-3-3:2013 | Exigences système et SL | Publié |
| IEC 62443-4-1:2018 | Cycle de développement sécurisé | Publié |
| IEC 62443-4-2:2019 | Exigences techniques composants | Publié |

### 15.2 Guides ANSSI sur la cybersécurité industrielle

- **ANSSI — Maîtriser la SSI pour les systèmes industriels** (Guide n°1 — Bonnes pratiques, 2014)
- **ANSSI — Maîtriser la SSI pour les systèmes industriels** (Guide n°2 — Méthode de classification et mesures, 2014)
- **ANSSI — Cybersécurité des systèmes industriels : 12 recommandations** (2022)
- **ANSSI — Guide EBIOS Risk Manager** (2018, mis à jour 2023)

Disponibles sur : [https://www.ssi.gouv.fr](https://www.ssi.gouv.fr)

### 15.3 Ressources NIST

- **NIST SP 800-82 Rev. 3** — Guide to Operational Technology (OT) Security (2023)
- **NIST Cybersecurity Framework 2.0** (2024)

Disponibles sur : [https://csrc.nist.gov](https://csrc.nist.gov)

### 15.4 Organismes et certifications

| Organisme | Rôle | Site |
|-----------|------|------|
| IEC | Éditeur de la norme | iec.ch |
| ISA | Éditeur des standards ISA-99 (base IEC 62443) | isa.org |
| ANSSI | Agence française, recommandations et certifications | ssi.gouv.fr |
| BSI | Agence allemande, homologue ANSSI | bsi.bund.de |
| CISA | Agence US, cybersécurité ICS | cisa.gov |
| TÜV Rheinland | Certification IEC 62443 composants et systèmes | tuv.com |
| Exida | Certification IEC 62443, spécialiste OT | exida.com |

### 15.5 Veille sur les vulnérabilités OT

| Ressource | Contenu | URL |
|-----------|---------|-----|
| ICS-CERT / CISA Advisories | Alertes vulnérabilités ICS | cisa.gov/ics-advisories |
| CERT-FR | Avis vulnérabilités (inclus OT) | cert.ssi.gouv.fr |
| NVD NIST | Base CVE nationale américaine | nvd.nist.gov |
| Dragos Year in Review | Rapport annuel menaces OT | dragos.com |
| Claroty State of CPS Security | Rapport annuel CPS/OT | claroty.com |
| Shodan | Découverte d'équipements OT exposés | shodan.io |

### 15.6 Formations et certifications professionnelles

| Certification | Organisme | Description |
|--------------|-----------|-------------|
| **ISA/IEC 62443 Cybersecurity Certificate** | ISA Global | Programme en 4 niveaux (Fundamentals → Expert) |
| **GICSP** (Global Industrial Cyber Security Professional) | GIAC/SANS | Certification large public OT |
| **CSSA** (Certified SCADA Security Architect) | IACRB | Spécialiste SCADA/ICS |
| **CFSE** (Certified Functional Safety Expert) | TÜV | Sécurité fonctionnelle + cybersécurité |
| **CISSP** (focus ICS) | (ISC)² | CISSP avec domaine systèmes OT |

---

*Document de référence pédagogique — SEC500 · Cybersécurité appliquée à l'industrie 4.0*
*JUNIA XP — Mastère Chef de projet Industrie 4.0 — Année 2 — 2025/2026*
*Formateur : Christophe CROISANT*
*Version 1.0 — Juin 2025*

> **Avertissement :** Ce document est un support pédagogique. Pour toute mise en conformité réelle, se référer aux textes normatifs officiels publiés par l'IEC et aux guides opérationnels de l'ANSSI. Les références aux produits commerciaux sont données à titre illustratif et ne constituent pas une recommandation commerciale.
