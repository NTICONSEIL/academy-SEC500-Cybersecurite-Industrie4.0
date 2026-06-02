# TP2 – Sécurisation des communications industrielles avec MQTT

**Module SEC500 – Cybersécurité appliquée à l'Industrie 4.0**

---

## Objectifs pédagogiques

À l'issue de ce TP, vous serez capable de :

* Comprendre le fonctionnement d'une architecture IIoT basée sur MQTT.
* Déployer un broker MQTT avec Docker.
* Développer un capteur industriel simulé en Python.
* Développer une application de supervision industrielle.
* Observer les vulnérabilités d'une communication non sécurisée.
* Réaliser une attaque passive d'interception.
* Réaliser une attaque active d'usurpation de capteur.
* Identifier les besoins de chiffrement et d'authentification.

---

# Partie 1 – Architecture MQTT non sécurisée et analyse des vulnérabilités

## 1. Contexte

L'entreprise **SmartFactory 4.0** exploite une ligne de production automatisée.

Des capteurs connectés transmettent en temps réel des données de fonctionnement :

* Température
* Vibrations
* État machine

Ces données sont collectées par une plateforme de supervision afin de surveiller l'état des équipements industriels.

Dans un premier temps, l'architecture mise en œuvre ne comporte aucun mécanisme de sécurité.

Votre mission consiste à analyser les risques associés à cette architecture.

---

## 2. Architecture étudiée

```text
Capteur IIoT
      |
      | MQTT
      |
Broker Mosquitto
      |
      | MQTT
      |
Supervision
```

Cette architecture permet la communication entre les équipements mais n'apporte aucune garantie de sécurité.

---

## 3. Préparation de l'environnement

### 3.1 Création de l'arborescence

Créer la structure suivante :

```text
TP2_MQTT/

├── docker-compose.yml
├── mosquitto/
│   └── mosquitto.conf
└── scripts/
```

---

### 3.2 Configuration Docker

Créer le fichier :

```yaml
services:
  mosquitto:
    image: eclipse-mosquitto:2
    container_name: tp_mqtt_broker
    ports:
      - "1883:1883"
    volumes:
      - ./mosquitto/mosquitto.conf:/mosquitto/config/mosquitto.conf
```

---

### 3.3 Configuration Mosquitto

Créer le fichier :

```conf
listener 1883
allow_anonymous true
```

---

### 3.4 Démarrage du broker

Lancer :

```bash
docker compose up -d
```

Vérifier :

```bash
docker ps
```

Le conteneur doit apparaître en état **Up**.

---

## 4. Création d'un capteur industriel simulé

Le capteur simulera :

* une température
* un niveau de vibration
* un état de fonctionnement

Le programme publiera automatiquement ces informations sur le broker MQTT.

### Question 1

Quel est le rôle d'un capteur IIoT dans une architecture Industrie 4.0 ?

---

## 5. Création de la supervision

La supervision devra :

* se connecter au broker MQTT
* s'abonner aux données du capteur
* afficher les informations reçues

### Question 2

Quel est le rôle d'un système de supervision dans une usine connectée ?

---

## 6. Validation de la communication

Exécuter :

Terminal 1 :

```bash
python supervisor_plain.py
```

Terminal 2 :

```bash
python sensor_plain.py
```

Vous devez observer la réception des messages publiés.

Exemple :

```json
{
  "timestamp":"2026-01-15T14:20:03",
  "machine":"machineA",
  "temperature":72.5,
  "vibration":0.62,
  "status":"OK"
}
```

---

## 7. Analyse de sécurité

La communication actuelle utilise :

```text
MQTT
Port 1883
Aucun chiffrement
Aucune authentification
```

### Question 3

Quels risques identifiez-vous dans cette architecture ?

Compléter le tableau suivant :

| Risque | Description |
| ------ | ----------- |
|        |             |
|        |             |
|        |             |
|        |             |

---

## 8. Attaque n°1 : interception des communications

Un attaquant obtient un accès au réseau industriel.

Il développe un programme capable d'écouter tous les messages MQTT circulant sur le broker.

Architecture :

```text
                    Attaquant
                        |
                        |
Capteur ---> Broker ---> Supervision
```

Lancer :

```bash
python attacker_sniffer.py
```

Observer les informations interceptées.

### Question 4

Quelles informations sensibles l'attaquant peut-il récupérer ?

---

### Question 5

Pourquoi cette attaque est-elle possible ?

---

## 9. Attaque n°2 : usurpation d'un capteur

L'attaquant décide désormais d'envoyer ses propres messages.

Il publie les données suivantes :

```json
{
  "machine":"machineA",
  "temperature":999,
  "vibration":99,
  "status":"CRITICAL"
}
```

Lancer :

```bash
python attacker_spoofer.py
```

Observer la réaction du système de supervision.

---

### Question 6

Le superviseur est-il capable de distinguer le vrai capteur du faux ?

Justifier.

---

### Question 7

Quels impacts cette attaque pourrait-elle avoir sur une ligne de production réelle ?

---

## 10. Synthèse

À l'issue de cette première partie du TP :

| Propriété de sécurité | État |
| --------------------- | ---- |
| Confidentialité       | ❌    |
| Intégrité             | ❌    |
| Authentification      | ❌    |
| Traçabilité           | ❌    |

Les attaques réalisées démontrent qu'une architecture MQTT non sécurisée ne peut pas être utilisée directement dans un environnement industriel critique.

---

## 11. Travail de réflexion

Répondre aux questions suivantes :

### Question 8

Comment empêcher un attaquant de lire les messages MQTT ?

---

### Question 9

Comment vérifier l'identité d'un capteur ?

---

### Question 10

Quels mécanismes de sécurité pourraient être ajoutés à cette architecture ?

---

> Dans la prochaine partie du TP, nous mettrons en œuvre :
> * une autorité de certification (CA)
> * des certificats X.509
> * le protocole MQTTs
> * le chiffrement TLS
> * l'authentification mutuelle (mTLS)
>
> afin de transformer cette architecture vulnérable en une architecture industrielle sécurisée.

---

# Partie 2 – Mise en œuvre d'une PKI et de MQTTs

## 12. Objectifs de cette deuxième partie

Dans la première partie du TP, nous avons démontré qu'une architecture MQTT classique présente plusieurs vulnérabilités :

* Interception des communications
* Usurpation d'identité
* Injection de données falsifiées
* Absence de confidentialité

L'objectif de cette deuxième partie est de mettre en œuvre un mécanisme de protection basé sur :

* TLS
* Certificats X.509
* Autorité de Certification (CA)
* MQTTs

---

## 13. Introduction à la PKI

### Qu'est-ce qu'une PKI ?

Une PKI (Public Key Infrastructure) est une infrastructure permettant :

* d'identifier les équipements
* de distribuer des certificats
* de garantir la confiance entre les systèmes

Dans un environnement industriel, elle est utilisée notamment pour :

* MQTTs
* OPC UA sécurisé
* HTTPS industriel
* VPN industriels

---

### Architecture de confiance

```text
                     Autorité de Certification
                               (CA)
                                      |
                +---------------------+---------------------+
                |                                           |
                |                                           |
      Certificat Serveur                         Certificat Client
                |                                           |
                |                                           |
          Broker MQTT                                Capteur IIoT
```

---

## 14. Création de l'Autorité de Certification

Créer un répertoire dédié :

```bash
mkdir certs
cd certs
```

---

### Génération de la clé privée de la CA

```bash
openssl genrsa -out ca.key 4096
```

Vérification :

```bash
ls
```

Résultat attendu :

```text
ca.key
```

---

### Création du certificat racine

```bash
openssl req \
-x509 \
-new \
-nodes \
-key ca.key \
-sha256 \
-days 3650 \
-out ca.crt
```

Renseigner par exemple :

```text
Country Name : FR
State : Nouvelle-Aquitaine
Organization : SmartFactory
Common Name : SmartFactory Root CA
```

---

### Vérification du certificat

```bash
openssl x509 -in ca.crt -text -noout
```

Identifier les informations suivantes :

* Émetteur (Issuer)
* Sujet (Subject)
* Date d'expiration
* Clé publique

---

### Question 11

Quel est le rôle d'une Autorité de Certification ?

---

### Question 12

Pourquoi la clé privée de la CA constitue-t-elle l'élément le plus sensible de la PKI ?

---

## 15. Création du certificat serveur MQTT

Le broker MQTT doit désormais posséder sa propre identité numérique.

---

### Génération de la clé privée

```bash
openssl genrsa -out server.key 2048
```

---

### Création de la demande de certificat

```bash
openssl req \
-new \
-key server.key \
-out server.csr
```

Important :

```text
Common Name = localhost
```

---

### Signature par la CA

```bash
openssl x509 \
-req \
-in server.csr \
-CA ca.crt \
-CAkey ca.key \
-CAcreateserial \
-out server.crt \
-days 365 \
-sha256
```

---

### Vérification

```bash
openssl verify \
-CAfile ca.crt \
server.crt
```

Résultat attendu :

```text
server.crt: OK
```

---

## 16. Préparation du broker MQTTs

Créer l'arborescence suivante :

```text
mosquitto/

├── certs/
│     ├── ca.crt
│     ├── server.crt
│     └── server.key
│
└── mosquitto_tls.conf
```

Copier les certificats :

```bash
cp certs/ca.crt mosquitto/certs/
cp certs/server.crt mosquitto/certs/
cp certs/server.key mosquitto/certs/
```

---

## 17. Configuration de Mosquitto

Créer le fichier :

```conf
listener 8883

cafile /mosquitto/config/certs/ca.crt

certfile /mosquitto/config/certs/server.crt

keyfile /mosquitto/config/certs/server.key

allow_anonymous true
```

À ce stade :

* Le trafic est chiffré.
* Le serveur est authentifié.
* Les clients ne sont pas encore authentifiés.

---

## 18. Mise à jour de Docker Compose

Modifier le fichier :

```yaml
services:
  mosquitto:
    image: eclipse-mosquitto:2
    container_name: tp_mqtt_broker

    ports:
      - "1883:1883"
      - "8883:8883"

    volumes:
      - ./mosquitto/mosquitto_tls.conf:/mosquitto/config/mosquitto.conf
      - ./mosquitto/certs:/mosquitto/config/certs
```

---

## 19. Redémarrage du broker

Appliquer la nouvelle configuration :

```bash
docker compose down
docker compose up -d --force-recreate
```

Vérifier :

```bash
docker ps
```

Résultat attendu :

```text
0.0.0.0:8883->8883/tcp
```

---

## 20. Vérification TLS avec OpenSSL

Tester la connexion sécurisée :

```bash
openssl s_client \
-connect localhost:8883 \
-CAfile certs/ca.crt
```

---

### Analyse des résultats

Identifier :

* Le certificat présenté par le serveur
* La chaîne de confiance
* La version TLS utilisée
* La suite cryptographique négociée

Vous devez notamment observer :

```text
Certificate chain
```

```text
Verify return code: 0 (ok)
```

---

### Question 13

Quel certificat est présenté au client lors de l'établissement de la connexion TLS ?

---

### Question 14

Pourquoi le client accepte-t-il ce certificat ?

---

### Question 15

Quel est le rôle du fichier `ca.crt` utilisé par OpenSSL ?

---

## 21. Validation des propriétés de sécurité

À ce stade du TP :

| Propriété de sécurité       | État |
| --------------------------- | ---- |
| Confidentialité             | ✅    |
| Intégrité                   | ✅    |
| Authentification du serveur | ✅    |
| Authentification du client  | ❌    |
| Authentification mutuelle   | ❌    |

---

## 22. Synthèse

L'utilisation de TLS permet désormais :

* de chiffrer les communications MQTT ;
* de garantir l'identité du broker ;
* d'empêcher l'écoute passive des échanges ;
* de préparer la mise en œuvre d'une authentification mutuelle.

> Dans la prochaine partie du TP, nous modifierons les scripts Python afin d'utiliser MQTTs et nous mettrons en œuvre une authentification mutuelle basée sur des certificats clients.

---

# Partie 3 – Mise en œuvre de MQTTs dans les applications Python

## 22. Objectifs de cette troisième partie

Dans la partie précédente, nous avons :

* créé une Autorité de Certification (CA) ;
* généré un certificat serveur ;
* configuré Mosquitto pour utiliser TLS ;
* validé le fonctionnement de MQTTs avec OpenSSL.

Nous allons maintenant modifier les applications Python afin qu'elles utilisent une connexion sécurisée basée sur TLS.

À l'issue de cette partie, vous serez capable de :

* utiliser MQTTs dans une application Python ;
* vérifier un certificat serveur ;
* comprendre le rôle de la chaîne de confiance ;
* analyser les effets du chiffrement sur les communications ;
* comparer MQTT et MQTTs.

---

## 23. Architecture étudiée

L'architecture évolue désormais vers une version sécurisée :

```text
Capteur IIoT
      |
      | MQTTs (TLS)
      |
Broker Mosquitto
      |
      | MQTTs (TLS)
      |
Supervision
```

Les données sont désormais chiffrées pendant leur transport.

---

## 24. Préparation des certificats côté client

Les applications Python doivent être capables de vérifier l'identité du broker MQTT.

Créer l'arborescence suivante :

```text
scripts/

├── certs/
│     └── ca.crt
│
├── sensor_tls.py
└── supervisor_tls.py
```

Copiez le certificat de l'Autorité de Certification :

```bash
cp certs/ca.crt scripts/certs/
```

---

## 25. Pourquoi utiliser le certificat de la CA ?

Lorsqu'une application Python se connecte au broker MQTT :

1. Le broker présente son certificat.
2. Le client vérifie que ce certificat a été signé par une autorité de confiance.
3. Si la vérification réussit, la connexion TLS est établie.

Le fichier `ca.crt` représente donc la racine de confiance utilisée par les applications.

---

### Question 16

Pourquoi le certificat de la CA doit-il être distribué aux clients ?

---

## 26. Création du superviseur sécurisé

Créer le fichier :

```text
supervisor_tls.py
```

```python
import ssl
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 8883

TOPIC = "factory/line1/#"

def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connexion MQTTs réussie")
    client.subscribe(TOPIC)

def on_message(client, userdata, message):
    print(
        f"[MESSAGE] {message.topic}"
        f" -> {message.payload.decode()}"
    )

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.tls_set(
    ca_certs="certs/ca.crt",
    cert_reqs=ssl.CERT_REQUIRED
)

client.on_connect = on_connect
client.on_message = on_message

client.connect(
    BROKER_HOST,
    BROKER_PORT
)

client.loop_forever()
```

---

### Analyse du code

La fonction :

```python
client.tls_set(...)
```

active TLS.

Le paramètre :

```python
ca_certs="certs/ca.crt"
```

indique quelle Autorité de Certification doit être utilisée pour vérifier le certificat du serveur.

Le paramètre :

```python
ssl.CERT_REQUIRED
```

oblige la vérification du certificat.

---

### Question 17

Que se passerait-il si la vérification du certificat n'était pas effectuée ?

---

## 27. Création du capteur sécurisé

Créer :

```text
sensor_tls.py
```

```python
import ssl
import json
import random
import time

from datetime import datetime

import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 8883

TOPIC = "factory/line1/machineA/telemetry"

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.tls_set(
    ca_certs="certs/ca.crt",
    cert_reqs=ssl.CERT_REQUIRED
)

client.connect(
    BROKER_HOST,
    BROKER_PORT
)

while True:

    payload = {

        "timestamp":
        datetime.now().isoformat(),

        "machine":
        "machineA",

        "temperature":
        round(random.uniform(50,80),2),

        "vibration":
        round(random.uniform(0.2,2.0),2),

        "status":
        "OK"
    }

    client.publish(
        TOPIC,
        json.dumps(payload)
    )

    print("Publication :", payload)

    time.sleep(2)
```

---

## 28. Validation de la connexion sécurisée

Lancer :

Terminal 1 :

```bash
python supervisor_tls.py
```

Terminal 2 :

```bash
python sensor_tls.py
```

Résultat attendu :

```text
Connexion MQTTs réussie
```

Puis :

```text
[MESSAGE]
factory/line1/machineA/telemetry
```

---

### Question 18

Quelles différences observez-vous par rapport aux scripts MQTT utilisés dans la première partie du TP ?

---

## 29. Vérification de la chaîne de confiance

Modifier temporairement :

```python
ca_certs="certs/ca.crt"
```

par :

```python
ca_certs="certs/fake.crt"
```

ou renommer le certificat.

Relancer l'application.

Résultat attendu :

```text
CERTIFICATE_VERIFY_FAILED
```

---

### Question 19

Pourquoi la connexion est-elle refusée ?

---

### Question 20

Quel risque serait encouru si l'on désactivait complètement la vérification des certificats ?

---

## 30. Analyse du trafic réseau

Avant TLS, les données MQTT circulaient en clair.

Nous allons maintenant observer le trafic réseau.

Lancer Wireshark.

Filtre :

```text
tcp.port == 8883
```

Observer les paquets échangés.

---

### Comparaison

#### Avant TLS

Les informations suivantes étaient visibles :

```text
temperature
vibration
status
machineA
```

---

#### Après TLS

Les données applicatives deviennent :

```text
Application Data
Application Data
Application Data
```

Le contenu réel des messages n'est plus accessible.

---

### Question 21

Pourquoi l'attaquant ne peut-il plus lire les valeurs de température ou de vibration ?

---

## 31. Tentative d'écoute avec l'attaquant

Modifier le script :

```text
attacker_sniffer.py
```

afin qu'il utilise TLS.

Lancer :

```bash
python attacker_sniffer.py
```

---

### Observation

L'attaquant parvient toujours à se connecter.

Il peut encore :

* s'abonner aux topics ;
* publier des messages ;
* écouter les communications.

Pourquoi ?

Parce que le broker accepte encore les connexions anonymes :

```conf
allow_anonymous true
```

---

### Question 22

Pourquoi TLS ne suffit-il pas à empêcher l'attaquant de se connecter ?

---

## 32. Analyse des propriétés de sécurité obtenues

À ce stade :

| Propriété                 | État |
| ------------------------- | ---- |
| Confidentialité           | ✅    |
| Intégrité                 | ✅    |
| Authentification serveur  | ✅    |
| Authentification client   | ❌    |
| Authentification mutuelle | ❌    |

---

## 33. Synthèse

Grâce à MQTTs, les communications entre le capteur et le broker sont désormais protégées contre l'écoute passive.

Le chiffrement TLS garantit :

* la confidentialité des données ;
* l'intégrité des échanges ;
* l'authentification du broker MQTT.

Cependant, tout client possédant le certificat de la CA peut encore établir une connexion avec le broker.

> Dans la prochaine partie du TP, nous mettrons en œuvre une authentification mutuelle (mTLS) afin d'authentifier également les clients et d'empêcher toute connexion non autorisée.

---

# Partie 4 – Authentification mutuelle (mTLS)

## 23. Objectifs de cette dernière partie

Dans la partie précédente, nous avons sécurisé les communications grâce à TLS.

Les propriétés suivantes sont désormais assurées :

| Propriété                   | État |
| --------------------------- | ---- |
| Confidentialité             | ✅    |
| Intégrité                   | ✅    |
| Authentification du serveur | ✅    |
| Authentification du client  | ❌    |

Un problème subsiste :

Tout client possédant le certificat de la CA peut encore se connecter au broker MQTT.

L'objectif de cette dernière partie est donc de mettre en œuvre une authentification mutuelle (Mutual TLS ou mTLS).

---

## 24. Principe du mTLS

### TLS classique

Avec TLS classique :

```text
Client
   |
   | Vérifie le certificat
   |
Serveur
```

Le client authentifie le serveur.

Le serveur n'authentifie pas le client.

---

### Mutual TLS

Avec mTLS :

```text
Client
   |
   | Vérifie le certificat du serveur
   |
Serveur

ET

Serveur
   |
   | Vérifie le certificat du client
   |
Client
```

Chaque partie vérifie l'identité de l'autre.

---

### Architecture finale

```text
                 Autorité de Certification
                           (CA)
                                  |
             +--------------------+--------------------+
             |                                         |
             |                                         |
      Certificat serveur                       Certificat client
         Broker MQTT                             Capteur IIoT
```

---

## 25. Création du certificat client

Nous allons créer une identité numérique pour notre capteur industriel.

---

### Génération de la clé privée

```bash
openssl genrsa -out client.key 2048
```

---

### Création de la demande de certificat

```bash
openssl req \
-new \
-key client.key \
-out client.csr
```

Renseigner :

```text
Common Name : sensor-machineA
```

---

### Signature du certificat

```bash
openssl x509 \
-req \
-in client.csr \
-CA ca.crt \
-CAkey ca.key \
-CAcreateserial \
-out client.crt \
-days 365 \
-sha256
```

---

### Vérification

```bash
openssl verify \
-CAfile ca.crt \
client.crt
```

Résultat attendu :

```text
client.crt: OK
```

---

### Question 20

Quel équipement est désormais identifié par ce certificat ?

---

### Question 21

Pourquoi le certificat client est-il signé par la même CA que le certificat serveur ?

---

## 26. Déploiement du certificat client

Créer l'arborescence suivante :

```text
scripts/

├── certs/
│     ├── ca.crt
│     ├── client.crt
│     └── client.key
```

Copier :

```bash
cp certs/client.crt scripts/certs/
cp certs/client.key scripts/certs/
```

---

## 27. Configuration du broker MQTT

Modifier le fichier :

```text
mosquitto_tls.conf
```

Remplacer :

```conf
listener 8883

cafile /mosquitto/config/certs/ca.crt

certfile /mosquitto/config/certs/server.crt

keyfile /mosquitto/config/certs/server.key

allow_anonymous true
```

par :

```conf
listener 8883

cafile /mosquitto/config/certs/ca.crt

certfile /mosquitto/config/certs/server.crt

keyfile /mosquitto/config/certs/server.key

require_certificate true

use_identity_as_username true

allow_anonymous false
```

---

### Signification des paramètres

#### require_certificate true

Le broker exige un certificat client valide.

---

#### allow_anonymous false

Les connexions anonymes sont interdites.

---

#### use_identity_as_username true

Le Common Name du certificat devient l'identité du client.

Exemple :

```text
sensor-machineA
```

---

## 28. Redémarrage du broker

Appliquer la nouvelle configuration :

```bash
docker compose down
docker compose up -d --force-recreate
```

---

### Vérification

Consulter les logs :

```bash
docker logs tp_mqtt_broker
```

Le broker doit démarrer sans erreur.

---

## 29. Modification du capteur sécurisé

Modifier le fichier :

```text
sensor_tls.py
```

Ajouter le certificat client :

```python
client.tls_set(
    ca_certs="certs/ca.crt",
    certfile="certs/client.crt",
    keyfile="certs/client.key",
    cert_reqs=ssl.CERT_REQUIRED
)
```

---

### Vérification

Lancer :

```bash
python sensor_tls.py
```

La connexion doit être acceptée.

---

## 30. Test d'une connexion sans certificat

Créer :

```python
test_no_certificate.py
```

```python
import ssl
import paho.mqtt.client as mqtt

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.tls_set(
    ca_certs="certs/ca.crt",
    cert_reqs=ssl.CERT_REQUIRED
)

client.connect(
    "localhost",
    8883
)

client.loop_start()
```

---

### Exécution

```bash
python test_no_certificate.py
```

Résultat attendu :

```text
Connection Refused
```

ou

```text
TLS handshake failed
```

---

### Question 22

Pourquoi cette connexion est-elle rejetée ?

---

## 31. Test de l'attaquant

Lancer :

```bash
python attacker_sniffer.py
```

sans certificat client.

---

Résultat attendu :

```text
Connexion refusée
```

---

### Question 23

L'attaquant peut-il encore écouter les communications ?

Justifier.

---

## 32. Test de l'usurpation

Lancer :

```bash
python attacker_spoofer.py
```

sans certificat.

---

Résultat attendu :

```text
Connexion refusée
```

---

### Question 24

Pourquoi l'attaque d'usurpation n'est-elle plus possible ?

---

## 33. Vérification avec OpenSSL

Tester la connexion sans certificat :

```bash
openssl s_client \
-connect localhost:8883 \
-CAfile certs/ca.crt
```

Observer les messages d'erreur.

---

Tester ensuite avec certificat :

```bash
openssl s_client \
-connect localhost:8883 \
-cert certs/client.crt \
-key certs/client.key \
-CAfile certs/ca.crt
```

La connexion doit être acceptée.

---

### Question 25

Quel est le rôle du certificat client dans cette connexion ?

---

## 34. Bilan sécurité

Comparer l'état de l'architecture avant et après le mTLS.

| Propriété de sécurité    | MQTT | MQTTs | MQTTs + mTLS |
| ------------------------ | ---- | ----- | ------------ |
| Confidentialité          | ❌    | ✅     | ✅            |
| Intégrité                | ❌    | ✅     | ✅            |
| Authentification serveur | ❌    | ✅     | ✅            |
| Authentification client  | ❌    | ❌     | ✅            |
| Usurpation               | ❌    | ❌     | ✅            |
| Écoute passive           | ❌    | ✅     | ✅            |

---

## 35. Synthèse

Vous avez progressivement transformé une architecture industrielle vulnérable en une architecture sécurisée conforme aux bonnes pratiques de l'Industrie 4.0.

Les mécanismes mis en œuvre dans ce TP sont utilisés dans :

* MQTTs industriels ;
* OPC UA sécurisé ;
* Passerelles IIoT ;
* Solutions Edge Computing ;
* Plateformes Cloud industrielles ;
* Architectures conformes à l'IEC 62443.

---

## Travail de synthèse

Rédiger un document de 2 à 3 pages présentant :

1. Les vulnérabilités observées dans la version MQTT non sécurisée.
2. Les apports de TLS.
3. Le rôle d'une PKI.
4. Le fonctionnement du mTLS.
5. Les bénéfices de cette architecture dans un contexte Industrie 4.0.
6. Les limites éventuelles de cette solution.

---

# Conclusion générale

Au cours de ce TP, nous avons étudié les problématiques de sécurité associées aux communications industrielles dans un environnement Industrie 4.0 reposant sur des équipements connectés et des échanges machine-to-machine.

Dans une première phase, nous avons déployé une architecture IIoT simple basée sur MQTT. Cette architecture a permis de mettre en évidence plusieurs vulnérabilités majeures :

* absence de chiffrement des communications ;
* possibilité d'intercepter les données échangées ;
* absence d'authentification des équipements ;
* possibilité d'usurper l'identité d'un capteur ;
* injection de données falsifiées dans le système de supervision.

Ces expérimentations ont démontré qu'une architecture MQTT classique ne peut pas être utilisée seule dans un environnement industriel critique où la disponibilité, l'intégrité et la confidentialité des informations constituent des enjeux majeurs.

Dans une seconde phase, nous avons mis en place une Infrastructure à Clés Publiques (PKI) afin d'établir une chaîne de confiance entre les différents composants de l'architecture. Nous avons créé une Autorité de Certification (CA), généré des certificats X.509 et configuré le broker MQTT pour utiliser le protocole TLS.

L'utilisation de MQTTs a permis d'apporter plusieurs garanties de sécurité :

* chiffrement des échanges ;
* protection contre l'écoute passive ;
* vérification de l'identité du serveur ;
* garantie de l'intégrité des données transmises.

Enfin, dans la dernière partie du TP, nous avons mis en œuvre une authentification mutuelle (mTLS). Cette approche impose que chaque équipement présente un certificat valide lors de l'établissement de la connexion. Le broker authentifie alors les clients et les clients authentifient le broker.

Cette étape a permis de neutraliser efficacement les attaques précédemment observées :

* impossibilité pour un équipement non autorisé de se connecter ;
* impossibilité d'écouter les communications ;
* impossibilité d'usurper l'identité d'un capteur ;
* impossibilité d'injecter de fausses données dans le système.

Au-delà de la maîtrise technique des outils utilisés (Docker, Mosquitto, OpenSSL et Python), ce TP a permis d'illustrer concrètement les concepts fondamentaux de la cybersécurité industrielle :

* gestion de l'identité numérique des équipements ;
* établissement d'une chaîne de confiance ;
* sécurisation des communications machine-to-machine ;
* défense contre les attaques de type écoute, usurpation et falsification ;
* mise en œuvre des principes de sécurité recommandés dans les architectures IIoT modernes.

Les mécanismes étudiés sont aujourd'hui largement utilisés dans les systèmes cyber-physiques et les infrastructures industrielles connectées, notamment au travers des protocoles MQTTs, OPC UA Secure, HTTPS industriel et de nombreuses solutions Edge Computing ou Cloud industriel.

Ce TP illustre ainsi la transition progressive d'une architecture fonctionnelle mais vulnérable vers une architecture sécurisée répondant aux exigences de l'Industrie 4.0 et aux principes de défense en profondeur recommandés par les standards de cybersécurité industrielle tels que l'IEC 62443.

```text
Capteur IIoT
      |
      | MQTTs + mTLS
      |
Broker MQTT
      |
      | MQTTs + mTLS
      |
Supervision
```

L'architecture obtenue garantit :

* la confidentialité des échanges ;
* l'intégrité des données ;
* l'authentification des équipements ;
* la résistance aux attaques d'écoute et d'usurpation.

Ces mécanismes constituent aujourd'hui la base de la sécurisation des communications dans les systèmes cyber-physiques et les infrastructures Industrie 4.0.
