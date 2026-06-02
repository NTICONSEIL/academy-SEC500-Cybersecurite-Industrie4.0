# SEC500 — Jour 2 : Vulnérabilités industrielles & audit de sécurité
**Cybersécurité appliquée à l'industrie 4.0**
*Mastère Chef de projet Industrie 4.0 — Année 2 · JUNIA XP 2025/2026*

---

## Sommaire

- [Module 3 — Vulnérabilités des systèmes industriels & audit OT](#module-3)
  - [3.1 Composants critiques et leurs vulnérabilités](#31-composants-critiques)
  - [3.2 CVE OT emblématiques et scores CVSS](#32-cve-ot)
  - [3.3 Scénarios d'attaque typiques](#33-scenarios-attaque)
  - [3.4 Matrice de risques OT](#34-matrice-risques)
- [Outils d'audit OT](#outils-audit)
  - [4.1 Shodan — reconnaissance passive](#41-shodan)
  - [4.2 Nmap — scan actif adapté à l'OT](#42-nmap)
  - [4.3 Wireshark — analyse de trames industrielles](#43-wireshark)
- [Atelier 1 — Identification de vulnérabilités sur une architecture simulée](#atelier-1)
- [CC1 — Préparation au QCM de fin de journée](#cc1)

---

## Module 3 — Vulnérabilités des systèmes industriels & audit OT {#module-3}

### 3.1 Composants critiques et leurs vulnérabilités {#31-composants-critiques}

#### Vue d'ensemble de l'architecture cible

Avant d'identifier les vulnérabilités, il est nécessaire de comprendre quels composants constituent une architecture industrielle typique et de connaître les caractéristiques de sécurité (ou l'absence de sécurité) de chacun.

```
  Internet / WAN
       │
  ┌────┴─────────────────────────────────────────────┐
  │  Niveau 4 — Réseau IT / Entreprise               │
  │  Postes bureautiques, messagerie, ERP, AD         │
  └────┬─────────────────────────────────────────────┘
       │ (souvent sans firewall ou avec règles permissives)
  ┌────┴─────────────────────────────────────────────┐
  │  Niveau 3 — MES / Historien de données           │
  │  OSIsoft PI, Aveva, serveur MES, reporting        │
  └────┬─────────────────────────────────────────────┘
       │
  ┌────┴─────────────────────────────────────────────┐
  │  Niveau 2 — Supervision (SCADA / HMI)            │
  │  Postes Windows, WinCC, InTouch, FactoryTalk      │
  └────┬─────────────────────────────────────────────┘
       │ réseau OT (souvent plat, sans VLAN)
  ┌────┴─────────────────────────────────────────────┐
  │  Niveau 1 — Contrôle (PLC / DCS)                 │
  │  Siemens S7, Allen-Bradley, Schneider M340/M580   │
  └────┬─────────────────────────────────────────────┘
       │
  ┌────┴─────────────────────────────────────────────┐
  │  Niveau 0 — Terrain                              │
  │  Capteurs, actionneurs, variateurs, relais        │
  └──────────────────────────────────────────────────┘
```

---

#### PLC / API — Automate Programmable Industriel

**Rôle :** exécuter un programme de contrôle en boucle cyclique (scan cycle : 1 ms à 100 ms) pour lire les entrées (capteurs) et commander les sorties (actionneurs).

**Fabricants et gammes principales :**

| Fabricant | Gamme | Protocole natif | Remarque |
|---|---|---|---|
| Siemens | S7-300, S7-400, S7-1200, S7-1500 | S7comm (TCP/102), PROFINET | CVE-2019-13945 (CVSS 9.8) |
| Allen-Bradley (Rockwell) | MicroLogix, CompactLogix, ControlLogix | EtherNet/IP, CIP | CVE-2012-6435 (DoS) |
| Schneider Electric | Modicon M221, M340, M580 | Modbus/TCP, EtherNet/IP | CVE-2018-7789 (DoS, CVSS 7.5) |
| Mitsubishi | MELSEC iQ-R, iQ-F | SLMP, MC Protocol | CVE-2021-20587 (DoS) |
| ABB | AC500, AC800 | IEC 61850, Modbus | Diverses CVE sur le firmware |

**Vulnérabilités structurelles des PLC :**

1. **Absence d'authentification native** — Modbus/TCP et S7comm (versions < TLS) acceptent des commandes de n'importe quelle IP sans vérification d'identité.
2. **Firmware non patchable sans arrêt** — la mise à jour nécessite un arrêt planifié et une validation constructeur, laissant des CVE critiques actives pendant 12 à 36 mois.
3. **Ressources limitées** — CPU et mémoire insuffisants pour héberger un agent de sécurité, un antivirus ou un stack TLS complet sur les anciens modèles.
4. **Services inutiles activés** — serveur web de diagnostic HTTP (port 80/443), serveur FTP pour le transfert de programmes, serveur Telnet.
5. **Mots de passe constructeur codés en dur** — backdoors de maintenance documentées dans les guides constructeurs, parfois non modifiables.
6. **Absence de journalisation** — un PLC standard n'enregistre pas les commandes reçues. Une écriture de registre malveillante ne laisse aucune trace.

> **Point critique :** Un PLC est conçu pour être fiable et rapide, pas pour être sécurisé. La philosophie de conception est à l'opposé de celle d'un serveur IT.

---

#### HMI — Human Machine Interface

**Rôle :** interface graphique permettant aux opérateurs de visualiser l'état du processus et d'envoyer des commandes manuelles.

**Caractéristiques à risque :**
- Souvent sous **Windows XP, Windows 7 ou Windows 10** non patchés (contraintes de qualification logicielle)
- Logiciels SCADA avec des années de retard sur les patches de sécurité (WinCC, InTouch, Wonderware)
- **RDP activé** pour la maintenance à distance — vecteur d'intrusion n°1
- Connexion simultanée au réseau IT (pour les rapports) et au réseau OT (pour le process)
- Antivirus parfois désactivé (incompatibilité avec le logiciel SCADA)
- Clés USB utilisées régulièrement par les techniciens de maintenance

**CVE emblématiques HMI :**
- **CVE-2014-2908** (Siemens WinCC) — XSS et divulgation d'informations
- **CVE-2020-7580** (Siemens SIMATIC WinCC) — exécution de code arbitraire
- **CVE-2021-40394** (Inductive Automation Ignition) — RCE non authentifiée

---

#### Passerelles industrielles (Protocol Converters / Gateways)

**Rôle :** assurer la traduction de protocoles entre le réseau OT (Modbus, PROFIBUS) et le réseau IT (Ethernet, MQTT, OPC-UA).

**Exemples :** Moxa NPort, Advantech, ProSoft Technology, Kepware.

**Pourquoi elles sont dangereuses :**
- Connectées **simultanément** à deux réseaux (IT et OT) → pivot naturel
- Firmware rarement mis à jour
- Interface web d'administration souvent sans HTTPS, credentials par défaut
- Exposent des ports OT sur le réseau IT par design (Modbus/TCP visible depuis le réseau d'entreprise)

**CVE emblématiques passerelles :**
- **CVE-2020-15778** (Moxa NPort) — accès non authentifié aux paramètres de configuration
- **CVE-2019-9201** (Moxa EDR routers) — plusieurs vulnérabilités critiques (injection de commandes, buffer overflow)

---

#### Capteurs connectés et équipements IIoT de terrain

**Caractéristiques à risque :**
- Firmware figé à la livraison, sans mécanisme de mise à jour automatique
- Stack réseau minimal (pas de TLS, pas d'authentification)
- Protocoles de configuration : SNMP v1/v2 (communautés par défaut "public"/"private")
- Interfaces physiques exposées : JTAG, UART, Ethernet non protégées physiquement
- Durée de vie > 10 ans — obsolescence programmée de la sécurité

---

#### Réseau OT — les vecteurs structurels

**Réseau plat (flat network) :** l'absence de segmentation entre les niveaux Purdue signifie que tout équipement connecté peut communiquer avec tout autre. Un poste bureautique compromis peut scanner et interagir directement avec les PLC.

**Protocoles sans sécurité :** Modbus/TCP, S7comm (versions non sécurisées), PROFINET, DNP3 — aucune authentification, aucun chiffrement, aucune intégrité des messages.

**Absence de surveillance (monitoring) :** la plupart des réseaux OT ne disposent pas d'IDS (Intrusion Detection System) ni de SIEM. Une attaque peut durer des semaines sans être détectée.

---

### 3.2 CVE OT emblématiques et scores CVSS {#32-cve-ot}

#### Comprendre le score CVSS

Le **CVSS (Common Vulnerability Scoring System)** quantifie la sévérité d'une vulnérabilité sur une échelle de 0 à 10 :

| Score | Sévérité | Action recommandée |
|---|---|---|
| 9.0 – 10.0 | **Critique** | Patch immédiat ou mitigation d'urgence |
| 7.0 – 8.9 | **Élevé** | Patch prioritaire sous 30 jours |
| 4.0 – 6.9 | **Moyen** | Patch planifié sous 90 jours |
| 0.1 – 3.9 | **Faible** | Patch selon disponibilité |
| 0.0 | Aucun | Information |

Le score CVSS v3.1 est calculé à partir de trois groupes de métriques :
- **Base** : exploitabilité (vecteur d'accès, complexité, privilèges requis) × impact (confidentialité, intégrité, disponibilité)
- **Temporel** : maturité de l'exploit, disponibilité d'un correctif
- **Environnemental** : impact spécifique à l'environnement de la cible

> **Particularité OT :** Une CVE "moyenne" en IT (score 5.0) peut devenir critique en OT si elle affecte la disponibilité d'un PLC de sécurité. Le contexte métier doit toujours compléter le score CVSS brut.

#### Tableau des CVE OT de référence

| CVE | Équipement | Impact | CVSS | Vecteur |
|---|---|---|---|---|
| **CVE-2019-13945** | Siemens S7-1200/S7-1500 | Écriture de programme sans auth → contrôle total du PLC | **9.8** | Réseau, sans auth |
| **CVE-2018-7789** | Schneider Modicon M221 | DoS — redémarrage forcé du PLC par paquet malformé | **7.5** | Réseau |
| **CVE-2012-6435** | Rockwell Allen-Bradley | DoS — crash du PLC | **7.8** | Réseau |
| **CVE-2020-15778** | Moxa NPort | Accès non authentifié à la configuration | **9.1** | Réseau |
| **CVE-2021-20587** | Mitsubishi MELSEC | DoS — arrêt forcé du PLC | **7.5** | Réseau |
| **CVE-2014-2908** | Siemens WinCC | XSS + divulgation d'informations | **4.3** | Réseau |
| **CVE-2020-7580** | Siemens WinCC SIMATIC | Exécution de code arbitraire | **6.7** | Local |
| **CVE-2017-9947** | Siemens APOGEE/TALON | Lecture de fichiers arbitraires (path traversal) | **5.3** | Réseau |

#### La problématique du patching OT

Contrairement aux systèmes IT où les patches sont déployés en quelques heures, le patching OT suit un processus rigoureux qui prend du temps :

```
  Publication CVE
       │
       ▼ (0 à 6 mois)
  Développement du patch par le constructeur
       │
       ▼ (1 à 3 mois)
  Validation constructeur sur environnement de test
       │
       ▼ (1 à 6 mois)
  Qualification par l'exploitant sur un environnement représentatif
       │
       ▼ (3 à 12 mois)
  Planification de l'arrêt de production (maintenance planifiée)
       │
       ▼
  Déploiement en production
  ────────────────────────────────────────────────────
  Délai total typique : 12 à 36 mois après publication
```

**Conséquence :** Des CVE critiques (CVSS > 9.0) restent délibérément non patchées pendant un à trois ans dans les environnements de production. Les mesures compensatoires (segmentation, liste blanche applicative, surveillance) deviennent indispensables.

---

### 3.3 Scénarios d'attaque typiques {#33-scenarios-attaque}

#### Scénario 1 — Reconnaissance et écoute passive (Sniffing)

**Objectif attaquant :** cartographier le réseau OT et comprendre le processus sans être détecté.

**Prérequis :** accès au réseau OT (physiquement, ou via pivot depuis le réseau IT).

**Étapes :**

1. Connexion à un port Ethernet libre sur un switch OT (aucun contrôle d'accès 802.1X)
2. Lancement de Wireshark en mode promiscuité
3. Observation passive des trames Modbus/TCP en circulation

**Ce que l'attaquant apprend sans envoyer un seul paquet :**
- Adresses IP de tous les équipements actifs sur le réseau
- Port utilisé (502 → Modbus/TCP), identification des PLC
- Function Codes : FC=03 (lecture) → valeurs de capteurs en temps réel
- Unit ID des esclaves Modbus, adresses des registres clés
- Périodicité des cycles de polling (→ comprendre la logique de contrôle)
- Présence d'un HMI (communication régulière avec plusieurs PLC)

**Niveau de détection :** **nul** — aucun paquet émis, aucun log généré côté PLC.

---

#### Scénario 2 — Scan de reconnaissance active (Nmap)

**Objectif attaquant :** identifier les équipements, leurs fabricants, modèles et versions de firmware.

**Outils :** Nmap avec scripts NSE OT.

**Commandes types :**
```bash
# Découverte des hôtes actifs sur le sous-réseau OT
nmap -sn 192.168.10.0/24

# Scan des ports OT standards
nmap -p 102,502,1102,2222,4840,20000,44818 192.168.10.0/24

# Identification du fabricant et firmware d'un PLC Modbus
nmap --script modbus-discover -p 502 192.168.10.110

# Identification d'un automate Siemens S7
nmap --script s7-info -p 102 192.168.10.110
```

**Résultat type de modbus-discover :**
```
PORT    STATE SERVICE
502/tcp open  modbus
| modbus-discover:
|   sid 0x64:
|     Vendor Name: Schneider Electric
|     Product Code: M340
|     Major Minor Revision: 2.6
|_  sid 0x65: <no data>
```

> **Attention :** un scan Nmap avec des options agressives (-T4, -T5, --script vuln) peut **crasher** un PLC à faible CPU. Toujours utiliser -T2 sur un réseau OT actif. Obtenir une autorisation écrite avant tout scan.

---

#### Scénario 3 — Attaque Man-in-the-Middle (MitM) sur Modbus/TCP

**Objectif attaquant :** intercepter et modifier les communications entre le HMI et le PLC.

**Prérequis :** accès au même réseau que le HMI et le PLC (réseau plat, pas de 802.1X).

**Étapes :**

1. **ARP Spoofing** — empoisonnement du cache ARP du HMI et du PLC pour intercepter le trafic :
   ```bash
   arpspoof -i eth0 -t 192.168.10.100 192.168.10.110  # Tromper le HMI
   arpspoof -i eth0 -t 192.168.10.110 192.168.10.100  # Tromper le PLC
   ```
2. **Activation du forwarding IP** — pour ne pas bloquer le trafic légitime
3. **Capture et analyse** des trames Modbus en transit avec Wireshark
4. **Modification des trames** à la volée (injection de commandes d'écriture)

**Pourquoi c'est facile sur Modbus/TCP :**
- Pas d'authentification → impossible de distinguer une commande légitime d'une commande forgée
- Pas de chiffrement → les valeurs sont lisibles en clair
- Pas d'intégrité des messages → modification sans détection
- Pas de séquencement strict → rejeu de commandes possibles

---

#### Scénario 4 — Falsification de registre (Write Register Attack)

**Objectif attaquant :** modifier une consigne de processus pour provoquer un dysfonctionnement ou un accident.

**Commande Modbus — Write Single Register (FC=06) :**
```
Transaction ID : 0x0001
Protocol ID    : 0x0000 (Modbus)
Length         : 0x0006
Unit ID        : 0x01
Function Code  : 0x06 (Write Single Register)
Register addr  : 0x0064 (registre 100 → ex. consigne température)
Register value : 0x270F (9999 → valeur extrême)
```

**Exemples d'impact selon le registre ciblé :**

| Registre | Valeur légitime | Valeur injectée | Impact potentiel |
|---|---|---|---|
| Consigne température four | 850 °C | 9999 | Surchauffe → incendie, dommage équipement |
| Consigne vitesse moteur | 1500 tr/min | 9000 | Destruction mécanique, éclatement |
| Consigne pression | 6 bar | 150 bar | Explosion de canalisation |
| Consigne dosage produit | 0.5 L/cycle | 50 L/cycle | Contamination produit, déversement |
| État vanne (ouvert/fermé) | 0 (fermée) | 1 (ouverte) | Déversement, inondation |

> **Point clé :** une commande logicielle envoyée via le réseau peut avoir des conséquences physiques irréversibles en quelques secondes. C'est la spécificité fondamentale de la cybersécurité OT.

---

#### Scénario 5 — Intrusion via RDP et pivot vers l'OT

**Objectif attaquant :** obtenir un accès complet au réseau OT à partir d'Internet.

**Architecture vulnérable type (MecaProd) :**
```
Internet → [RDP 3389] → PC SCADA (Windows 10 non patchné)
                             │
                       Réseau OT plat
                      /      │       \
                  PLC1      PLC2     PLC3
               (Modbus)  (Modbus)  (S7comm)
```

**Étapes de l'attaque :**

1. **Reconnaissance Shodan** : `port:3389 "Windows 10" country:FR` → liste des RDP exposés
2. **Brute force / credential stuffing** : essai de credentials compromis (HaveIBeenPwned, dark web)
3. **Accès RDP** : session ouverte sur le PC SCADA avec les credentials trouvés
4. **Reconnaissance interne** : `nmap -sn 192.168.10.0/24` depuis le PC SCADA → cartographie OT
5. **Interaction avec les PLC** : utilisation directe du logiciel SCADA installé (WinCC, InTouch) ou d'outils Modbus
6. **Déploiement ransomware** : chiffrement du PC SCADA + tentative de propagation via le réseau OT

**C'est exactement le scénario MecaProd (EKANS, Valenciennes)** — vecteur RDP exposé sans MFA.

---

### 3.4 Matrice de risques OT {#34-matrice-risques}

#### Construction d'une matrice de risques

Une matrice de risques croise la **probabilité** d'occurrence d'une menace avec son **impact** (financier, humain, opérationnel) :

```
         │ Impact
         │  Faible  │  Moyen   │  Élevé   │ Critique
─────────┼──────────┼──────────┼──────────┼──────────
Probable │    ■     │    ■■    │   ■■■    │  ■■■■
─────────┼──────────┼──────────┼──────────┼──────────
Possible │    □     │    ■     │   ■■■    │  ■■■■
─────────┼──────────┼──────────┼──────────┼──────────
Rare     │    □     │    □     │    ■     │  ■■■
─────────┼──────────┼──────────┼──────────┼──────────
P
r
o
b
a
b
i
l
i
t
é
         ■■■■ = Critique / traiter en urgence
         ■■■  = Élevé / traiter prioritairement
         ■■   = Moyen / planifier le traitement
         ■    = Faible / surveiller
         □    = Négligeable / accepter
```

#### Matrice de risques OT — exemple pour MecaProd

| Risque | Probabilité | Impact | Niveau | Vulnérabilité associée |
|---|---|---|---|---|
| Ransomware via RDP exposé | Probable | Critique | **Critique** | RDP sans MFA sur SCADA |
| Écoute passive réseau Modbus | Probable | Élevé | **Critique** | Réseau plat, Modbus en clair |
| Falsification de registre PLC | Possible | Critique | **Critique** | Modbus sans authentification |
| DoS sur PLC via scan agressif | Possible | Élevé | **Élevé** | CVE firmware non patché |
| Compromission passerelle OT/IT | Possible | Critique | **Critique** | Credentials par défaut |
| Accès physique non autorisé | Rare | Élevé | **Élevé** | Absence de contrôle d'accès physique |
| Infection USB par technicien | Possible | Élevé | **Élevé** | Pas de politique USB |
| Attaque supply chain (logiciel) | Rare | Critique | **Élevé** | Absence de vérification d'intégrité |

---

## Outils d'audit OT {#outils-audit}

### 4.1 Shodan — reconnaissance passive {#41-shodan}

#### Présentation de Shodan

**Shodan** (https://www.shodan.io) est un moteur de recherche qui indexe les équipements connectés à Internet en effectuant ses propres scans de manière continue. Contrairement à Google qui indexe les pages web, Shodan indexe les **bannières de services** répondant sur les ports TCP/UDP.

**Fonctionnement :**
- Des crawlers Shodan scannent en permanence l'ensemble de l'espace d'adressage IPv4 (et IPv6)
- Pour chaque port ouvert, ils collectent la bannière de réponse (version, OS, info équipement)
- Les résultats sont indexés et consultables via l'interface web ou l'API

**Usage en audit OT :**
Shodan est utilisé en **phase de reconnaissance passive** — l'auditeur consulte les résultats sans interagir directement avec la cible. C'est une technique **OSINT (Open Source Intelligence)**.

> **Aspect légal (France) :** Consulter les résultats indexés par Shodan est légal — c'est une lecture de données publiques, au même titre que consulter un moteur de recherche. En revanche, tenter de se connecter à un équipement découvert via Shodan sans autorisation constitue un **accès frauduleux à un système informatique** (article 323-1 du Code pénal — jusqu'à 2 ans d'emprisonnement et 60 000 € d'amende). La ligne est claire : **consulter l'index = légal ; interagir avec l'équipement = illégal sans autorisation.**

---

#### Requêtes Shodan OT essentielles

**Recherche par protocole industriel :**
```
port:502                    → Modbus/TCP (automates exposés)
port:102                    → S7comm Siemens
port:4840                   → OPC-UA
port:20000                  → DNP3 (énergie, eau)
port:44818                  → EtherNet/IP (Rockwell)
port:1883                   → MQTT non sécurisé
port:47808                  → BACnet (bâtiment)
```

**Recherche par fabricant / produit :**
```
"Siemens S7-1200"           → automates Siemens S7-1200 exposés
"schneider electric"        → équipements Schneider
"GE Fanuc"                  → automates GE
"Modicon"                   → automates Schneider Modicon
"WinCC" port:102            → serveurs SCADA WinCC accessibles
```

**Recherche géographique :**
```
port:502 country:FR                     → Modbus en France
port:502 country:FR city:"Valenciennes" → Modbus à Valenciennes
port:3389 country:FR "Windows 10"       → RDP Windows 10 en France
```

**Recherche par CVE :**
```
vuln:CVE-2019-13945         → S7-1200 vulnérables à la CVE critique
vuln:CVE-2020-15778         → Moxa NPort vulnérables
```

**Opérateurs avancés :**
```
port:502 -"Authentication Required"     → Modbus sans authentification
port:1883 -password                     → MQTT sans mot de passe
net:192.168.0.0/16                      → plage d'adresses privée (résultats limités)
```

#### Lecture d'un résultat Shodan

Exemple de résultat pour un automate Modbus exposé :
```
IP: 203.0.113.42
Organization: SomeFrench Industries SAS
Country: France
City: Valenciennes
Port: 502/tcp
Banner:
  Vendor Name: Schneider Electric
  Product Code: M340 BMX P34 2020
  Firmware: V2.60
  Hardware: V1.0
  Serial: M340-XXXX-YYYY
CVEs: CVE-2018-7789 (CVSS 7.5)
Last seen: 2024-11-15
```

**Ce que cela révèle :** fabricant exact, modèle, version firmware → l'attaquant sait exactement quelle CVE exploiter sans avoir interagi une seule fois avec l'équipement.

---

### 4.2 Nmap — scan actif adapté à l'OT {#42-nmap}

#### Présentation de Nmap

**Nmap** (Network Mapper) est l'outil de référence pour la cartographie réseau et l'inventaire des services. Il envoie des paquets réseau et analyse les réponses.

> **Contrainte OT critique :** Nmap est un outil **actif** — il génère du trafic réseau. Sur un réseau OT en production, un scan mal configuré peut provoquer le **crash ou le redémarrage d'automates** à faible CPU. Les règles d'or :
> - **Toujours utiliser -T2 (polite)** sur un réseau OT actif
> - **Ne jamais utiliser -T4 ou -T5** (aggressive/insane) sur des équipements OT
> - **Obtenir une autorisation écrite** avant tout scan de production
> - **Tester d'abord** sur un équipement hors production si possible

#### Architecture des scripts NSE (Nmap Scripting Engine)

Le **NSE** permet d'étendre Nmap avec des scripts Lua spécialisés. Pour l'OT, les scripts pertinents sont :

| Script NSE | Protocole | Description |
|---|---|---|
| `modbus-discover` | Modbus/TCP | Lit l'identification de l'équipement (FC=43 MEI) |
| `s7-info` | S7comm (Siemens) | Identifie le module, firmware, état CPU |
| `dnp3-info` | DNP3 | Informations sur l'équipement DNP3 |
| `enip-info` | EtherNet/IP | Informations sur les équipements Rockwell |
| `bacnet-info` | BACnet | Informations sur les équipements de gestion technique |
| `modbus-enum` | Modbus/TCP | Énumération des Unit IDs disponibles |

---

#### Commandes Nmap OT — référence complète

**Découverte du réseau (ping sweep) :**
```bash
# Découverte des hôtes actifs (ICMP + TCP SYN sur port 80/443)
nmap -sn 192.168.10.0/24

# Découverte sur réseau OT (utiliser les ports OT pour le ping)
nmap -sn -PS502,102,4840 192.168.10.0/24

# Découverte sans ICMP (si ICMP filtré)
nmap -sn -PA502 192.168.10.0/24
```

**Scan des ports OT standards :**
```bash
# Scan des principaux ports industriels
nmap -p 102,502,1102,2222,4840,20000,44818,47808,1883,8883 192.168.10.0/24

# Scan des ports OT + IT courants (vue complète)
nmap -p 21,22,23,80,102,443,502,3389,4840,44818 192.168.10.0/24 -T2
```

**Identification de service et version :**
```bash
# Version des services (ATTENTION : peut provoquer instabilité sur équipements anciens)
nmap -sV -p 502 192.168.10.0/24 -T2

# OS detection (nécessite privilèges root)
nmap -O 192.168.10.110 -T2
```

**Scripts NSE OT :**
```bash
# Identification d'un automate Modbus (fabricant, modèle, firmware)
nmap --script modbus-discover -p 502 192.168.10.110 -T2

# Identification d'un automate Siemens S7
nmap --script s7-info -p 102 192.168.10.110 -T2

# Scan complet Modbus (enumération des Unit IDs)
nmap --script modbus-discover,modbus-enum -p 502 192.168.10.0/24 -T2

# Enumération EtherNet/IP (Rockwell)
nmap --script enip-info -p 44818 192.168.10.0/24 -T2

# Scan BACnet (bâtiment)
nmap --script bacnet-info -p 47808 192.168.10.0/24 --script-args=broadcast -T2
```

**Sauvegarde des résultats :**
```bash
# Sauvegarde en XML (pour traitement ultérieur)
nmap --script modbus-discover -p 502 192.168.10.0/24 -oX scan_ot_$(date +%Y%m%d).xml -T2

# Sauvegarde en texte et XML simultanément
nmap -p 502,102,4840 192.168.10.0/24 -oA scan_ot_complet -T2
```

#### Interprétation des résultats Nmap

**Résultat type — modbus-discover :**
```
Nmap scan report for 192.168.10.110
Host is up (0.0023s latency).

PORT    STATE SERVICE    VERSION
502/tcp open  modbus
| modbus-discover:
|   sid 0x01:
|     Vendor Name: Schneider Electric
|     Product Code: BMX P34 2020
|     Major Minor Revision: 2.60
|   sid 0x64:
|     Vendor Name: Schneider Electric
|     Product Code: BMX NOC 0401
|_    Major Minor Revision: 1.90
MAC Address: 00:80:F4:1A:2B:3C (Schneider Electric)
```

**Résultat type — s7-info :**
```
PORT    STATE SERVICE
102/tcp open  iso-tsap
| s7-info:
|   Module: 6ES7 315-2EH14-0AB0
|   Basic Hardware: 6ES7 315-2EH14-0AB0
|   Version: 0.1
|   System Name: S7 300 Station
|   Module Type: CPU 315-2 PN/DP
|   Serial Number: S7300-XXXX-YYYY
|   Plant Identification:
|_  Copyright: Original Siemens Equipment
```

**Ce que l'auditeur documente :**
- Liste exhaustive des équipements avec IP, MAC, fabricant, modèle, firmware
- Ports ouverts inattendus (web, SSH, Telnet sur un PLC → risque)
- Équipements identifiés avec des CVE connues (croisement avec base CVE)
- Présence de services d'administration non sécurisés

---

### 4.3 Wireshark — analyse de trames industrielles {#43-wireshark}

#### Présentation de Wireshark

**Wireshark** est l'analyseur de protocoles réseau de référence. Il capture le trafic sur une interface réseau et permet l'analyse détaillée de chaque trame, jusqu'au niveau applicatif.

**Modes de capture :**
- **Mode normal** : capture uniquement le trafic destiné à la machine
- **Mode promiscuité** (`-p`) : capture tout le trafic visible sur le segment réseau (nécessite accès à un port de switch en mode mirror/SPAN, ou connexion sur un hub)
- **Mode monitor (Wi-Fi)** : capture 802.11 brut

**Pour auditer un réseau OT :**
1. Connecter la machine d'audit sur un **port miroir (SPAN port)** du switch OT — le switch réplique tout le trafic vers ce port
2. Lancer Wireshark en mode promiscuité sur l'interface connectée
3. Capturer pendant 5 à 15 minutes pour avoir un échantillon représentatif

---

#### Dissecteurs de protocoles OT dans Wireshark

Wireshark intègre nativement des dissecteurs pour les principaux protocoles industriels :

| Protocole | Filtre Wireshark | Dissecteur | Informations extraites |
|---|---|---|---|
| Modbus/TCP | `modbus` | Natif | Function Code, Unit ID, adresse registre, valeur |
| S7comm | `s7comm` | Natif | Type de bloc, adresse, données |
| OPC-UA | `opcua` | Natif | NodeID, services, valeurs |
| DNP3 | `dnp3` | Natif | Function code, objets, valeurs |
| EtherNet/IP | `enip` | Natif | CIP services, assemblies |
| PROFINET | `pn_io` | Natif | IOD, IOC, alarmes |
| MQTT | `mqtt` | Natif | Topic, payload, QoS |
| BACnet | `bacapp` | Natif | Object type, property, valeur |

---

#### Filtres Wireshark OT — référence complète

**Filtres de base :**
```
# Afficher uniquement le trafic Modbus
modbus

# Afficher uniquement le trafic sur le port Modbus/TCP
tcp.port == 502

# Trafic S7comm (Siemens)
s7comm

# Trafic OPC-UA
opcua

# Trafic MQTT
mqtt

# Trafic DNP3
dnp3
```

**Filtres par Function Code Modbus :**
```
# Toutes les écritures Modbus (FC >= 5)
modbus.func_code >= 5

# Write Single Coil (FC=05)
modbus.func_code == 5

# Write Single Register (FC=06) — surveillance prioritaire
modbus.func_code == 6

# Write Multiple Registers (FC=16)
modbus.func_code == 16

# Read Device Identification (FC=43) — reconnaissance
modbus.func_code == 43

# Lectures seules (FC=1,2,3,4)
modbus.func_code <= 4
```

**Filtres combinés :**
```
# Écritures Modbus depuis une IP spécifique
modbus.func_code >= 5 && ip.src == 192.168.10.50

# Toutes les communications avec un PLC spécifique
ip.addr == 192.168.10.110

# Trafic entre HMI et PLC
ip.addr == 192.168.10.100 && ip.addr == 192.168.10.110

# Détecter un scan Nmap (connexions rapides sur port 502)
tcp.port == 502 && tcp.flags.syn == 1

# Détecter des paquets malformés Modbus
modbus && tcp.len > 0 && !modbus.len
```

**Filtres pour la détection d'anomalies :**
```
# Nouvelle IP jamais vue sur le réseau OT (à croiser avec baseline)
ip.src != 192.168.10.0/24

# Communication en dehors des heures ouvrables (pas filtrable directement,
# utiliser Edit > Time Reference + filtre temporel)

# Broadcast ARP excessifs (signe de scan ou d'ARP spoofing)
arp.opcode == 1 && eth.dst == ff:ff:ff:ff:ff:ff
```

---

#### Analyse d'une trame Modbus — décomposition détaillée

Une trame **Write Single Register (FC=06)** sur Modbus/TCP :

```
Frame 42: 66 bytes on wire, 66 bytes captured
  Ethernet II
    Destination: 00:80:F4:1A:2B:3C (Schneider Electric)
    Source:      00:50:56:C0:00:01 (VMware — poste HMI)
  Internet Protocol Version 4
    Source: 192.168.10.100 (HMI)
    Destination: 192.168.10.110 (PLC)
  Transmission Control Protocol
    Source Port: 54321
    Destination Port: 502
    Sequence number: 1
    Flags: 0x018 (PSH, ACK)
  Modbus/TCP
    Transaction Identifier: 1
    Protocol Identifier: 0          ← toujours 0 pour Modbus
    Length: 6
    Unit Identifier: 1              ← adresse esclave (PLC n°1)
    Function Code: Write Single Register (6)
    Register Address: 0x0064 (100)  ← registre cible
    Register Value: 0x0352 (850)    ← valeur (ex. consigne 850 °C)
```

**Lecture d'un registre (FC=03) — échange requête/réponse :**
```
→ REQUÊTE (HMI → PLC)
  Function Code: Read Holding Registers (3)
  Starting Address: 0x0064 (100)
  Quantity of Registers: 10        ← lecture de 10 registres

← RÉPONSE (PLC → HMI)
  Function Code: Read Holding Registers (3)
  Byte Count: 20
  Register 100: 0x0352 (850)       ← consigne température
  Register 101: 0x034A (842)       ← valeur mesurée
  Register 102: 0x0001 (1)         ← état : en chauffe
  Register 103: 0x0000 (0)         ← alarme : aucune
  ...
```

> **Pour l'attaquant :** en lisant ces échanges passivement pendant quelques minutes, il comprend la logique de contrôle, identifie les registres de consigne, et peut préparer une attaque FC=06 ciblée.

---

#### Workflow d'analyse en audit OT

**Étape 1 — Capture**
```bash
# Capture via CLI (tshark) sur interface eth0, port Modbus, durée 600s
tshark -i eth0 -f "tcp port 502" -w capture_ot_$(date +%Y%m%d_%H%M).pcap -a duration:600
```

**Étape 2 — Analyse statistique**
- `Statistics > Protocol Hierarchy` → répartition des protocoles (Modbus, S7comm, HTTP, ...)
- `Statistics > Conversations` → liste des pairs communicants (IP source ↔ IP destination)
- `Statistics > Endpoints` → tous les équipements actifs avec volume de trafic
- `Statistics > IO Graph` → visualisation du trafic dans le temps (pics, anomalies)

**Étape 3 — Détection d'anomalies**
- Filtrer les FC d'écriture (≥ 5) et noter les sources
- Identifier les IP qui ne figurent pas dans le plan d'adressage officiel
- Repérer les communications sur des plages horaires anormales
- Chercher des trames malformées ou des erreurs Modbus (Exception Codes)

**Étape 4 — Documentation**
- Cartographie réseau construite à partir de la capture (sources, destinations, protocoles)
- Inventaire des équipements avec leurs Function Codes utilisés
- Liste des anomalies avec horodatage et trame de référence

---

## Atelier 1 — Identification de vulnérabilités sur une architecture simulée {#atelier-1}

### Objectifs pédagogiques

À l'issue de cet atelier, chaque binôme doit être capable de :
- Utiliser Shodan pour identifier passivement des équipements industriels exposés
- Conduire un scan Nmap OT avec les scripts NSE appropriés sur un réseau simulé
- Capturer et analyser des trames Modbus/TCP avec Wireshark
- Identifier les Function Codes d'écriture et leur impact potentiel
- Produire un rapport de vulnérabilités structuré et hiérarchisé

### Architecture de l'atelier

```
  ┌─────────────────────────────────────────────────┐
  │  Réseau de l'atelier : 192.168.10.0/24           │
  │                                                  │
  │  192.168.10.100 — Poste HMI (attaquant)          │
  │                   Kali Linux / Ubuntu + outils   │
  │                                                  │
  │  192.168.10.110 — PLC simulé Modbus/TCP          │
  │                   (Modbus slave simulator)       │
  │                                                  │
  │  192.168.10.120 — Passerelle OT/IT               │
  │                   (simulée)                      │
  └─────────────────────────────────────────────────┘
```

### Phase 1 — Reconnaissance Shodan (30 min)

**Consigne :** En utilisant Shodan, répondez aux questions suivantes sur des équipements réels publiquement exposés (sans interagir avec eux).

**Exercice 1.1 :** Rechercher des automates Modbus exposés en France.
```
Requête Shodan : port:502 country:FR
```
- Combien de résultats obtient-on ?
- Quel est le fabricant le plus représenté ?
- Identifier un équipement avec une CVE associée et noter le score CVSS.

**Exercice 1.2 :** Rechercher des brokers MQTT non sécurisés.
```
Requête Shodan : port:1883 -password
```
- Vérifier si des topics industriels sont visibles dans les bannières.

**Exercice 1.3 :** Rechercher des RDP Windows exposés en France.
```
Requête Shodan : port:3389 "Windows 10" country:FR
```
- Estimer le nombre d'accès distants exposés sans protection visible.
- **Rappel légal :** consultation des résultats uniquement — toute tentative de connexion est illégale.

**Livrable Phase 1 :** tableau de 3 équipements identifiés (type, fabricant, pays, CVE éventuelle, risque estimé).

---

### Phase 2 — Scan Nmap OT (45 min)

**Consigne :** Réaliser un inventaire complet de l'architecture simulée (192.168.10.0/24) en utilisant Nmap avec les options adaptées à l'OT.

**Étape 2.1 — Découverte des hôtes :**
```bash
nmap -sn 192.168.10.0/24
```
→ Lister toutes les IP actives et les adresses MAC. Identifier les fabricants (via les OUI MAC).

**Étape 2.2 — Scan des ports OT :**
```bash
nmap -p 502,102,4840,1883,80,443,22,23 192.168.10.0/24 -T2 -oX scan_phase2.xml
```
→ Identifier les ports ouverts sur chaque équipement. Noter les services inattendus (HTTP sur un PLC, Telnet actif).

**Étape 2.3 — Identification Modbus :**
```bash
nmap --script modbus-discover -p 502 192.168.10.110 -T2
```
→ Relever le fabricant, modèle et version firmware de l'automate simulé.

**Étape 2.4 — Analyse des résultats :**
- Croiser le firmware identifié avec la base CVE (https://nvd.nist.gov ou https://cve.mitre.org)
- La version identifiée est-elle vulnérable à une CVE connue ? Quel est le score CVSS ?

**Livrable Phase 2 :** tableau d'inventaire complet + liste des vulnérabilités identifiées avec score CVSS.

---

### Phase 3 — Capture et analyse Wireshark (60 min)

**Consigne :** Capturer le trafic Modbus/TCP sur le réseau simulé et analyser les communications.

**Étape 3.1 — Mise en place de la capture :**
```bash
# Démarrer Wireshark sur l'interface eth0
wireshark -i eth0 -f "tcp port 502" &
# Ou via tshark
tshark -i eth0 -f "tcp port 502" -w capture_atelier1.pcap
```

**Étape 3.2 — Analyse des échanges :**
Appliquer les filtres suivants et noter les observations :
```
modbus                         → vue globale du trafic Modbus
modbus.func_code == 3          → lectures de registres (FC=03)
modbus.func_code >= 5          → écritures (alertes)
modbus.func_code == 6          → Write Single Register
```

**Questions d'analyse :**
1. Quels Function Codes sont utilisés dans les échanges normaux ?
2. Quelle est la fréquence de polling (lectures par minute) ?
3. Quels registres sont lus régulièrement ? Quelles valeurs ?
4. Y a-t-il des trames d'écriture (FC ≥ 5) ? De quelle source ?
5. Peut-on déduire la logique de contrôle du processus en lisant passivement ?

**Étape 3.3 — Simulation d'une écriture malveillante :**
Depuis le poste HMI (attaquant), envoyer une commande d'écriture vers le PLC simulé avec un outil Modbus (ex. `mbpoll` ou `modpoll`) :
```bash
# Écriture FC=06 sur le registre 100 avec la valeur 9999
mbpoll -t 4 -r 100 -1 192.168.10.110 9999
```

**Étape 3.4 — Détection dans Wireshark :**
- Appliquer le filtre `modbus.func_code == 6` et localiser la trame injectée
- Identifier l'IP source, l'adresse du registre, la valeur écrite
- Rédiger une alerte de sécurité décrivant l'incident (heure, source, impact potentiel)

**Livrable Phase 3 :** capture annotée + rapport d'incident simulé (1 page max).

---

### Grille d'évaluation de l'Atelier 1 (/20 points)

| Critère | Points | Indicateurs |
|---|---|---|
| **Phase 1 — Shodan** | 4 pts | Tableau complet (3 équipements), CVE identifiée, risque évalué correctement |
| **Phase 2 — Nmap** | 6 pts | Inventaire exhaustif, ports OT identifiés, identification fabricant/firmware, CVE croisée |
| **Phase 3 — Wireshark** | 6 pts | Filtres utilisés correctement, FC identifiés, écriture malveillante détectée et documentée |
| **Rapport final** | 4 pts | Structure claire, vulnérabilités hiérarchisées par CVSS, recommandations pertinentes |

---

## CC1 — Préparation au QCM de fin de journée {#cc1}

### Rappel du format

- **Durée :** 30 minutes
- **Note :** /20 (1 point par question, pas de pénalité)
- **Portée :** Modules 1, 2 et 3 (Jours 1 et 2)
- **Format :** 20 questions à choix unique (A/B/C/D)
- **Documents :** non autorisés

### Points clés à maîtriser pour le CC1

**Bloc 1 — Modules 1 & 2 (8 questions) :**
- Ordre de priorité de la triade CIA en OT : **Disponibilité > Intégrité > Confidentialité**
- Stuxnet : premier malware à effets physiques irréversibles (centrifugeuses iraniennes)
- Triton/TRISIS : seul malware ciblant les SIS (Safety Instrumented Systems)
- EKANS : liste de ~64 processus industriels terminés avant chiffrement
- Modèle de Purdue : PLC au **Niveau 1**, SCADA/HMI au **Niveau 2**
- IIoT : surface d'attaque élargie via firmware non patchable + credentials par défaut
- Edge computing : latence faible, mais pivot OT si compromis

**Bloc 2 — Module 3, composants & scénarios (7 questions) :**
- Port Modbus/TCP : **502**
- Port S7comm Siemens : **102**
- Port OPC-UA : **4840**
- Modbus/TCP : **aucune authentification, aucun chiffrement natif**
- FC=06 (Write Single Register) : peut provoquer des dommages physiques si le registre contrôle une consigne de processus
- CVE-2019-13945 (Siemens S7-1200/1500) : écriture de programme sans authentification, CVSS **9.8**
- Écoute passive Modbus : révèle topologie, valeurs capteurs, adresses registres → **totalement indétectable**
- Gestion des patches OT : délai typique **12 à 36 mois** (validation constructeur + arrêt planifié)

**Bloc 3 — Module 3, outils d'audit (5 questions) :**
- `nmap --script modbus-discover -p 502` → identification fabricant/firmware via FC=43 MEI
- `modbus.func_code == 6` → filtre Wireshark pour Write Single Register
- Shodan : **OSINT passif** — indexe les données publiques — consulter est légal, se connecter sans autorisation ne l'est pas
- `-T2 (polite)` ou `-T3 (normal)` : options Nmap recommandées sur réseau OT actif
- `-T5 (insane)` : risque de crash des PLC à faible CPU — **à ne jamais utiliser en OT**

### Auto-évaluation — Questions types

1. Sur quel port TCP fonctionne Modbus/TCP ? → **502**
2. Quel script NSE Nmap permet d'identifier le firmware d'un automate Modbus ? → `modbus-discover`
3. Quel filtre Wireshark affiche uniquement les Write Single Register ? → `modbus.func_code == 6`
4. Pourquoi une CVE critique OT reste-t-elle souvent non patchée 24 mois ? → validation constructeur + arrêt planifié de production nécessaire
5. Quelle commande FC=06 envoie une valeur 9999 au registre 100 d'un PLC 192.168.10.110 ? → `mbpoll -t 4 -r 100 -1 192.168.10.110 9999`

---

## Synthèse du Jour 2

### Points clés à retenir

1. **Les composants OT sont structurellement non sécurisés** : PLC, HMI, passerelles ont été conçus pour la fiabilité et la performance, pas pour la sécurité. L'absence d'authentification et de chiffrement est la norme, pas l'exception.

2. **Le CVSSv3 doit être contextualisé en OT** : une CVE de score "moyen" peut être critique si elle affecte un PLC de sécurité. Le contexte métier prime sur le score brut.

3. **Shodan = OSINT légal, connexion = illégal** : consulter l'index Shodan est légal (données publiques). Toute interaction directe avec un équipement découvert sans autorisation est un accès frauduleux (art. 323-1 CP).

4. **Nmap en OT = T2 obligatoire** : un scan agressif peut crasher des PLC. L'autorisation écrite préalable est indispensable.

5. **Wireshark révèle tout sur Modbus** : en mode passif sur un réseau Modbus/TCP, un attaquant obtient la topologie complète, les valeurs temps réel et la logique de contrôle sans émettre un seul paquet.

6. **FC=06 (Write Single Register) = risque physique** : une commande d'écriture sur un registre de consigne peut provoquer un accident industriel. C'est le vecteur de sabotage le plus simple sur Modbus.

### Passerelle vers le Jour 3

Le **Jour 3** abordera les **normes et standards** (IEC 62443, ISO 27001, NIST CSF) ainsi que la **sécurisation des communications** (TLS/mTLS, MQTT sécurisé, PKI industrielle). L'atelier pratique portera sur la mise en place d'une authentification mutuelle mTLS sur un broker MQTT.

Pour préparer le Jour 3, il est utile de comprendre :
- Pourquoi MQTT sur port 1883 est un protocole non sécurisé par défaut
- Ce qu'est un certificat X.509 et à quoi sert une PKI (Public Key Infrastructure)
- La différence entre TLS (authentification serveur) et mTLS (authentification mutuelle)

---

## Ressources complémentaires

### Bases de données de vulnérabilités
- **NVD — National Vulnerability Database** : https://nvd.nist.gov (base CVE avec scores CVSS)
- **CISA Known Exploited Vulnerabilities** : https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- **ICS-CERT Advisories** : https://www.cisa.gov/ics-advisories (CVE spécifiques ICS/OT)
- **CERT-FR Avis** : https://www.cert.ssi.gouv.fr/avis/ (version française)

### Documentation des outils
- **Nmap NSE OT scripts** : https://nmap.org/nsedoc/scripts/ (filtrer par "modbus", "s7", "dnp3")
- **Wireshark OT dissectors** : https://wiki.wireshark.org/Modbus (wiki officiel)
- **Shodan API** : https://developer.shodan.io (documentation API pour l'automatisation)
- **mbpoll** (client Modbus CLI) : https://github.com/epsilonrt/mbpoll

### Frameworks et référentiels
- **MITRE ATT&CK for ICS** : https://attack.mitre.org/matrices/ics/
  - Technique T0836 : Modify Parameter (FC=06)
  - Technique T0846 : Remote System Discovery (Nmap OT)
  - Technique T0888 : Remote System Information Discovery (Shodan)
- **ANSSI — Guide de la sécurité des systèmes industriels** : https://www.ssi.gouv.fr

---

*Document pédagogique SEC500 — Jour 2 · JUNIA XP 2025/2026 · Formateur : Christophe CROISANT*
*Version 1.0 — à compléter selon retours terrain lors de l'animation*
