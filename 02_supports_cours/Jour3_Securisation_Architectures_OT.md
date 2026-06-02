# SEC500 — Jour 3 : Normes, standards & sécurisation des communications
**Cybersécurité appliquée à l'industrie 4.0**
*Mastère Chef de projet Industrie 4.0 — Année 2 · JUNIA XP 2025/2026*

---

## Sommaire

- [Module 4 — Normes et standards de cybersécurité industrielle](#module-4)
  - [4.1 IEC 62443 — structure, zones, conduits et niveaux de sécurité](#41-iec62443)
  - [4.2 ISO/IEC 27001 — application au contexte OT](#42-iso27001)
  - [4.3 NIST Cybersecurity Framework (CSF)](#43-nist-csf)
  - [4.4 Référentiels ANSSI pour les systèmes industriels](#44-anssi)
  - [4.5 Gouvernance et certification OT](#45-gouvernance)
- [Module 5 — Sécurisation des communications et systèmes embarqués](#module-5)
  - [5.1 TLS et mTLS — principes et application industrielle](#51-tls-mtls)
  - [5.2 PKI industrielle — certificats X.509 et gestion des clés](#52-pki)
  - [5.3 MQTT sécurisé (MQTTs) — du port 1883 au port 8883](#53-mqtt-securise)
  - [5.4 OPC-UA sécurisé](#54-opcua-securise)
  - [5.5 Contraintes de sécurité sur les objets IIoT embarqués](#55-iiot-embarque)
- [Atelier 2 — Sécurisation MQTT avec authentification mutuelle mTLS](#atelier-2)
- [Étude de cas — Mise en conformité IEC 62443 & debriefing Atelier 2](#etude-de-cas)

---

## Module 4 — Normes et standards de cybersécurité industrielle {#module-4}

### 4.1 IEC 62443 — structure, zones, conduits et niveaux de sécurité {#41-iec62443}

#### Présentation générale

La norme **IEC 62443** (anciennement ANSI/ISA-99) est le cadre normatif international de référence pour la cybersécurité des **systèmes d'automatisation et de contrôle industriels (IACS — Industrial Automation and Control Systems)**. Elle est publiée conjointement par l'IEC (International Electrotechnical Commission) et l'ISA (International Society of Automation).

**Pourquoi IEC 62443 et pas ISO 27001 seule ?**

ISO 27001 est généraliste (systèmes d'information) et ne prend pas en compte les contraintes spécifiques de l'OT :
- Disponibilité continue du processus (pas d'arrêt pour patches)
- Temps réel et sûreté physique
- Cycles de vie des équipements de 15 à 30 ans
- Protocoles sans authentification native

IEC 62443 comble ces lacunes avec des exigences adaptées aux contraintes industrielles.

---

#### Structure de la norme — quatre séries

IEC 62443 est organisée en quatre séries de documents, chacune adressant un acteur différent de l'écosystème industriel :

```
┌─────────────────────────────────────────────────────────────────┐
│  IEC 62443 — Vue d'ensemble et organisation                     │
├──────────────────┬──────────────────────────────────────────────┤
│  Série 1         │  Concepts généraux et terminologie           │
│  (Généralités)   │  1-1 : Terminologie, concepts, modèles       │
│                  │  1-2 : Glossaire de termes et abréviations   │
│                  │  1-3 : Métriques de conformité               │
│                  │  1-4 : Cycle de vie IACS et cas d'utilisation│
├──────────────────┼──────────────────────────────────────────────┤
│  Série 2         │  Politiques et procédures (pour les          │
│  (Opérateurs)    │  exploitants / Asset Owners)                 │
│                  │  2-1 : Exigences pour un programme CSMS      │
│                  │  2-2 : Implémentation d'un CSMS              │
│                  │  2-3 : Gestion des patches                   │
│                  │  2-4 : Exigences pour les prestataires IACS  │
├──────────────────┼──────────────────────────────────────────────┤
│  Série 3         │  Sécurité du système (pour les intégrateurs) │
│  (Intégrateurs)  │  3-1 : Technologies de sécurité pour IACS   │
│                  │  3-2 : Évaluation des risques (PSSA/TSSA)   │
│                  │  3-3 : Exigences de sécurité système (SSR)  │
├──────────────────┼──────────────────────────────────────────────┤
│  Série 4         │  Sécurité des composants (pour les          │
│  (Fournisseurs)  │  fabricants d'équipements)                   │
│                  │  4-1 : Cycle de développement sécurisé (SDLC)│
│                  │  4-2 : Exigences de sécurité des composants  │
└──────────────────┴──────────────────────────────────────────────┘
```

> **Pour un chef de projet Industrie 4.0**, les sections les plus pertinentes sont **2-1** (programme de cybersécurité), **3-2** (évaluation des risques) et **3-3** (exigences de sécurité système).

---

#### Zones et conduits — le cœur du modèle IEC 62443

Le concept fondamental d'IEC 62443 est la division du système industriel en **zones de sécurité** reliées par des **conduits**.

**Zone de sécurité (Security Zone) :**
Regroupement logique d'actifs (équipements, systèmes, réseaux) partageant le même niveau d'exigences de sécurité et les mêmes exigences de protection. Tous les actifs d'une zone partagent le même Security Level (SL).

**Conduit :**
Mécanisme de communication entre deux zones. Un conduit protège le flux de données entre zones de niveaux différents (firewall, DMZ, data diode). Tout flux entre deux zones doit passer par un conduit défini et contrôlé.

**Exemple d'architecture zonée — MecaProd après sécurisation :**

```
┌──────────────────────────────────────────────────────────────────┐
│  Zone 4 : Entreprise / IT (SL-1)                                 │
│  ERP, messagerie, postes bureautiques, AD                        │
└──────────────────────┬───────────────────────────────────────────┘
                       │  Conduit A : Firewall + DMZ
┌──────────────────────┴───────────────────────────────────────────┐
│  Zone DMZ industrielle (SL-2)                                    │
│  Historien de données, Jump server, serveur de fichiers OT       │
└──────────────────────┬───────────────────────────────────────────┘
                       │  Conduit B : Firewall OT (règles strictes)
┌──────────────────────┴───────────────────────────────────────────┐
│  Zone 3 : Supervision (SL-2)                                     │
│  Serveurs SCADA, HMI, MES                                        │
└──────────────────────┬───────────────────────────────────────────┘
                       │  Conduit C : Firewall applicatif OT
┌──────────────────────┴───────────────────────────────────────────┐
│  Zone 2 : Contrôle (SL-2 à SL-3)                                │
│  PLC, DCS, contrôleurs de terrain                                │
└──────────────────────┬───────────────────────────────────────────┘
                       │  (accès physique uniquement)
┌──────────────────────┴───────────────────────────────────────────┐
│  Zone 1 : Terrain (SL-1 à SL-2)                                  │
│  Capteurs, actionneurs, variateurs, instruments                  │
└──────────────────────────────────────────────────────────────────┘
```

---

#### Niveaux de sécurité (Security Levels — SL)

IEC 62443 définit quatre **Security Levels (SL)** qui décrivent la capacité de résistance d'un système face à différents types d'attaquants :

| SL | Niveau | Description | Profil attaquant résisté |
|---|---|---|---|
| **SL-1** | Basique | Protection contre les violations non intentionnelles (erreurs humaines, pannes accidentelles) | Utilisateur non spécialisé agissant accidentellement |
| **SL-2** | Standard | Protection contre les attaquants avec moyens limités, motivation généraliste | Attaquant simple utilisant des outils génériques |
| **SL-3** | Élevé | Protection contre les attaquants avec moyens significatifs, motivation et compétences OT | Attaquant sophistiqué avec connaissances spécifiques IACS |
| **SL-4** | Critique | Protection contre les acteurs étatiques disposant de ressources exceptionnelles | APT étatique, ressources illimitées |

**Trois types de SL :**
- **SL-T (Target)** : niveau de sécurité cible défini lors de l'évaluation des risques
- **SL-C (Capability)** : niveau que le système est capable d'atteindre avec ses contre-mesures
- **SL-A (Achieved)** : niveau effectivement atteint après vérification et audit

> **En pratique :** La grande majorité des systèmes industriels existants est en dessous de SL-1. L'objectif réaliste pour une PME industrielle est d'atteindre SL-2 sur les zones critiques.

---

#### Les 7 Foundational Requirements (FR)

IEC 62443-3-3 définit 7 exigences fondamentales (FR) que tout IACS sécurisé doit satisfaire :

| FR | Intitulé | Description | Exemples de mesures |
|---|---|---|---|
| **FR 1** | Identification & authentification | Contrôler et vérifier l'identité des utilisateurs, équipements et logiciels | MFA, comptes nominatifs, certificats |
| **FR 2** | Contrôle des usages | Restreindre les accès aux fonctions nécessaires (principe du moindre privilège) | RBAC, liste blanche applicative |
| **FR 3** | Intégrité des données | Protéger l'intégrité des informations et des systèmes | Signature des programmes PLC, checksums |
| **FR 4** | Confidentialité des données | Protéger les informations contre les divulgations non autorisées | Chiffrement des communications (TLS) |
| **FR 5** | Flux de données restreints | Segmenter le réseau et contrôler les flux entre zones | Firewalls, DMZ, conduits définis |
| **FR 6** | Réaction aux événements | Détecter, enregistrer et réagir aux incidents de sécurité | SIEM, IDS OT, journalisation |
| **FR 7** | Disponibilité des ressources | Garantir la disponibilité des ressources nécessaires au processus | Redondance, protection DoS, backup |

Pour chaque FR, IEC 62443-3-3 définit des **System Requirements (SR)** et des **Requirement Enhancements (RE)** correspondant aux différents SL.

---

### 4.2 ISO/IEC 27001 — application au contexte OT {#42-iso27001}

#### Présentation

**ISO/IEC 27001** est la norme internationale de management de la sécurité de l'information (SMSI — Système de Management de la Sécurité de l'Information). Elle s'applique à tout type d'organisation et de système d'information.

**Structure de la norme :**
- Clauses 4 à 10 : exigences du système de management (contexte, leadership, planification, support, opération, évaluation, amélioration)
- **Annexe A** : 93 mesures de sécurité organisées en 4 thèmes (organisationnelles, humaines, physiques, technologiques) dans la version 2022

**Principaux apports d'ISO 27001 pour l'OT :**
- Cadre de gouvernance : politique de sécurité, rôles et responsabilités, revues de direction
- Gestion des actifs : inventaire exhaustif des équipements (PLC, HMI, passerelles...)
- Gestion des risques : méthodologie formalisée (EBIOS RM, ISO 31000)
- Gestion des incidents : procédures de détection, réponse, post-mortem
- Continuité d'activité : PCA/PRA adaptés aux contraintes OT

**Limites d'ISO 27001 seule en OT :**

| Limite | Impact |
|---|---|
| Conçue pour les systèmes IT | Pas de guidance sur Modbus, PLC, temps réel |
| Disponibilité = objectif parmi d'autres | En OT, la disponibilité prime sur tout |
| Cycles de patches normaux supposés | Ne tient pas compte des délais de validation constructeur |
| Concepts IT (antivirus, EDR) | Inapplicables sur PLC avec 256 Ko de RAM |

**Complémentarité ISO 27001 + IEC 62443 :**

```
ISO 27001                          IEC 62443
    │                                  │
    ▼                                  ▼
Gouvernance générale          Exigences techniques OT
Politique de sécurité   +     Zones et conduits
Gestion des risques           Security Levels
Continuité d'activité         Protocoles industriels
Audit et certification        Contraintes temps réel
```

---

### 4.3 NIST Cybersecurity Framework (CSF) {#43-nist-csf}

#### Présentation

Le **NIST CSF (Cybersecurity Framework)** est un cadre volontaire publié par le National Institute of Standards and Technology (NIST) des États-Unis. Sa version 2.0 (2024) est structurée autour de **6 fonctions** :

| Fonction | Description | Exemples de catégories |
|---|---|---|
| **GOVERN** *(nouveau CSF 2.0)* | Établir et surveiller la stratégie de cybersécurité | Politique, rôles, gestion des risques |
| **IDENTIFY** | Comprendre le contexte et les risques | Inventaire des actifs, évaluation des risques |
| **PROTECT** | Mettre en place des mesures de protection | Contrôle d'accès, formation, chiffrement |
| **DETECT** | Détecter les événements de cybersécurité | Surveillance réseau, SIEM, IDS |
| **RESPOND** | Répondre aux incidents détectés | Plan de réponse, communication, atténuation |
| **RECOVER** | Rétablir les capacités après un incident | Plan de reprise, communication post-incident |

**Application du NIST CSF à l'OT industriel :**

NIST a publié le **SP 800-82 Rev.3** spécifiquement pour l'OT (Guide to Operational Technology Security), qui adapte le CSF aux contraintes industrielles. Les points clés :

- **IDENTIFY** → inventaire exhaustif de tous les équipements OT, y compris les équipements legacy sans agent
- **PROTECT** → segmentation réseau, liste blanche applicative (Application Allowlisting) plutôt qu'antivirus
- **DETECT** → surveillance réseau passive (écoute sur port SPAN) plutôt qu'agents sur les PLC
- **RESPOND** → procédures adaptées à l'OT : ne pas éteindre un PLC de sécurité sans procédure
- **RECOVER** → tests de restauration réguliers des sauvegardes de programmes PLC

---

### 4.4 Référentiels ANSSI pour les systèmes industriels {#44-anssi}

#### L'ANSSI et les OIV/OSE

L'**ANSSI (Agence Nationale de la Sécurité des Systèmes d'Information)** est l'autorité nationale française en cybersécurité. Elle produit des référentiels et des guides applicables aux systèmes industriels, notamment pour les :

- **OIV (Opérateurs d'Importance Vitale)** — entités dont l'activité est indispensable à la survie de la nation (énergie, eau, transport, santé, défense...) — soumis à la **Loi de Programmation Militaire (LPM)** et à ses arrêtés sectoriels
- **OSE (Opérateurs de Services Essentiels)** — entités fournissant des services essentiels à l'économie selon la **directive NIS** (Network and Information Systems) transposée en droit français

#### Principaux documents ANSSI pour l'OT

| Document | Contenu | Public cible |
|---|---|---|
| **Maîtriser la SSI pour les SI industriels** (2014, mise à jour 2021) | Guide de référence, 25 mesures fondamentales pour les SI industriels | DSI, RSSI, responsables OT |
| **Cybersécurité des systèmes industriels** (Guide pratique) | Mise en œuvre des 25 mesures, exemples concrets | Intégrateurs, opérateurs |
| **Guide de l'hygiène informatique** | 42 règles de base applicables à tout SI, y compris OT | Toute organisation |
| **Référentiel d'exigences pour les prestataires de détection** (PDIS) | Exigences pour les SOC gérant des réseaux OT | Prestataires de sécurité |
| **Méthode EBIOS Risk Manager** | Méthode d'analyse de risques, utilisée pour les OIV et adaptable à l'OT | RSSI, chefs de projet sécurité |

#### Les 25 mesures ANSSI pour les SI industriels

Organisées en 5 catégories :

**Mesures organisationnelles (1–5) :**
1. Établir une politique de sécurité des SI industriels
2. Réaliser une analyse de risques spécifique OT
3. Identifier et cartographier les actifs industriels
4. Intégrer la cybersécurité dans les projets OT dès la conception
5. Sensibiliser et former les équipes OT

**Mesures d'architecture (6–12) :**
6. Cloisonner les réseaux IT et OT (pas de réseau plat)
7. Définir des DMZ industrielles pour les échanges IT/OT
8. Mettre en place des mécanismes d'authentification sur les accès distants
9. Surveiller les accès distants (journalisation, enregistrement de sessions)
10. Gérer les comptes privilégiés OT (pas de comptes partagés)
11. Appliquer le principe du moindre privilège
12. Sécuriser les postes d'ingénierie et les laptops de maintenance

**Mesures techniques (13–19) :**
13. Mettre en place un antivirus (si compatible avec le système) ou liste blanche applicative
14. Gérer les médias amovibles (politique USB, chiffrement)
15. Sauvegarder les programmes PLC et les configurations équipements
16. Gérer les vulnérabilités et les patches (processus documenté)
17. Surveiller le réseau OT (IDS passif, journalisation des flux)
18. Tester régulièrement les sauvegardes et procédures de reprise
19. Intégrer la cybersécurité dans les contrats de maintenance

**Mesures de réponse aux incidents (20–22) :**
20. Établir et tester un plan de réponse aux incidents OT
21. Définir les procédures de communication de crise (interne et externe)
22. Prévoir des modes de fonctionnement dégradé (sans réseau)

**Mesures spécifiques aux accès tiers (23–25) :**
23. Encadrer les interventions des prestataires et mainteneurs
24. Sécuriser les téléaccès des fournisseurs (VPN dédié, supervision)
25. Auditer régulièrement la sécurité des SI industriels

---

### 4.5 Gouvernance et certification OT {#45-gouvernance}

#### Le CSMS — Cyber Security Management System

IEC 62443-2-1 définit les exigences d'un **CSMS (Cyber Security Management System)** pour les opérateurs industriels. Il couvre :

- **Analyse de risques** (Risk Assessment) — identification des actifs, menaces, vulnérabilités, impacts
- **Politique de sécurité** — règles, responsabilités, procédures
- **Implémentation** — mesures techniques et organisationnelles
- **Surveillance et amélioration continue** — audits, revues, indicateurs

**Articulation avec ISO 27001 :** un SMSI certifié ISO 27001 peut servir de base au CSMS, avec des extensions spécifiques OT pour les zones, conduits et SL.

#### Certifications disponibles

| Certification | Référentiel | Portée | Valeur |
|---|---|---|---|
| **ISA/IEC 62443 Cybersecurity Certificate Program** (ISA) | IEC 62443 | Individus (CSST, CSSPM, CSSE) | Reconnaissance internationale |
| **ISO/IEC 27001** (organismes certificateurs accrédités) | ISO 27001 | Organisations | Cadre de gouvernance général |
| **CISA — Certified SCADA Security Architect** (SANS) | GICSP | Individus | Pratique OT reconnue |
| **Qualification PDIS/PRIS** (ANSSI) | Référentiel ANSSI | Prestataires de sécurité | Obligatoire pour les OIV |

---

## Module 5 — Sécurisation des communications et systèmes embarqués {#module-5}

### 5.1 TLS et mTLS — principes et application industrielle {#51-tls-mtls}

#### TLS (Transport Layer Security) — rappels

**TLS** est le protocole de chiffrement des communications sur les réseaux IP. Il remplace SSL (obsolète depuis 2015) et est utilisé dans HTTPS, SMTPS, IMAPS, et les protocoles industriels sécurisés (MQTTs, OPC-UA, S7commTLS).

**Version actuelle recommandée :** TLS 1.3 (RFC 8446, 2018). TLS 1.0 et 1.1 sont dépréciés et vulnérables (POODLE, BEAST). TLS 1.2 est encore acceptable avec les bonnes suites cryptographiques.

**Ce que TLS garantit :**
- **Confidentialité** — chiffrement asymétrique pour l'échange de clés, chiffrement symétrique pour les données (AES-256-GCM)
- **Intégrité** — HMAC ou AEAD pour détecter toute modification des données en transit
- **Authentification du serveur** — le client vérifie que le serveur est légitime via son certificat X.509

**Ce que TLS seul ne garantit pas :**
- L'authentification du **client** — le serveur accepte tout client qui se connecte (problème pour les réseaux OT)

#### TLS standard — déroulé du handshake (simplifié TLS 1.3)

```
  Client (HMI)                          Serveur (broker MQTT / OPC-UA)
       │                                          │
       │──── ClientHello (versions, ciphers) ────>│
       │                                          │
       │<─── ServerHello + Certificate ───────────│
       │     (certificat serveur + clé publique)  │
       │                                          │
       │  [Client vérifie le certificat serveur   │
       │   via la CA de confiance]                │
       │                                          │
       │──── Finished (clé de session dérivée) ──>│
       │                                          │
       │<══════ Canal chiffré TLS établi ════════>│
       │                                          │
       │──── Données chiffrées (MQTT publish) ───>│
```

**Problème en OT :** avec TLS standard, n'importe quel client peut se connecter au broker MQTT ou au serveur OPC-UA tant qu'il accepte le certificat serveur. Un PLC compromis ou un équipement non autorisé peuvent donc accéder au système.

---

#### mTLS (Mutual TLS) — authentification mutuelle

**mTLS** (Mutual TLS) étend TLS en exigeant que **les deux parties** (client ET serveur) présentent un certificat X.509 valide, signé par une CA de confiance commune. C'est le standard recommandé pour les communications industrielles sécurisées.

**Ce que mTLS ajoute à TLS :**
- **Authentification du client** — le serveur vérifie que le client est un équipement connu et autorisé
- **Zero Trust réseau** — même si un attaquant accède au réseau OT, il ne peut pas se connecter sans un certificat valide
- **Révocation possible** — un certificat client compromis peut être révoqué via CRL ou OCSP

#### mTLS — déroulé du handshake

```
  Client (capteur IIoT / PLC)              Serveur (broker MQTT sécurisé)
       │                                              │
       │──── ClientHello ────────────────────────────>│
       │                                              │
       │<─── ServerHello + Certificate               │
       │     + CertificateRequest ───────────────────│
       │     (le serveur demande le cert client)      │
       │                                              │
       │  [Client vérifie certificat serveur via CA]  │
       │                                              │
       │──── Certificate (certificat client)─────────>│
       │──── CertificateVerify (signature) ──────────>│
       │──── Finished ───────────────────────────────>│
       │                                              │
       │  [Serveur vérifie certificat client via CA]  │
       │                                              │
       │<══════════ Canal mTLS établi ═══════════════>│
       │                                              │
  ✓ Client authentifié + Serveur authentifié
  ✓ Communications chiffrées et intègres
  ✗ Tout client sans certificat valide est rejeté
```

**Cas d'usage industriels du mTLS :**
- MQTT entre capteurs IIoT et broker (authentification de chaque capteur)
- OPC-UA entre PLC et serveur SCADA
- API REST entre systèmes MES et ERP
- Communications entre edge nodes et cloud industriel

---

### 5.2 PKI industrielle — certificats X.509 et gestion des clés {#52-pki}

#### Infrastructure à clés publiques (PKI)

Une **PKI (Public Key Infrastructure)** est l'ensemble des composants, politiques et procédures permettant de créer, distribuer, gérer et révoquer des certificats numériques.

**Composants d'une PKI :**

```
┌────────────────────────────────────────────────────────────┐
│  Root CA (Autorité de Certification Racine)                │
│  Auto-signée, hors ligne (offline), hautement sécurisée    │
│  Signe les certificats des CA intermédiaires               │
└────────────────────────┬───────────────────────────────────┘
                         │ signe
┌────────────────────────┴───────────────────────────────────┐
│  Intermediate CA (CA intermédiaire)                        │
│  En ligne, signe les certificats finaux                    │
│  Peut être dédiée par usage (PKI serveurs, PKI équipements)│
└────────────────────────┬───────────────────────────────────┘
                         │ signe
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
   Certificat       Certificat       Certificat
   serveur          client 1         client 2
   (broker MQTT)    (capteur A)      (PLC B)
```

**Pourquoi une CA racine hors ligne ?**
Si la CA racine est compromise, tous les certificats signés par elle deviennent invalides. En la maintenant hors ligne, on élimine le risque d'intrusion réseau. Elle n'est connectée que lors des rares opérations de signature de CA intermédiaires.

#### Structure d'un certificat X.509

Un certificat X.509 contient les champs suivants :

```
Certificate:
  Version: 3
  Serial Number: 01:23:45:67:89:AB:CD:EF
  Signature Algorithm: sha256WithRSAEncryption
  Issuer: CN=Industrial-CA, O=MecaProd, C=FR    ← identité de la CA émettrice
  Validity:
    Not Before: 2025-09-01 00:00:00 UTC
    Not After:  2026-09-01 00:00:00 UTC          ← durée de validité
  Subject: CN=sensor-temp-001, O=MecaProd, C=FR ← identité de l'équipement
  Subject Public Key Info:
    Public Key Algorithm: rsaEncryption
    RSA Public Key: (2048 bit)
  X509v3 Extensions:
    Key Usage: Digital Signature, Key Encipherment
    Extended Key Usage: TLS Web Client Authentication ← usage client mTLS
    Basic Constraints: CA:FALSE
    Subject Alternative Name: DNS:sensor-temp-001.ot.mecaprod.fr
  Signature: [signé par la clé privée de la CA]
```

#### Génération d'une PKI avec OpenSSL — référence complète

**Étape 1 — Créer l'Autorité de Certification (CA) :**
```bash
# Créer le répertoire de travail PKI
mkdir -p /opt/pki/{ca,server,clients}
cd /opt/pki

# Générer la clé privée de la CA (RSA 4096 bits, chiffrée avec passphrase)
openssl genrsa -aes256 -out ca/ca.key 4096

# Générer le certificat auto-signé de la CA (valable 10 ans)
openssl req -x509 -new -nodes -key ca/ca.key -sha256 -days 3650 \
  -out ca/ca.crt \
  -subj "/C=FR/ST=HDF/L=Valenciennes/O=MecaProd/CN=MecaProd-Industrial-CA"
```

**Étape 2 — Créer le certificat serveur (broker MQTT) :**
```bash
# Générer la clé privée du serveur
openssl genrsa -out server/server.key 2048

# Générer une CSR (Certificate Signing Request)
openssl req -new -key server/server.key \
  -out server/server.csr \
  -subj "/C=FR/O=MecaProd/CN=mqtt.ot.mecaprod.fr"

# Signer la CSR par la CA (certificat valable 1 an)
openssl x509 -req -in server/server.csr \
  -CA ca/ca.crt -CAkey ca/ca.key -CAcreateserial \
  -out server/server.crt -days 365 -sha256
```

**Étape 3 — Créer un certificat client (capteur / PLC) :**
```bash
# Générer la clé privée du client
openssl genrsa -out clients/sensor-temp-001.key 2048

# Générer la CSR client
openssl req -new -key clients/sensor-temp-001.key \
  -out clients/sensor-temp-001.csr \
  -subj "/C=FR/O=MecaProd/CN=sensor-temp-001"

# Signer par la CA avec l'extension clientAuth
openssl x509 -req -in clients/sensor-temp-001.csr \
  -CA ca/ca.crt -CAkey ca/ca.key -CAcreateserial \
  -out clients/sensor-temp-001.crt -days 365 -sha256 \
  -extfile <(echo "extendedKeyUsage = clientAuth")
```

**Étape 4 — Vérifier la chaîne de confiance :**
```bash
# Vérifier le certificat serveur
openssl verify -CAfile ca/ca.crt server/server.crt
# Résultat attendu : server/server.crt: OK

# Vérifier le certificat client
openssl verify -CAfile ca/ca.crt clients/sensor-temp-001.crt
# Résultat attendu : clients/sensor-temp-001.crt: OK

# Inspecter un certificat
openssl x509 -in server/server.crt -text -noout
```

#### Gestion du cycle de vie des certificats

**Points de vigilance critiques en environnement OT :**

| Point | Problème | Solution |
|---|---|---|
| **Expiration** | Un certificat expiré bloque toutes les communications → arrêt de production | Inventaire des dates d'expiration, alertes automatiques 30/60/90 jours avant |
| **Révocation** | Un équipement volé ou compromis doit être retiré de la PKI | CRL (Certificate Revocation List) publiée et consultée, ou OCSP |
| **Stockage des clés privées** | Une clé privée volée compromet toute l'identité de l'équipement | HSM (Hardware Security Module) ou TPM pour les équipements qui le supportent |
| **Rotation** | Les certificats doivent être renouvelés régulièrement | Plan de rotation documenté, processus automatisé si possible |
| **Sauvegarde** | Perte de la clé CA = impossibilité de renouveler les certificats | Sauvegarde chiffrée hors ligne de la clé CA racine |

---

### 5.3 MQTT sécurisé (MQTTs) — du port 1883 au port 8883 {#53-mqtt-securise}

#### Rappel : MQTT en clair — les risques

MQTT sur port 1883 sans configuration de sécurité :
- Aucune authentification client → n'importe qui peut publier/s'abonner
- Données en clair → écoute passive triviale (Wireshark)
- Pas de contrôle d'accès aux topics → un client peut lire tous les topics
- Broker potentiellement exposé sur Internet (recherche Shodan `port:1883`)

**Exemple d'un broker MQTT non sécurisé exposé :**
```bash
# Connexion anonyme à un broker MQTT non sécurisé
mosquitto_sub -h 203.0.113.42 -p 1883 -t "#" -v
# Résultat : abonnement à TOUS les topics → lecture de toutes les données
factory/line1/temp/sensor01 : 847.3
factory/line1/pressure/valve02 : 6.2
factory/emergency/stop : 0
```

> **Analyse :** avec cette seule commande, un attaquant accède en temps réel à toutes les données de production, dont l'état des arrêts d'urgence.

---

#### Architecture de Mosquitto sécurisé (mTLS)

**Mosquitto** est le broker MQTT open source de référence (Eclipse Foundation). Il supporte TLS, mTLS, authentification par username/password et ACL (Access Control Lists).

**Fichier de configuration Mosquitto sécurisé (`/etc/mosquitto/mosquitto.conf`) :**

```ini
# ─── Port non sécurisé — DÉSACTIVÉ ─────────────────────────────
# listener 1883
# allow_anonymous true

# ─── Port sécurisé mTLS ─────────────────────────────────────────
listener 8883

# Certificats PKI
cafile   /opt/pki/ca/ca.crt           # CA racine → vérifie les certificats clients
certfile /opt/pki/server/server.crt   # Certificat serveur
keyfile  /opt/pki/server/server.key   # Clé privée serveur

# Authentification mutuelle obligatoire
require_certificate true              # Le client DOIT présenter un certificat
use_identity_as_username true         # Le CN du certificat = username MQTT

# Protocole TLS minimum
tls_version tlsv1.2                   # Rejeter TLS 1.0 et 1.1

# Accès anonyme interdit
allow_anonymous false

# ─── Contrôle d'accès par ACL ───────────────────────────────────
acl_file /etc/mosquitto/acl.conf

# ─── Journalisation ──────────────────────────────────────────────
log_dest file /var/log/mosquitto/mosquitto.log
log_type all
connection_messages true
```

**Fichier ACL (`/etc/mosquitto/acl.conf`) :**
```ini
# sensor-temp-001 : peut uniquement publier sur son topic
user sensor-temp-001
topic write factory/line1/temp/sensor01

# plc-line1 : peut lire les capteurs de la ligne 1 et publier les états
user plc-line1
topic read factory/line1/temp/#
topic read factory/line1/pressure/#
topic write factory/line1/control/#

# scada-server : accès en lecture à tout
user scada-server
topic read #
```

---

#### Test et validation de la configuration mTLS

**Test de connexion légitime (avec certificat valide) :**
```bash
# Connexion d'un client avec son certificat
mosquitto_pub \
  --cafile /opt/pki/ca/ca.crt \
  --cert /opt/pki/clients/sensor-temp-001.crt \
  --key /opt/pki/clients/sensor-temp-001.key \
  -h mqtt.ot.mecaprod.fr \
  -p 8883 \
  -t "factory/line1/temp/sensor01" \
  -m "847.3"
# Résultat attendu : message publié avec succès
```

**Test de rejet d'un client non autorisé (sans certificat) :**
```bash
# Tentative de connexion sans certificat
mosquitto_pub -h mqtt.ot.mecaprod.fr -p 8883 \
  -t "factory/line1/temp/sensor01" -m "test"
# Résultat attendu : Error: Connection refused (not authorised)
# ou : SSL handshake failed
```

**Vérification dans Wireshark :**
```
Filtre : tcp.port == 8883

→ Avant mTLS (port 1883) :
  Trames MQTT en clair : topics et payloads lisibles

→ Après mTLS (port 8883) :
  Trames TLS chiffrées : Application Data [chiffré]
  Seuls les métadonnées TCP/IP sont visibles (IP source/dest, taille)
  Le contenu (topic, payload) est illisible
```

---

### 5.4 OPC-UA sécurisé {#54-opcua-securise}

#### Modèles de sécurité OPC-UA

OPC-UA est l'un des rares protocoles industriels à avoir intégré la sécurité dès sa conception. Il définit trois **Security Modes** :

| Mode | Chiffrement | Signature | Usage recommandé |
|---|---|---|---|
| **None** | Non | Non | Tests uniquement — **jamais en production** |
| **Sign** | Non | Oui | Intégrité garantie, pas de confidentialité |
| **SignAndEncrypt** | Oui (AES-128/256) | Oui | **Standard en production** |

**Security Policies disponibles (TLS 1.3 équivalent) :**
- `Basic256Sha256` — RSA 2048, AES-256-CBC, SHA-256 (minimum recommandé)
- `Aes128_Sha256_RsaOaep` — AES-128-CTR, SHA-256, RSA-OAEP
- `Aes256_Sha256_RsaPss` — AES-256-CTR, SHA-256, RSA-PSS (niveau le plus élevé)

**Point de vigilance OPC-UA :** les implémentations OPC-UA autorisent souvent le mode **None** par défaut pour des raisons de compatibilité. Un audit doit systématiquement vérifier que ce mode est désactivé.

```bash
# Vérification des modes de sécurité disponibles sur un serveur OPC-UA
# avec l'outil opcua-client ou python-opcua
python3 -c "
from opcua import Client
c = Client('opc.tcp://192.168.10.110:4840')
c.connect()
print('Security modes:', c.server_policy_ids)
c.disconnect()
"
```

---

### 5.5 Contraintes de sécurité sur les objets IIoT embarqués {#55-iiot-embarque}

#### Le paradoxe de la sécurité embarquée

Les objets IIoT (capteurs, passerelles légères, RTU) cumulent des contraintes qui rendent l'implémentation de la sécurité difficile :

| Contrainte | Valeur typique | Impact sur la sécurité |
|---|---|---|
| CPU | 32–200 MHz (Cortex-M) | TLS complet consomme trop de cycles |
| RAM | 64 Ko – 512 Ko | Stack TLS nécessite ~50–80 Ko |
| Flash | 256 Ko – 4 Mo | Pas de place pour un agent de sécurité |
| Énergie | < 10 mW (batterie) | Chiffrement asymétrique trop coûteux |
| Réseau | LPWAN (868 MHz) | Trame de 51 octets max (LoRaWAN) |
| Durée de vie | 10–20 ans | Obsolescence sécurité inévitable |

#### Mesures adaptées aux contraintes embarquées

**1. Cryptographie légère (Lightweight Cryptography)**
- **AES-128-CCM** : chiffrement + authentification en une passe, adapté aux microcontrôleurs
- **ChaCha20-Poly1305** : alternative à AES, efficace sans accélération matérielle
- **ECDH / ECDSA sur courbes elliptiques** (ex. Curve25519) : clés courtes (256 bits) pour une sécurité équivalente à RSA-3072
- **Standard NIST LwC** : ASCON (finaliste 2023) — optimisé pour les environnements ultra-contraints

**2. TLS adapté**
- **DTLS** (Datagram TLS) : TLS sur UDP pour les protocoles temps réel
- **TLS-PSK** (Pre-Shared Key) : TLS avec clé partagée préchargée, sans PKI complète
- **Mbed TLS** (anciennement PolarSSL) : implémentation TLS optimisée pour les microcontrôleurs ARM

**3. Gestion des identités sans PKI complète**
- Provisioning de clés pré-partagées en usine (HSM de provisioning)
- Token JWT (JSON Web Token) pour l'authentification des capteurs vers le cloud
- **Zero Touch Provisioning** : les équipements récupèrent leurs certificats automatiquement lors du premier démarrage

**4. Segmentation réseau comme compensation**
Quand la sécurité intrinsèque de l'équipement est insuffisante, la segmentation réseau devient indispensable :
- VLAN dédié aux capteurs IIoT avec règles de firewall strictes (only MQTT out, rien d'autre)
- Passerelle de sécurité (Industrial DMZ) entre les capteurs et le réseau de supervision
- Liste blanche des flux autorisés (uniquement port 8883 vers le broker connu)

---

## Atelier 2 — Sécurisation MQTT avec authentification mutuelle mTLS {#atelier-2}

### Objectifs pédagogiques

À l'issue de cet atelier, chaque binôme doit être capable de :
- Démontrer les risques concrets d'un broker MQTT non sécurisé
- Générer une PKI complète (CA + certificat serveur + certificat client) avec OpenSSL
- Configurer Mosquitto en mode mTLS avec authentification mutuelle obligatoire
- Valider la sécurisation en testant le rejet d'un client non autorisé
- Capturer avec Wireshark le trafic avant (clair) et après (chiffré) pour documenter l'apport de mTLS

### Environnement de l'atelier

```
  ┌─────────────────────────────────────────────────────┐
  │  Réseau de l'atelier : 192.168.20.0/24              │
  │                                                     │
  │  192.168.20.10  — Serveur Mosquitto (Ubuntu)        │
  │                   Broker MQTT port 1883 → 8883      │
  │                                                     │
  │  192.168.20.20  — Client légitime (Ubuntu)          │
  │                   Simule un capteur IIoT avec cert  │
  │                                                     │
  │  192.168.20.30  — Poste d'audit (Kali / Ubuntu)     │
  │                   Wireshark + test client non auth  │
  └─────────────────────────────────────────────────────┘
```

---

### Phase 1 — Démonstration de l'insécurité MQTT (20 min)

**Objectif :** mesurer concrètement les risques du port 1883.

**1.1 — Démarrer Mosquitto en mode non sécurisé :**
```bash
# Sur le serveur Mosquitto (192.168.20.10)
sudo systemctl stop mosquitto

# Créer une configuration non sécurisée de démonstration
sudo tee /etc/mosquitto/conf.d/demo_insecure.conf << 'EOF'
listener 1883
allow_anonymous true
EOF

sudo systemctl start mosquitto
```

**1.2 — Écoute passive depuis le poste d'audit (Wireshark) :**
```bash
# Capture de tout le trafic MQTT port 1883
sudo wireshark -i eth0 -f "tcp port 1883" &
```

**1.3 — Publication de données depuis le client légitime :**
```bash
# Sur 192.168.20.20 — Simulation de publications d'un capteur
while true; do
  mosquitto_pub -h 192.168.20.10 -p 1883 \
    -t "factory/line1/temp/sensor01" \
    -m "$(shuf -i 840-860 -n 1).$(shuf -i 0-9 -n 1)"
  sleep 2
done
```

**1.4 — Interception depuis le poste d'audit :**
```bash
# Connexion anonyme et abonnement à tous les topics
mosquitto_sub -h 192.168.20.10 -p 1883 -t "#" -v
```

**Questions :**
1. Les données de température sont-elles visibles dans Wireshark ? Dans quel champ de la trame ?
2. En tant qu'attaquant, que pouvez-vous publier sur le topic `factory/line1/control/setpoint` ?
3. Que révèle l'abonnement au topic `#` sur la structure du système ?

---

### Phase 2 — Création de la PKI (30 min)

**Objectif :** générer une PKI industrielle minimale (CA + certificat serveur + certificat client).

**2.1 — Créer la structure de répertoires :**
```bash
mkdir -p ~/pki/{ca,server,clients}
cd ~/pki
```

**2.2 — Générer la CA :**
```bash
# Clé privée CA (sans passphrase pour faciliter l'atelier)
openssl genrsa -out ca/ca.key 4096

# Certificat auto-signé CA (10 ans)
openssl req -x509 -new -nodes -key ca/ca.key -sha256 -days 3650 \
  -out ca/ca.crt \
  -subj "/C=FR/O=MecaProd-Atelier/CN=MecaProd-CA"

# Vérification
openssl x509 -in ca/ca.crt -text -noout | grep -E "Subject:|Validity|Not"
```

**2.3 — Générer le certificat serveur Mosquitto :**
```bash
# Clé privée serveur
openssl genrsa -out server/server.key 2048

# CSR serveur
openssl req -new -key server/server.key -out server/server.csr \
  -subj "/C=FR/O=MecaProd-Atelier/CN=mqtt-broker"

# Signature par la CA
openssl x509 -req -in server/server.csr \
  -CA ca/ca.crt -CAkey ca/ca.key -CAcreateserial \
  -out server/server.crt -days 365 -sha256

# Vérification de la chaîne
openssl verify -CAfile ca/ca.crt server/server.crt
```

**2.4 — Générer le certificat client (capteur simulé) :**
```bash
# Clé privée client
openssl genrsa -out clients/sensor-temp-001.key 2048

# CSR client
openssl req -new -key clients/sensor-temp-001.key \
  -out clients/sensor-temp-001.csr \
  -subj "/C=FR/O=MecaProd-Atelier/CN=sensor-temp-001"

# Signature avec extension clientAuth
openssl x509 -req -in clients/sensor-temp-001.csr \
  -CA ca/ca.crt -CAkey ca/ca.key -CAcreateserial \
  -out clients/sensor-temp-001.crt -days 365 -sha256 \
  -extfile <(echo "extendedKeyUsage = clientAuth")

# Vérification
openssl verify -CAfile ca/ca.crt clients/sensor-temp-001.crt
```

**2.5 — Inspecter les certificats :**
```bash
# Voir le contenu du certificat client
openssl x509 -in clients/sensor-temp-001.crt -text -noout | \
  grep -A3 -E "Subject:|Issuer:|Validity|Extended Key"
```

**Questions :**
1. Quel est le champ `CN` (Common Name) du certificat CA ? Du certificat client ?
2. Par quelle entité le certificat `sensor-temp-001.crt` est-il signé ?
3. Quelle est la date d'expiration du certificat client généré ?

---

### Phase 3 — Configuration Mosquitto mTLS (30 min)

**Objectif :** reconfigurer Mosquitto pour n'accepter que les clients avec un certificat valide.

**3.1 — Copier les certificats sur le serveur :**
```bash
# Sur le serveur Mosquitto (192.168.20.10)
sudo mkdir -p /etc/mosquitto/certs
sudo cp ~/pki/ca/ca.crt            /etc/mosquitto/certs/
sudo cp ~/pki/server/server.crt    /etc/mosquitto/certs/
sudo cp ~/pki/server/server.key    /etc/mosquitto/certs/
sudo chown -R mosquitto:mosquitto  /etc/mosquitto/certs/
sudo chmod 600 /etc/mosquitto/certs/server.key
```

**3.2 — Écrire la configuration sécurisée :**
```bash
sudo tee /etc/mosquitto/conf.d/secure.conf << 'EOF'
# Désactiver le port non sécurisé
#listener 1883

# Port sécurisé mTLS
listener 8883

# Certificats
cafile   /etc/mosquitto/certs/ca.crt
certfile /etc/mosquitto/certs/server.crt
keyfile  /etc/mosquitto/certs/server.key

# mTLS : certificat client obligatoire
require_certificate true
use_identity_as_username true

# TLS minimum 1.2
tls_version tlsv1.2

# Pas d'accès anonyme
allow_anonymous false
EOF

# Supprimer la configuration non sécurisée
sudo rm /etc/mosquitto/conf.d/demo_insecure.conf

# Redémarrer
sudo systemctl restart mosquitto
sudo systemctl status mosquitto
```

**3.3 — Tester la connexion légitime (avec certificat) :**
```bash
# Depuis le client légitime (192.168.20.20)
# Copier le certificat client depuis le serveur PKI
scp user@192.168.20.10:~/pki/clients/sensor-temp-001.{crt,key} ~/
scp user@192.168.20.10:~/pki/ca/ca.crt ~/

# Publication avec certificat
mosquitto_pub \
  --cafile ~/ca.crt \
  --cert ~/sensor-temp-001.crt \
  --key ~/sensor-temp-001.key \
  -h 192.168.20.10 \
  -p 8883 \
  -t "factory/line1/temp/sensor01" \
  -m "847.3"
# Résultat attendu : aucun message d'erreur = succès
```

**3.4 — Tester le rejet d'un client non autorisé :**
```bash
# Depuis le poste d'audit (192.168.20.30) — sans certificat
mosquitto_pub -h 192.168.20.10 -p 8883 \
  -t "factory/line1/temp/sensor01" -m "attaque"
# Résultat attendu : Error: A TLS error occurred / Connection refused

# Avec le certificat CA seulement (sans certificat client)
mosquitto_pub --cafile ~/ca.crt \
  -h 192.168.20.10 -p 8883 \
  -t "factory/line1/temp/sensor01" -m "attaque"
# Résultat attendu : Error: Connection refused (not authorised)
```

---

### Phase 4 — Capture Wireshark avant / après (20 min)

**4.1 — Capture du trafic chiffré (port 8883) :**
```bash
# Wireshark sur le poste d'audit — port 8883
sudo wireshark -i eth0 -f "tcp port 8883" &
```

**4.2 — Générer du trafic MQTT sécurisé :**
```bash
# Depuis le client légitime
for i in $(seq 1 10); do
  mosquitto_pub --cafile ~/ca.crt \
    --cert ~/sensor-temp-001.crt \
    --key ~/sensor-temp-001.key \
    -h 192.168.20.10 -p 8883 \
    -t "factory/line1/temp/sensor01" \
    -m "$(shuf -i 840-860 -n 1)"
  sleep 1
done
```

**4.3 — Analyse comparative dans Wireshark :**

Appliquer les filtres :
```
tcp.port == 1883    → trafic MQTT non sécurisé (Phase 1)
tcp.port == 8883    → trafic mTLS (Phase 4)
tls.handshake      → voir le handshake mTLS (échange de certificats)
```

**Questions d'analyse :**
1. Sur le port 1883 : peut-on lire les topics et les valeurs ? Dans quel champ ?
2. Sur le port 8883 : que voit-on dans le champ Data des trames ?
3. Lors du handshake TLS, combien de messages sont échangés avant les données ?
4. Peut-on identifier le certificat client dans la capture Wireshark (si oui, dans quel message) ?

---

### Livrables de l'Atelier 2

**Livrable 1 — Configuration commentée Mosquitto (fichier `secure.conf`)** avec les explications de chaque directive.

**Livrable 2 — Capture Wireshark annotée** montrant :
- Une capture port 1883 avec les données en clair visibles et annotées
- Une capture port 8883 avec les données chiffrées + le handshake mTLS identifié

**Livrable 3 — Réponses aux questions** de chaque phase (intégrées dans un rapport de 2 pages maximum).

---

### Grille d'évaluation de l'Atelier 2 (observation formative — non noté séparément)

| Critère | Indicateurs de réussite |
|---|---|
| **PKI générée correctement** | CA auto-signée, certificat serveur et client signés par la CA, vérification `openssl verify` = OK |
| **Mosquitto configuré en mTLS** | Port 8883 actif, port 1883 désactivé, `require_certificate true` |
| **Rejet du client non autorisé** | Message d'erreur documenté pour connexion sans certificat |
| **Analyse Wireshark** | Comparaison avant/après pertinente, chiffrement démontré, handshake identifié |
| **Livrables clairs** | Configuration commentée, captures annotées, réponses précises |

---

## Étude de cas — Mise en conformité IEC 62443 & debriefing Atelier 2 {#etude-de-cas}

### Contexte : MecaProd et la conformité IEC 62443 SL-2

Suite à l'attaque EKANS, MecaProd souhaite se mettre en conformité avec IEC 62443 au niveau SL-2 sur ses zones critiques. L'objectif est de résister à des attaquants disposant de moyens limités utilisant des outils génériques (le cas de l'attaque initiale : RDP sans MFA + credentials compromis).

### Analyse de l'écart (Gap Analysis) avant/après

| Exigence IEC 62443-3-3 | État avant attaque | État cible SL-2 |
|---|---|---|
| **FR1 — Authentification** | RDP sans MFA, Modbus sans auth | MFA sur tous les accès distants, certificats mTLS sur MQTT |
| **FR2 — Moindre privilège** | Comptes admin partagés, accès non contrôlés | Comptes nominatifs, RBAC, séparation IT/OT |
| **FR3 — Intégrité** | Programmes PLC non signés | Sauvegarde signée des programmes, vérification avant déploiement |
| **FR4 — Confidentialité** | Modbus/TCP en clair, MQTT port 1883 | Chiffrement TLS sur les nouveaux flux, segmentation pour les anciens |
| **FR5 — Flux restreints** | Réseau plat IT/OT | DMZ industrielle, firewall OT, VLAN séparés |
| **FR6 — Détection** | Aucun IDS, aucun SIEM | IDS passif réseau OT (Claroty/Nozomi), logs centralisés |
| **FR7 — Disponibilité** | PAS de redondance SCADA | SCADA redondant, backup PLC, PRA testé |

### Plan de mise en conformité — 3 phases

**Phase 1 — Quick wins (0 à 3 mois) :**
- Activer MFA sur tous les accès VPN et RDP
- Désactiver le port 1883 sur les brokers MQTT existants → migrer vers 8883
- Segmenter IT et OT par un firewall (même une règle de blocage globale est un premier pas)
- Sauvegarder tous les programmes PLC
- Changer tous les mots de passe par défaut des équipements OT

**Phase 2 — Architecture (3 à 12 mois) :**
- Déployer une DMZ industrielle avec deux firewalls (IT-DMZ et DMZ-OT)
- Mettre en place une PKI industrielle et déployer mTLS sur les nouveaux flux
- Déployer un IDS réseau OT passif (port SPAN)
- Mettre en place une gestion centralisée des logs OT
- Qualifier et déployer les patches OT critiques sur les équipements non couverts

**Phase 3 — Conformité et certification (12 à 36 mois) :**
- Réaliser une évaluation formelle IEC 62443-3-2 (PSSA) avec un auditeur qualifié
- Atteindre SL-2 sur les zones Supervision et Contrôle
- Établir un CSMS (Cyber Security Management System) documenté
- Former les équipes OT (maintenance, opérateurs) à la cybersécurité
- Planifier des audits périodiques (annuels)

---

## Synthèse du Jour 3

### Points clés à retenir

1. **IEC 62443 est la référence OT** : elle structure la sécurité en zones et conduits, définit 4 Security Levels et 7 Foundational Requirements. ISO 27001 est complémentaire (gouvernance) mais insuffisante seule pour l'OT.

2. **SL-2 est l'objectif réaliste pour la majorité des industriels** : résister à des attaquants avec des moyens limités utilisant des outils génériques — soit précisément le profil de l'attaque EKANS sur MecaProd.

3. **MQTT sur port 1883 = exposition totale des données** : toutes les valeurs de capteurs sont lisibles et modifiables par n'importe qui sur le réseau. La migration vers le port 8883 avec mTLS est une mesure critique.

4. **mTLS garantit l'authentification mutuelle** : contrairement à TLS standard (qui n'authentifie que le serveur), mTLS exige que chaque client présente un certificat valide. Un équipement non enrôlé dans la PKI est automatiquement rejeté.

5. **Une PKI se gère dans le temps** : l'émission des certificats n'est que le début. La surveillance des expirations, la révocation en cas de compromission et la rotation périodique sont indispensables.

6. **Les équipements IIoT contraints ne peuvent pas tous supporter TLS** : des mesures compensatoires (segmentation réseau, VLAN dédié, passerelle de sécurité) sont alors nécessaires pour réduire l'exposition.

### Passerelle vers le Jour 4

Le **Jour 4** approfondira la **défense en profondeur** (Module 6) avec les firewalls industriels, la segmentation réseau avancée, les IDS OT et la supervision SIEM. L'Atelier 3 simulera un incident ransomware complet (scénario EKANS) avec analyse forensique de logs Windows et rédaction d'un rapport d'incident.

Pour préparer le Jour 4, il est utile de comprendre :
- Ce qu'est un Windows Event Log et quels EventID sont pertinents pour la détection (4624, 4688, 7045)
- La différence entre un IDS réseau (NIDS) et un IDS hôte (HIDS)
- Ce qu'est un SIEM et comment il corrèle les événements de sécurité

---

## Ressources complémentaires

### Normes et référentiels
- **IEC 62443** — disponible sur iec.ch (payant) ; résumés gratuits sur isa.org
- **ISO/IEC 27001:2022** — disponible sur iso.org
- **NIST SP 800-82 Rev.3** — Guide to OT Security : https://doi.org/10.6028/NIST.SP.800-82r3 (gratuit)
- **ANSSI — Maîtriser la SSI pour les SI industriels** : https://www.ssi.gouv.fr/guide/maitrise-de-la-ssi-pour-les-systemes-industriels/ (gratuit)
- **ANSSI — EBIOS Risk Manager** : https://www.ssi.gouv.fr/guide/ebios-risk-manager/ (gratuit)

### Documentation technique
- **Mosquitto MQTT broker** : https://mosquitto.org/documentation/
- **OpenSSL** : https://www.openssl.org/docs/
- **Mbed TLS** (implémentation légère) : https://tls.mbed.org
- **OPC Foundation — OPC-UA Security** : https://opcfoundation.org/developer-tools/specifications-unified-architecture

### Outils de vérification PKI
```bash
# Vérifier une connexion TLS et voir le certificat présenté
openssl s_client -connect mqtt.ot.mecaprod.fr:8883 \
  -CAfile ca.crt -cert client.crt -key client.key

# Vérifier la date d'expiration d'un certificat distant
echo | openssl s_client -connect mqtt.ot.mecaprod.fr:8883 2>/dev/null \
  | openssl x509 -noout -dates

# Tester les suites TLS disponibles sur un serveur
nmap --script ssl-enum-ciphers -p 8883 192.168.20.10
```

---

*Document pédagogique SEC500 — Jour 3 · JUNIA XP 2025/2026 · Formateur : Christophe CROISANT*
*Version 1.0 — à compléter selon retours terrain lors de l'animation*
