# SEC500 — Jour 1 : Fondamentaux IT/OT & Architectures industrielles
**Cybersécurité appliquée à l'industrie 4.0**
*Mastère Chef de projet Industrie 4.0 — Année 2 · JUNIA XP 2025/2026*

---

## Sommaire

- [Module 1 — Introduction à la cybersécurité en environnement industriel](#module-1)
  - [1.1 Enjeux de la cybersécurité dans l'industrie 4.0](#11-enjeux)
  - [1.2 Différences fondamentales IT vs OT](#12-it-vs-ot)
  - [1.3 Typologies de menaces](#13-menaces)
  - [1.4 Études de cas célèbres](#14-etudes-de-cas)
- [Module 2 — Systèmes cyber-physiques & architectures distribuées](#module-2)
  - [2.1 Principes des systèmes CPS et IIoT](#21-cps-iiot)
  - [2.2 Communication M2M, edge computing, cloud industriel](#22-m2m-edge-cloud)
  - [2.3 Intelligence centralisée vs distribuée](#23-centralise-vs-distribue)
  - [2.4 Panorama des protocoles OT](#24-protocoles-ot)
  - [2.5 Risques liés à l'interconnexion IT/OT](#25-risques-interconnexion)

---

## Module 1 — Introduction à la cybersécurité en environnement industriel {#module-1}

### 1.1 Enjeux de la cybersécurité dans l'industrie 4.0 {#11-enjeux}

#### Contexte : la transformation numérique de l'industrie

L'industrie 4.0 désigne la quatrième révolution industrielle, caractérisée par la convergence entre systèmes de production physiques et technologies numériques. Elle repose sur quatre piliers fondamentaux :

- **Interconnexion** — machines, capteurs, systèmes d'information en réseau continu
- **Transparence de l'information** — collecte massive de données de production (data lakes, digital twins)
- **Assistance technique** — aide à la décision, maintenance prédictive, systèmes autonomes
- **Décisions décentralisées** — les équipements prennent des décisions locales en temps réel

Cette transformation génère une **surface d'attaque radicalement élargie** : chaque capteur connecté, chaque passerelle IT/OT, chaque accès distant est un vecteur potentiel d'intrusion.

#### Pourquoi la cybersécurité industrielle est-elle critique ?

Contrairement aux systèmes IT classiques où une intrusion compromet principalement des **données**, une cyberattaque sur un système industriel peut :

1. **Provoquer des dommages physiques** — endommagement d'équipements, destruction d'infrastructure
2. **Mettre en danger des vies humaines** — accidents industriels, désactivation de systèmes de sécurité (SIS)
3. **Paralyser la production** — pertes financières directes, ruptures de chaîne d'approvisionnement
4. **Impacter des infrastructures critiques** — énergie, eau, transports, santé

> **Chiffres clés** (sources : IBM X-Force, Claroty, 2023–2024)
> - Les incidents de cybersécurité OT ont augmenté de **140 %** entre 2020 et 2023
> - Le coût moyen d'un incident industriel dépasse **4,5 M€**
> - **72 %** des entreprises industrielles ont subi au moins un incident OT significatif en 2023
> - Délai moyen de détection d'une intrusion OT : **200 jours**

#### Secteurs les plus exposés

| Secteur | Risque principal | Exemple d'impact |
|---|---|---|
| Énergie / Utilities | Sabotage d'infrastructure nationale | Blackout, rupture d'alimentation en eau |
| Industrie manufacturière | Arrêt de production, sabotage qualité | Perte de production, rappels produits |
| Chimie / Pharmaceutique | Modification de formulations, accidents | Risque environnemental, humain |
| Transport / Logistique | Perturbation de flux, blocage de ports | Paralysie de la chaîne d'approvisionnement |
| Agroalimentaire | Contamination, altération de process | Risque sanitaire, rappels massifs |

---

### 1.2 Différences fondamentales IT vs OT {#12-it-vs-ot}

#### La triade CIA revisitée

La sécurité de l'information repose classiquement sur la triade **CIA** (Confidentiality – Integrity – Availability). Les priorités divergent radicalement selon le contexte :

| Priorité | Environnement IT | Environnement OT |
|---|---|---|
| **1er** | Confidentialité | **Disponibilité** |
| **2ème** | Intégrité | **Intégrité** |
| **3ème** | Disponibilité | Confidentialité |

> **Raisonnement OT :** un automate qui s'arrête, même pour un patch de sécurité, peut coûter des dizaines de milliers d'euros par heure. La confidentialité des valeurs de registres Modbus d'un four industriel est peu critique ; son arrêt intempestif l'est.

À cette triade, les environnements OT ajoutent deux dimensions :

- **Sûreté (Safety)** — prévention des atteintes physiques aux personnes et à l'environnement
- **Fiabilité (Reliability)** — continuité du service de production

#### Tableau comparatif IT vs OT

| Critère | IT classique | OT industriel |
|---|---|---|
| **Priorité principale** | Confidentialité des données | Disponibilité du processus |
| **Cycles de vie des équipements** | 3 à 5 ans | 15 à 30 ans |
| **Mises à jour / patches** | Fréquentes, automatisables | Rares, validation constructeur requise |
| **Temps réel** | Non critique | Critique (ms à s) |
| **Tolérance aux arrêts** | Haute (redémarrage accepté) | Faible à nulle (24/7) |
| **Protocoles** | TCP/IP, HTTP/S, TLS | Modbus, S7comm, OPC-UA, PROFINET |
| **Antivirus / EDR** | Standard | Souvent impossible (CPU limité) |
| **Authentification** | Généralisée | Rare ou absente dans les protocoles natifs |
| **Chiffrement** | Généralisé | Quasi absent sur les anciens équipements |
| **Tests de sécurité** | Réguliers (pentest, audit) | Risqués (peuvent crasher l'équipement) |
| **Personnel de sécurité** | RSSI, SOC dédié | Souvent absent (géré par la maintenance) |

#### Les systèmes de contrôle industriel (ICS)

Un **ICS (Industrial Control System)** est l'ensemble des systèmes et équipements qui surveillent et contrôlent les processus industriels. Il comprend plusieurs sous-catégories :

**SCADA — Supervisory Control and Data Acquisition**
- Supervision centralisée d'infrastructures étendues (pipeline, réseau électrique)
- Collecte de données en temps réel, commandes à distance
- Interfaces HMI pour les opérateurs

**DCS — Distributed Control System**
- Contrôle distribué de processus continus (raffinerie, chimie)
- Intelligence déportée dans les contrôleurs de terrain
- Communication par bus de terrain (PROFIBUS, FOUNDATION Fieldbus)

**PLC/API — Programmable Logic Controller / Automate Programmable Industriel**
- Unité de contrôle locale d'un équipement ou d'une machine
- Traitement d'entrées/sorties (capteurs → actionneurs) en temps cyclique (ms)
- Langages IEC 61131-3 : Ladder, FBD, SFC, ST, IL

**SIS — Safety Instrumented System**
- Systèmes de mise en sécurité indépendants du processus
- Objectif : ramener le processus à un état sûr en cas de danger (ex. : fermeture d'une vanne, arrêt d'urgence)
- Norme IEC 61511 — niveaux SIL 1 à 4
- **Cible prioritaire des attaquants souhaitant causer des dommages physiques** (cf. Triton)

**HMI — Human Machine Interface**
- Interface opérateur pour visualiser et interagir avec le processus
- Souvent sous Windows (XP, 7, 10) — vecteur d'attaque majeur

#### Le modèle de Purdue (PERA)

Le **modèle de référence de Purdue** (Purdue Enterprise Reference Architecture) est le cadre de segmentation de référence des architectures industrielles. Il définit 5 niveaux hiérarchiques :

```
┌─────────────────────────────────────────────────────┐
│  Niveau 4 — Entreprise / IT                         │
│  ERP, CRM, messagerie, infrastructure bureautique   │
├─────────────────────────────────────────────────────┤
│               ↕  DMZ industrielle                   │
├─────────────────────────────────────────────────────┤
│  Niveau 3 — MES / Opérations de production          │
│  MES, historiens de données, planification           │
├─────────────────────────────────────────────────────┤
│  Niveau 2 — Supervision (SCADA / HMI)               │
│  Postes opérateurs, serveurs SCADA, interfaces HMI  │
├─────────────────────────────────────────────────────┤
│  Niveau 1 — Contrôle (PLC / DCS / SIS)              │
│  Automates, régulateurs, systèmes de sécurité       │
├─────────────────────────────────────────────────────┤
│  Niveau 0 — Terrain (capteurs / actionneurs)        │
│  Capteurs de température, pression, débitmètres,    │
│  vérins, moteurs, vannes...                         │
└─────────────────────────────────────────────────────┘
```

> **Point critique :** La convergence IT/OT a progressivement érodé les frontières entre niveaux. Un accès RDP ouvert sur un poste SCADA (N2) qui partage un réseau plat avec les PLC (N1) annule l'isolation théorique du modèle de Purdue.

---

### 1.3 Typologies de menaces {#13-menaces}

#### Acteurs de la menace

| Acteur | Motivation | Moyens | Exemples |
|---|---|---|---|
| **États / APT** | Sabotage, espionnage, déstabilisation | Très élevés, 0-day, longue durée | Stuxnet (NSA/UNIT 8200), Sandworm (GRU) |
| **Cybercriminels** | Extorsion (ransomware), revente de données | Élevés, kits clés-en-main (RaaS) | EKANS, LockBit Industrial |
| **Hacktivistes** | Idéologique, protestation | Limités, DDoS, défacement | Attaques sur utilités après conflits |
| **Initiés malveillants** | Vengeance, corruption, négligence | Accès direct aux systèmes | 40 % des incidents impliquent un initié |
| **Compétiteurs** | Espionnage industriel | Variables | Vol de formulations, plans de production |

#### Les 5 grandes familles de menaces OT

**1. Ransomware industriel**

Le ransomware cible traditionnellement les systèmes IT (chiffrement de fichiers, extorsion). Sa variante industrielle (ex. : EKANS, Industroyer2) ajoute :
- Terminaison des processus de supervision (WinCC, InTouch, Proficy)
- Perturbation directe des opérations OT
- Double extorsion : chiffrement + menace de publication de données

**Vecteurs d'entrée typiques :**
- RDP exposé sur Internet (port 3389)
- Phishing ciblé (spear-phishing) sur les équipes maintenance/IT
- VPN non patchés (Fortinet, Pulse Secure — CVE critiques 2020–2023)
- Supply chain (mise à jour logicielle compromise)

**2. APT (Advanced Persistent Threat)**

Campagne longue durée (mois à années) conduite par des acteurs étatiques :
- Phase 1 — Reconnaissance : OSINT, Shodan, spear-phishing
- Phase 2 — Intrusion initiale : exploitation d'une vulnérabilité, phishing
- Phase 3 — Persistence : backdoor, compte fantôme, rootkit
- Phase 4 — Mouvement latéral : propagation vers le réseau OT
- Phase 5 — Mission : sabotage, collecte de renseignement, attente

**3. Sabotage de processus**

Modification malveillante de paramètres de production :
- Altération de consignes (température, pression, débit) → accident physique
- Modification de programme PLC → comportement anormal de la machine
- Désactivation de systèmes de sécurité (SIS) → zone de danger

**4. Écoute passive (sniffing)**

Sur les réseaux OT non chiffrés (Modbus, S7comm), une capture passive révèle :
- Topologie réseau complète, adresses IP et MAC de tous les équipements
- Valeurs temps réel de tous les capteurs et actionneurs
- Adresses de registres et leurs consignes
- Cycles de communication et patterns opérationnels

> **L'écoute passive est totalement indétectable** : aucun paquet n'est émis, aucun log n'est généré.

**5. Déni de service (DoS/DDoS) OT**

- **Flooding réseau** : saturation de la bande passante, équipements à faible CPU incapables de traiter les requêtes légitimes → perte de contrôle du processus
- **Exploitation de vulnérabilités** : envoi de paquets malformés provoquant le crash ou le redémarrage de l'équipement (ex. : buffer overflow sur PLC)

#### La Kill Chain industrielle (ICS Cyber Kill Chain)

Adaptée du framework Lockheed Martin, la Kill Chain ICS comprend deux étapes macro :

**Étape 1 — Compromission du réseau IT**
1. Reconnaissance (OSINT, Shodan, LinkedIn)
2. Armement (préparation de l'exploit/payload)
3. Livraison (phishing, clé USB, VPN compromis)
4. Exploitation (exécution de code sur la cible initiale)
5. Installation (persistence, C2)
6. Commande & Contrôle (communication avec l'attaquant)
7. Pivot (mouvement latéral vers le réseau OT)

**Étape 2 — Action sur le réseau OT**
1. Reconnaissance OT (scan réseau, identification des équipements)
2. Développement (compréhension du processus, développement de l'attaque OT)
3. Test (validation en environnement similaire)
4. Exécution (déclenchement de l'action : sabotage, ransomware, espionnage)

---

### 1.4 Études de cas célèbres {#14-etudes-de-cas}

#### Stuxnet (2010) — La première cyberarme

**Contexte :** Programme nucléaire iranien de Natanz — centrifugeuses d'enrichissement d'uranium Siemens S7-315/S7-417.

**Mécanisme :**
- Propagation initiale via clé USB (4 zero-days Windows exploités simultanément)
- Ciblage précis : n'activait sa charge utile que sur des configurations Siemens Step 7 spécifiques
- Action : modification des fréquences des variateurs de vitesse (33 Hz → 1410 Hz → 2 Hz) sur des cycles aléatoires
- Camouflage : renvoyait des valeurs normales aux opérateurs via la HMI

**Impact :**
- ~1000 centrifugeuses détruites (sur ~5000)
- Retard estimé de 2 ans sur le programme nucléaire iranien
- **Premier malware connu à avoir produit des effets physiques irréversibles**

**Leçons :**
- L'air gap (isolation physique) n'est pas une protection absolue
- Un malware peut simuler le fonctionnement normal pendant qu'il détruit
- Les systèmes propriétaires (Step 7, Siemens) sont également vulnérables

---

#### Triton / TRISIS (2017) — L'attaque sur les SIS

**Contexte :** Pétrochimie au Moyen-Orient (probablement Arabie Saoudite — SABIC/Petro Rabigh). Contrôleurs de sécurité instrumentée **Triconex** de Schneider Electric.

**Mécanisme :**
- Compromission initiale via la zone IT, pivot vers la DMZ
- Injection d'un framework malveillant (TRITON) dans les automates de sécurité SIS
- Objectif : désactiver ou reprogrammer les systèmes de mise en sécurité d'urgence

**Découverte :** par accident — un bug dans le malware a déclenché un arrêt d'urgence automatique, alertant les ingénieurs.

**Impact :**
- Pas de dommages physiques (découverte avant l'action finale)
- Si réussi : désactivation des arrêts d'urgence → risque d'explosion, de fuite de produits toxiques, de victimes

**Leçons :**
- **Les SIS ne doivent pas être considérés comme sûrs par défaut**
- La séparation SIS / DCS est une exigence fondamentale (IEC 61511)
- Attribution à un acteur étatique (probablement lié à la Russie)

---

#### Colonial Pipeline (2021) — Ransomware sur infrastructure critique

**Contexte :** Principal pipeline de carburant de la côte Est des États-Unis (5500 miles, 45 % de l'approvisionnement en carburant de la côte Est).

**Mécanisme :**
- Vecteur initial : compte VPN sans MFA (mot de passe compromis trouvé sur le dark web)
- Ransomware **DarkSide** déployé sur le réseau IT
- L'entreprise a elle-même arrêté les systèmes OT **par précaution** (pas de compromission OT directe)

**Impact :**
- 6 jours d'arrêt du pipeline
- Pénuries d'essence sur toute la côte Est, ruées sur les stations
- Rançon payée : **4,4 M$** (75 bitcoins, partiellement récupérés par le DOJ)
- Coût total estimé : **>100 M$**

**Leçons :**
- L'IT et l'OT peuvent être indissociables sur le plan opérationnel
- L'absence de MFA sur les accès distants est une faute grave
- Le paiement de rançon ne garantit pas la reprise rapide

---

#### EKANS / Snake (2019–2020) — Ransomware OT natif

**Contexte :** Honda, Enel (électricien européen), Fresenius (santé) — 2020.

**Mécanisme :**
- Ransomware conçu spécifiquement pour les environnements industriels
- Embarque une liste de ~64 processus industriels qu'il **termine avant de chiffrer** :
  - Wonderware InTouch, GE iFIX/Proficy, Honeywell HMIWeb, Siemens WinCC
  - Services liés à Fanuc, GE Digital, ProfiSAFE
- Vérifie le domaine Active Directory avant d'agir (cible des entreprises spécifiques)

**Particularité :** Premier ransomware avec une liste de kill processes **spécifiquement OT**, signalant un acteur ayant des connaissances profondes des environnements industriels.

**Leçons :**
- Les ransomwares évoluent vers une connaissance métier poussée des cibles OT
- La supervision (WinCC, InTouch) est une cible prioritaire avant le chiffrement
- La segmentation IT/OT limite la propagation et la portée de l'attaque

---

## Module 2 — Systèmes cyber-physiques & architectures distribuées {#module-2}

### 2.1 Principes des systèmes CPS et IIoT {#21-cps-iiot}

#### Systèmes cyber-physiques (CPS)

Un **système cyber-physique (CPS — Cyber-Physical System)** est un système dans lequel des composants informatiques et des processus physiques sont étroitement intégrés et s'influencent mutuellement.

**Définition formelle :** "Systèmes dans lesquels des réseaux de calcul et de communication interagissent avec le monde physique." — National Science Foundation (USA)

**Composants d'un CPS :**

```
  Monde physique          Réseau cyber
  ┌────────────┐         ┌────────────────┐
  │ Capteurs   │ ──────> │ Traitement     │
  │ Actionneurs│ <────── │ Décision       │
  │ Processus  │         │ Communication  │
  └────────────┘         └────────────────┘
        ↑                        ↑
        └────────────────────────┘
             Boucle fermée
```

**Exemples de CPS industriels :**
- Bras robotiques de soudure (automobile)
- Systèmes de contrôle de turbines (énergie)
- Lignes d'embouteillage automatisées (agro-alimentaire)
- Réseaux de distribution d'eau intelligents

#### IIoT — Industrial Internet of Things

L'**IIoT** est l'application de l'IoT (Internet of Things) aux environnements industriels. Il se caractérise par :

- **Densité** — des milliers à des millions de capteurs sur un même site industriel
- **Hétérogénéité** — capteurs, passerelles, PLC, HMI, serveurs, cloud
- **Contraintes embarquées** — CPU limité, mémoire faible, batterie, connectivité intermittente
- **Longévité** — durée de vie > 10–20 ans pour les équipements de terrain

**Protocoles typiques IIoT :**

| Protocole | Usage | Port | Sécurité native |
|---|---|---|---|
| **MQTT** | Messagerie publish/subscribe légère | 1883 (TCP), 8883 (TLS) | Aucune par défaut |
| **CoAP** | REST pour contraints (UDP) | 5683 (UDP) | DTLS optionnel |
| **AMQP** | Messagerie enterprise IoT | 5672 / 5671 (TLS) | TLS supporté |
| **OPC-UA** | Standard de communication industrielle | 4840 | Chiffrement intégré |
| **Modbus/TCP** | Automates, capteurs terrain | 502 | Aucune |

#### IIoT et surface d'attaque

Chaque dispositif IIoT connecté représente un vecteur d'attaque potentiel pour plusieurs raisons structurelles :

1. **Firmware non patchable** — cycle de mise à jour inexistant ou trop long, CVE non corrigées
2. **Credentials par défaut** — admin/admin, root/root, non changés après installation
3. **Protocoles sans authentification** — MQTT sur port 1883 sans user/password ni TLS
4. **Accès physique** — interfaces JTAG/UART exposées pour la maintenance
5. **Ressources insuffisantes** — impossible de faire tourner un agent de sécurité sur 256 Ko de RAM

> **Illustration :** Un capteur de température IIoT bon marché, connecté au réseau OT, utilise un firmware vieux de 5 ans avec une vulnérabilité connue sur son stack HTTP. Il est accessible depuis le réseau de supervision via une mauvaise règle de firewall. Il devient la porte d'entrée vers les PLC.

---

### 2.2 Communication M2M, edge computing, cloud industriel {#22-m2m-edge-cloud}

#### Communication M2M (Machine-to-Machine)

La communication **M2M** désigne l'échange automatisé de données entre équipements industriels, sans intervention humaine. Elle s'appuie sur :

**Bus de terrain (Fieldbus) — niveau terrain/contrôle :**
- **PROFIBUS** — Siemens, RS-485, jusqu'à 12 Mbit/s
- **CANopen** — automobile, machines, 1 Mbit/s
- **DeviceNet** — Allen-Bradley, topologie bus
- **FOUNDATION Fieldbus** — pétrochimie, process continu

**Réseaux industriels Ethernet — niveau supervision :**
- **PROFINET** — Siemens, Ethernet temps réel (IRT : < 1 ms de jitter)
- **EtherNet/IP** — Rockwell/Allen-Bradley, CIP protocol
- **Modbus/TCP** — couche application Modbus sur TCP/IP standard
- **EtherCAT** — automation ultra-rapide, < 100 µs de cycle

**Réseaux OT longue portée :**
- **WirelessHART** — capteurs process sans fil, 802.15.4
- **ISA 100.11a** — standard IEC pour réseaux sans fil industriels
- **5G privé** — couverture d'usine, faible latence (< 10 ms)

#### Edge Computing industriel

L'**edge computing** déporte une partie du traitement des données au plus près de la source (capteur, machine, atelier), réduisant la dépendance au cloud central.

```
  Capteur/Machine          Edge Node              Cloud
  ┌────────────┐         ┌───────────┐         ┌─────────┐
  │ Donnée     │ ──────> │ Filtrage  │ ──────> │ Analyse │
  │ brute      │         │ Agrégation│         │ longue  │
  │ 10 kHz     │         │ ML local  │         │ durée   │
  └────────────┘         │ Alerte    │         └─────────┘
                         │ immédiate │
                         └───────────┘
                         Latence < 5 ms        Latence > 100 ms
```

**Avantages de l'edge computing :**
- Latence très faible pour les décisions temps réel (détection d'anomalie, arrêt d'urgence)
- Réduction du volume de données transmises au cloud (coût, bande passante)
- Fonctionnement en mode dégradé si la connexion cloud est coupée
- Données sensibles traitées localement (conformité RGPD, propriété industrielle)

**Risques de sécurité spécifiques :**
- **Compromission physique** — l'edge node est dans l'atelier, accessible physiquement
- **Pivot réseau** — un edge node compromis est sur le réseau OT → accès aux PLC
- **Mise à jour difficile** — déployé dans des endroits peu accessibles, firmware obsolète
- **Surface d'attaque logicielle** — Linux embarqué avec services inutiles actifs (SSH, HTTP)

#### Cloud industriel

Le **cloud industriel** offre des services d'hébergement, d'analyse et de gestion des données de production à l'échelle :

**Cas d'usage :** digital twins, maintenance prédictive, optimisation énergétique, reporting MES/ERP.

**Modèles de déploiement :**

| Modèle | Description | Risque principal |
|---|---|---|
| **Cloud public** | AWS IoT, Azure IoT Hub, Google Cloud IoT | Données OT exposées hors site, dépendance |
| **Cloud privé** | Infrastructure dédiée on-premise | Coût élevé, compétences internes nécessaires |
| **Cloud hybride** | Mix public/privé selon sensibilité des données | Complexité de gouvernance |
| **Multi-cloud** | Plusieurs fournisseurs | Intégration, cohérence sécurité |

**Vecteurs d'attaque cloud industriel :**
- Credentials API volés (secrets dans le code source, GitHub leaks)
- Mauvaise configuration des buckets de stockage (S3 public, Azure Blob ouvert)
- Token d'accès IoT hub compromis → injection de commandes sur les équipements terrain

---

### 2.3 Intelligence centralisée vs distribuée {#23-centralise-vs-distribue}

#### Architecture centralisée

Toute l'intelligence de décision est concentrée dans un système central (SCADA, DCS maître).

**Avantages :**
- Vue globale du processus, cohérence des décisions
- Sécurité centralisable (un seul point à sécuriser)
- Auditabilité centralisée des actions

**Inconvénients :**
- **Single point of failure** — si le système central est compromis ou tombe, tout s'arrête
- Latence pour les décisions de terrain
- Scalabilité limitée

#### Architecture distribuée

L'intelligence est répartie entre de nombreux équipements autonomes (PLC décentralisés, edge nodes, robots collaboratifs).

**Avantages :**
- Résilience — la défaillance d'un nœud n'impacte pas l'ensemble
- Faible latence pour les décisions locales
- Scalabilité (ajout de nœuds sans refonte centrale)

**Inconvénients :**
- **Surface d'attaque démultipliée** — chaque nœud est un vecteur potentiel
- Cohérence des configurations de sécurité difficile à maintenir
- Détection d'incidents complexifiée (logs distribués)

#### Implications de sécurité

```
Architecture centralisée     Architecture distribuée
         │                            │
         ▼                            ▼
  Protéger 1 point            Protéger N points
  fort → Zero Trust            chacun exposé
  sur ce point                 → Défense en profondeur
```

**Principe de défense adapté :**
- Architecture centralisée → focus sur la résilience du point central, MFA, backups
- Architecture distribuée → segmentation, least privilege, inventaire exhaustif, supervision des nœuds

---

### 2.4 Panorama des protocoles OT {#24-protocoles-ot}

#### Modbus (1979)

- **Origine :** Modicon (1979) — protocole maître/esclave pour automates
- **Versions :** Modbus RTU (RS-232/485, binaire), Modbus ASCII, **Modbus/TCP** (port 502)
- **Fonctionnement :** le maître interroge les esclaves via des Function Codes (FC)

**Function Codes principaux :**

| FC | Nom | Opération | Risque |
|---|---|---|---|
| 01 | Read Coils | Lecture sorties digitales | Lecture |
| 02 | Read Discrete Inputs | Lecture entrées digitales | Lecture |
| 03 | Read Holding Registers | Lecture registres | Lecture (valeurs process) |
| 04 | Read Input Registers | Lecture registres d'entrée | Lecture |
| **05** | Write Single Coil | Écriture sortie digitale | **Écriture — risque sabotage** |
| **06** | Write Single Register | Écriture registre | **Écriture — risque sabotage** |
| **15** | Write Multiple Coils | Écriture multiple | **Écriture — risque sabotage** |
| **16** | Write Multiple Registers | Écriture multiple | **Écriture — risque sabotage** |
| 43 | Read Device Identification | Info fabricant/modèle | Reconnaissance |

> **Absence totale d'authentification et de chiffrement** — tout équipement sur le réseau peut envoyer un FC=06 à n'importe quel PLC Modbus.

---

#### S7comm (Siemens)

- Protocole propriétaire Siemens pour les gammes S7-300/400/1200/1500
- Fonctionne sur TCP port 102 (via ISO-TSAP)
- Permet la lecture/écriture de blocs de données, le téléchargement de programmes, le contrôle de l'état de l'automate (RUN/STOP)
- **CVE-2019-13945** : écriture de programme sans authentification sur S7-1200/1500 (CVSS 9.8)

---

#### OPC-UA (OPC Unified Architecture)

- Standard ouvert de l'OPC Foundation (2008), adopté IEC 62541
- **Port :** 4840 (TCP), 4843 (HTTPS)
- Orienté données et services, multi-plateforme
- **Sécurité native** : chiffrement TLS, authentification par certificats X.509, contrôle d'accès basé sur les rôles
- Principal protocole recommandé pour les nouvelles architectures IIoT sécurisées
- **Attention :** la sécurité OPC-UA n'est garantie que si le mode "None" (sans chiffrement) est désactivé

---

#### MQTT (Message Queuing Telemetry Transport)

- Protocole publish/subscribe créé par IBM (1999), standardisé OASIS en 2014
- **Port :** 1883 (TCP non sécurisé), 8883 (TLS)
- Architecture : broker central, clients publishers, clients subscribers
- **Adapté** aux environnements contraints (faible bande passante, connectivité intermittente)
- **Par défaut, pas d'authentification ni de chiffrement** → MQTT sur port 1883 en clair est une vulnérabilité majeure
- **MQTTs** : MQTT over TLS — standard pour les déploiements sécurisés

---

#### PROFINET / EtherNet/IP

- Protocoles Ethernet industriels temps réel pour les réseaux de terrain
- Basés sur Ethernet standard (802.3), ajoutent des mécanismes de QoS et de temps réel
- Pas de chiffrement natif dans la plupart des implémentations
- Vulnérables aux attaques réseau classiques (ARP spoofing, flooding)

---

### 2.5 Risques liés à l'interconnexion IT/OT {#25-risques-interconnexion}

#### La convergence IT/OT : opportunité et risque

La convergence IT/OT est motivée par des gains opérationnels réels :
- Visibilité en temps réel de la production depuis le SI d'entreprise
- Maintenance prédictive alimentée par les données machine
- Optimisation logistique (synchronisation production/ERP)
- Pilotage énergétique en temps réel

Mais elle crée un **continuum de connectivité** qui efface les frontières historiques de sécurité :

```
Internet → VPN/RDP → Réseau IT → DMZ (??) → Réseau OT → PLC/SCADA
```

Sans segmentation rigoureuse, une compromission à l'entrée du réseau IT se propage librement jusqu'aux automates.

#### Vecteurs de convergence les plus risqués

**1. Accès distants non sécurisés**
- RDP sans MFA exposé sur Internet (port 3389)
- VPN avec credentials partagés entre IT et OT
- Jump server sans surveillance ni enregistrement de session

**2. Réseaux plats (flat networks)**
- IT et OT sur le même VLAN / même sous-réseau
- Absence de firewall entre les niveaux Purdue
- PLC accessibles depuis les postes bureautiques

**3. Médias amovibles**
- Clés USB utilisées pour transférer des programmes PLC → vecteur de malware (Stuxnet)
- Laptops de maintenance connectés alternativement au réseau IT et au réseau OT

**4. Mises à jour à distance**
- Accès fournisseur via VPN dédié non surveillé
- Téléchargement de firmware sans vérification d'intégrité

**5. Historiens de données (Data Historians)**
- Serveurs (ex. OSIsoft PI, Aveva) connectés simultanément au réseau OT et au réseau IT/entreprise
- Si compromis → pivot parfait entre IT et OT

#### Principes de réduction du risque (aperçu — approfondi Jour 4)

Ces principes seront développés en détail lors du Module 6 (Jour 4), mais il est important d'en établir les fondements dès Jour 1 :

| Principe | Description |
|---|---|
| **Segmentation réseau** | Séparer physiquement ou logiquement IT et OT par des firewalls industriels |
| **DMZ industrielle** | Zone tampon entre IT et OT pour les flux de données légitimes (historiens, MES) |
| **Least privilege** | Chaque utilisateur et système n'accède qu'aux ressources strictement nécessaires |
| **Zero Trust** | "Ne jamais faire confiance, toujours vérifier" — même pour le trafic interne |
| **Inventaire continu** | Cartographie exhaustive et à jour de tous les équipements OT |
| **MFA sur les accès distants** | Authentification multi-facteurs obligatoire pour tout accès VPN/RDP/jump server |

---

## Synthèse du Jour 1

### Points clés à retenir

1. **La triade CIA est inversée en OT** : Disponibilité > Intégrité > Confidentialité. Un arrêt non planifié est souvent plus grave qu'une fuite de données.

2. **Les protocoles OT (Modbus, S7comm) ont été conçus sans sécurité** : pas d'authentification, pas de chiffrement, pas d'audit natif. Tout équipement sur le réseau peut interagir avec les automates.

3. **Le modèle de Purdue définit 5 niveaux** (0 terrain → 4 IT entreprise). Les PLC sont au Niveau 1, la supervision (SCADA/HMI) au Niveau 2. La convergence IT/OT érode ces frontières.

4. **Stuxnet, Triton, Colonial Pipeline et EKANS** sont les quatre cas de référence illustrant les quatre familles de menaces : cyberarme étatique, attaque sur SIS, ransomware IT→OT, ransomware OT natif.

5. **L'IIoT multiplie la surface d'attaque** : chaque capteur connecté est un vecteur potentiel avec firmware non patchable et credentials par défaut.

6. **L'edge computing réduit la latence et l'exposition cloud** mais déplace le risque vers les équipements de terrain (compromission physique, pivot réseau OT).

### Préparation pour le Jour 2

Le **Jour 2** portera sur les vulnérabilités concrètes et les outils d'audit (Module 3). Pour y aborder les ateliers pratiques (Nmap OT, Wireshark, Shodan), il est recommandé de :

- Mémoriser les Function Codes Modbus critiques (FC=01, 03, 05, 06, 43)
- Connaître le port Modbus/TCP (502) et OPC-UA (4840)
- Comprendre la différence entre écoute passive (sniffing) et scan actif (Nmap)
- Savoir pourquoi une commande FC=06 mal utilisée peut avoir des conséquences physiques

---

## Ressources complémentaires

### Références normatives et institutionnelles
- **IEC 62443** — Norme de sécurité des systèmes d'automatisation et de contrôle industriels
- **ANSSI — Guide de l'hygiène informatique** (applicable OT) : https://www.ssi.gouv.fr
- **ANSSI — Maîtriser la SSI pour les systèmes industriels** : https://www.ssi.gouv.fr/guide/maitrise-de-la-ssi-pour-les-systemes-industriels/
- **CISA — ICS Security** : https://www.cisa.gov/ics
- **NIST SP 800-82 Rev.3** — Guide to Operational Technology (OT) Security

### Frameworks d'attaque ICS
- **MITRE ATT&CK for ICS** : https://attack.mitre.org/matrices/ics/ — matrice des techniques d'attaque spécifiques OT
- **ICS Cyber Kill Chain** (Assante & Lee, SANS 2015)

### Veille sécurité OT
- **CERT-FR** (alertes et avis) : https://www.cert.ssi.gouv.fr
- **Dragos Year in Review** (rapport annuel OT threats)
- **Claroty Biannual ICS Risk & Vulnerability Report**
- **SCADAfence Blog** (actualité des vulnérabilités OT)

---

*Document pédagogique SEC500 — Jour 1 · JUNIA XP 2025/2026 · Formateur : Christophe CROISANT*
*Version 1.0 — à compléter selon retours terrain lors de l'animation*
