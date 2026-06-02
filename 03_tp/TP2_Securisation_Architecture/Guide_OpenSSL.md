# Guide OpenSSL — Niveau intermédiaire
## PKI, Certificats et TLS pour l'Industrie 4.0

**Module SEC500 — Cybersécurité appliquée à l'Industrie 4.0**
JUNIA XP · Mastère Chef de projet Industrie 4.0 · 2025/2026
Formateur : Christophe CROISANT

---

## Introduction

OpenSSL est une bibliothèque open source qui implémente les protocoles SSL/TLS ainsi que l'ensemble des primitives cryptographiques associées. Dans un contexte industriel, c'est l'outil de référence pour :

- générer des clés privées et des certificats X.509 ;
- construire une Infrastructure à Clés Publiques (PKI) ;
- sécuriser les communications entre équipements IIoT ;
- auditer et diagnostiquer des connexions TLS.

Ce guide couvre les opérations intermédiaires : création d'une PKI complète, gestion du cycle de vie des certificats, inspection, et vérification de connexions TLS.

---

## 1. Rappels — Concepts fondamentaux

### 1.1 Cryptographie asymétrique

La cryptographie asymétrique repose sur une paire de clés mathématiquement liées :

| Clé | Visibilité | Usage principal |
|-----|-----------|----------------|
| **Clé privée** | Secrète, jamais partagée | Signer, déchiffrer |
| **Clé publique** | Distribuée librement | Vérifier, chiffrer |

Ce qui est signé avec la clé privée peut être vérifié avec la clé publique — et réciproquement. L'asymétrie garantit que seul le détenteur de la clé privée peut produire une signature valide.

### 1.2 Certificat X.509

Un certificat X.509 est un document numérique qui associe une clé publique à une identité (un équipement, un serveur, un utilisateur). Il contient notamment :

- le **sujet** (Subject) : identité du propriétaire du certificat ;
- l'**émetteur** (Issuer) : autorité qui a signé le certificat ;
- la **clé publique** du sujet ;
- la **période de validité** (dates début/fin) ;
- l'**empreinte numérique** (signature de l'émetteur).

Un certificat sans signature d'une autorité de confiance est dit **auto-signé** (self-signed).

### 1.3 Infrastructure à Clés Publiques (PKI)

Une PKI est l'ensemble des composants permettant de gérer le cycle de vie des certificats :

```
Autorité de Certification Racine (Root CA)
        |
        | signe
        |
Autorité de Certification Intermédiaire (optionnel)
        |
        | signe
        |
Certificats finaux (serveurs, clients, équipements)
```

Dans les TPs de ce module, nous utilisons une PKI simplifiée à un seul niveau (Root CA → certificats finaux).

### 1.4 TLS et mTLS

**TLS (Transport Layer Security)** chiffre les communications et authentifie le serveur auprès du client.

**mTLS (Mutual TLS)** ajoute l'authentification du client auprès du serveur — les deux parties présentent un certificat signé par la même CA.

| Mécanisme | Authentification serveur | Authentification client | Chiffrement |
|-----------|:---:|:---:|:---:|
| TCP nu    | ❌ | ❌ | ❌ |
| TLS       | ✅ | ❌ | ✅ |
| mTLS      | ✅ | ✅ | ✅ |

---

## 2. Gestion des clés privées

### 2.1 Générer une clé RSA

```bash
# Clé RSA 4096 bits (recommandé pour une CA)
openssl genrsa -out ca.key 4096

# Clé RSA 2048 bits (suffisant pour certificats finaux)
openssl genrsa -out server.key 2048

# Clé RSA protégée par un mot de passe (AES-256)
openssl genrsa -aes256 -out ca_protected.key 4096
```

> **Taille recommandée** : 4096 bits pour une CA (longue durée de vie), 2048 bits pour les certificats finaux renouvelés annuellement. En-dessous de 2048 bits, la clé est considérée insuffisante.

### 2.2 Inspecter une clé privée

```bash
# Afficher les composants mathématiques de la clé
openssl rsa -in server.key -text -noout

# Vérifier uniquement que la clé est valide
openssl rsa -in server.key -check

# Extraire la clé publique depuis la clé privée
openssl rsa -in server.key -pubout -out server_public.pem
```

### 2.3 Supprimer la protection par mot de passe

```bash
# Utile pour les serveurs qui démarrent sans interaction humaine
openssl rsa -in ca_protected.key -out ca.key
# → Demande le mot de passe, produit une clé non chiffrée
```

> ⚠️ **Sécurité** : une clé privée non chiffrée doit être stockée avec des permissions restrictives : `chmod 600 ca.key`. Sur un système Linux, seul le propriétaire doit pouvoir la lire.

### 2.4 Générer une clé ECDSA (alternative moderne)

```bash
# Courbe P-256 (bonne performance, forte sécurité)
openssl ecparam -name prime256v1 -genkey -noout -out ec.key

# Courbe P-384 (plus forte, recommandée pour CA)
openssl ecparam -name secp384r1 -genkey -noout -out ec_ca.key
```

> ECDSA produit des clés plus courtes qu'RSA pour un niveau de sécurité équivalent — avantageux pour les équipements IIoT à ressources limitées.

---

## 3. Autorité de Certification (CA)

### 3.1 Créer un certificat racine auto-signé

```bash
openssl req \
  -x509 \
  -new \
  -nodes \
  -key ca.key \
  -sha256 \
  -days 3650 \
  -out ca.crt \
  -subj "/C=FR/ST=Hauts-de-France/O=MecaProd/CN=MecaProd Root CA"
```

**Explication des options :**

| Option | Signification |
|--------|--------------|
| `-x509` | Produit directement un certificat (pas un CSR) |
| `-new` | Nouvelle requête |
| `-nodes` | No DES — clé privée non chiffrée dans le certificat |
| `-sha256` | Algorithme de hachage pour la signature |
| `-days 3650` | Validité 10 ans (typique pour une CA racine) |
| `-subj "..."` | Sujet du certificat en ligne de commande (évite le mode interactif) |

**Champs du sujet (`-subj`) :**

| Champ | Signification | Exemple |
|-------|--------------|---------|
| `C`  | Country — code ISO 2 lettres | `FR` |
| `ST` | State / Province | `Hauts-de-France` |
| `L`  | Locality / Ville | `Valenciennes` |
| `O`  | Organization | `MecaProd` |
| `OU` | Organizational Unit | `Production` |
| `CN` | Common Name — identifiant principal | `MecaProd Root CA` |

### 3.2 Inspecter le certificat CA

```bash
# Affichage complet
openssl x509 -in ca.crt -text -noout

# Afficher uniquement les dates de validité
openssl x509 -in ca.crt -noout -dates

# Afficher uniquement le sujet
openssl x509 -in ca.crt -noout -subject

# Afficher uniquement l'émetteur
openssl x509 -in ca.crt -noout -issuer

# Afficher l'empreinte SHA-256
openssl x509 -in ca.crt -noout -fingerprint -sha256
```

---

## 4. Demande de Certificat (CSR)

### 4.1 Générer un CSR

Un **CSR (Certificate Signing Request)** est une requête de signature de certificat. Il contient la clé publique du demandeur et les informations d'identité souhaitées. Il est transmis à la CA pour obtenir un certificat signé.

```bash
# Méthode interactive (OpenSSL pose les questions)
openssl req \
  -new \
  -key server.key \
  -out server.csr

# Méthode non-interactive (paramètres en ligne de commande)
openssl req \
  -new \
  -key server.key \
  -out server.csr \
  -subj "/C=FR/O=MecaProd/CN=scada.mecaprod.local"
```

> **CN (Common Name) pour un serveur** : doit correspondre exactement au nom DNS ou à l'adresse IP utilisée par les clients pour se connecter. Un écart entre le CN du certificat et l'adresse de connexion provoque une erreur TLS.

### 4.2 Inspecter un CSR

```bash
# Vérifier le contenu d'un CSR avant de le signer
openssl req -in server.csr -text -noout

# Vérifier uniquement le sujet
openssl req -in server.csr -noout -subject

# Vérifier la signature du CSR (intégrité)
openssl req -in server.csr -verify
```

### 4.3 CSR avec Subject Alternative Names (SAN)

Les SAN permettent à un certificat de couvrir plusieurs noms DNS ou adresses IP. C'est la méthode moderne recommandée (le CN seul est déprécié pour la validation de serveur).

```bash
# Créer un fichier de configuration étendu
cat > server_ext.cnf << 'EOF'
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
C  = FR
O  = MecaProd
CN = scada.mecaprod.local

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = scada.mecaprod.local
DNS.2 = mqtt.mecaprod.local
IP.1  = 192.168.10.100
EOF

# Générer le CSR avec les SAN
openssl req \
  -new \
  -key server.key \
  -out server.csr \
  -config server_ext.cnf
```

---

## 5. Signature de certificats

### 5.1 Signer un CSR avec la CA

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

**Explication des options :**

| Option | Signification |
|--------|--------------|
| `-req` | L'entrée est un CSR (pas une clé) |
| `-CA ca.crt` | Certificat de la CA qui signe |
| `-CAkey ca.key` | Clé privée de la CA |
| `-CAcreateserial` | Crée le fichier de suivi des numéros de série (`ca.srl`) |
| `-days 365` | Validité du certificat signé (1 an typique pour les finaux) |

### 5.2 Signer avec les extensions SAN

```bash
cat > v3.ext << 'EOF'
authorityKeyIdentifier = keyid, issuer
basicConstraints = CA:FALSE
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = scada.mecaprod.local
IP.1  = 192.168.10.100
EOF

openssl x509 \
  -req \
  -in server.csr \
  -CA ca.crt \
  -CAkey ca.key \
  -CAcreateserial \
  -out server.crt \
  -days 365 \
  -sha256 \
  -extfile v3.ext
```

### 5.3 Vérifier la chaîne de confiance

```bash
# Vérifier qu'un certificat a bien été signé par la CA
openssl verify -CAfile ca.crt server.crt
# Résultat attendu : server.crt: OK

# Vérifier un certificat client
openssl verify -CAfile ca.crt client.crt
```

> En cas d'erreur, OpenSSL retourne un code explicite : `error 18` = certificat auto-signé, `error 10` = certificat expiré, `error 20` = CA inconnue.

---

## 6. Inspection et diagnostic

### 6.1 Inspecter un certificat

```bash
# Affichage complet (verbose)
openssl x509 -in server.crt -text -noout

# Extraits ciblés
openssl x509 -in server.crt -noout -subject       # Sujet
openssl x509 -in server.crt -noout -issuer        # Émetteur
openssl x509 -in server.crt -noout -dates         # Dates de validité
openssl x509 -in server.crt -noout -serial        # Numéro de série
openssl x509 -in server.crt -noout -fingerprint -sha256  # Empreinte
openssl x509 -in server.crt -noout -purpose       # Usages autorisés
```

### 6.2 Vérifier la cohérence clé/certificat

Un certificat est invalide s'il ne correspond pas à la clé privée associée. Pour vérifier, on compare les modules RSA :

```bash
# Les deux commandes doivent retourner la même empreinte
openssl rsa  -in server.key -modulus -noout | openssl md5
openssl x509 -in server.crt -modulus -noout | openssl md5
```

Si les empreintes sont identiques, la clé et le certificat forment bien une paire.

### 6.3 Convertir les formats de certificats

```bash
# PEM → DER (format binaire, utilisé par certains équipements industriels)
openssl x509 -in server.crt -outform DER -out server.der

# DER → PEM
openssl x509 -in server.der -inform DER -outform PEM -out server.crt

# PEM → PKCS#12 (bundle clé + certificat, utilisé sur Windows / Java)
openssl pkcs12 -export \
  -out server.p12 \
  -inkey server.key \
  -in server.crt \
  -certfile ca.crt \
  -name "MecaProd Server"

# PKCS#12 → PEM
openssl pkcs12 -in server.p12 -out server_out.pem -nodes
```

**Formats courants :**

| Format | Extension | Description |
|--------|-----------|-------------|
| PEM | `.pem`, `.crt`, `.key` | Base64, lisible en texte, le plus courant sous Linux |
| DER | `.der`, `.cer` | Binaire, utilisé sur Windows et équipements embarqués |
| PKCS#12 | `.p12`, `.pfx` | Bundle binaire clé + certificat(s), protégé par mot de passe |

---

## 7. Connexions TLS — Test et diagnostic

### 7.1 Tester une connexion TLS avec s_client

`openssl s_client` est l'outil de diagnostic TLS par excellence. Il établit une connexion TLS et affiche tous les détails de la négociation.

```bash
# Connexion TLS simple
openssl s_client -connect hostname:port

# Avec vérification du certificat serveur par la CA locale
openssl s_client \
  -connect mqtt.mecaprod.local:8883 \
  -CAfile ca.crt

# Avec certificat client (mTLS)
openssl s_client \
  -connect mqtt.mecaprod.local:8883 \
  -CAfile   ca.crt \
  -cert     client.crt \
  -key      client.key

# Forcer TLS 1.2 ou TLS 1.3
openssl s_client -connect hostname:443 -tls1_2
openssl s_client -connect hostname:443 -tls1_3
```

### 7.2 Analyser la sortie de s_client

Une connexion réussie produit une sortie similaire à :

```
CONNECTED(00000003)
depth=1 CN=MecaProd Root CA
verify return:1
depth=0 CN=scada.mecaprod.local
verify return:1
---
Certificate chain
 0 s:CN=scada.mecaprod.local
   i:CN=MecaProd Root CA
 1 s:CN=MecaProd Root CA
   i:CN=MecaProd Root CA
---
Server certificate
[... détails du certificat ...]
---
SSL handshake has read 1823 bytes and written 405 bytes
---
New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384
[...]
Verify return code: 0 (ok)
```

**Points clés à vérifier :**

| Élément | Signification |
|---------|--------------|
| `Verify return code: 0 (ok)` | Chaîne de confiance validée |
| `TLSv1.3` | Version TLS négociée (1.2 minimum acceptable) |
| `TLS_AES_256_GCM_SHA384` | Suite cryptographique — AES-256 = robuste |
| `depth=0`, `depth=1` | Profondeur de la chaîne de certificats |

### 7.3 Tester un serveur HTTPS

```bash
# Connexion HTTPS avec vérification
openssl s_client -connect example.com:443 -servername example.com

# Extraire uniquement le certificat du serveur
openssl s_client -connect example.com:443 -showcerts \
  2>/dev/null | openssl x509 -text -noout

# Vérifier la date d'expiration d'un certificat serveur distant
echo | openssl s_client -connect example.com:443 2>/dev/null \
  | openssl x509 -noout -dates
```

### 7.4 Codes d'erreur courants

| Code | Message | Cause probable |
|------|---------|---------------|
| `error 2` | Unable to get issuer certificate | CA absente ou non fournie |
| `error 10` | Certificate has expired | Certificat périmé |
| `error 18` | Self signed certificate | Certificat auto-signé non approuvé |
| `error 20` | Unable to get local issuer certificate | CA non trouvée dans le magasin de confiance |
| `error 21` | Unable to verify the first certificate | Chaîne de certificats incomplète |

---

## 8. Cas pratique — PKI complète pour un réseau IIoT

Voici la séquence complète pour construire une PKI opérationnelle dans le contexte du TP MecaProd.

### Étape 1 — Créer l'arborescence

```bash
mkdir -p pki/{ca,server,clients,crl}
cd pki
```

### Étape 2 — Générer la CA

```bash
# Clé privée de la CA
openssl genrsa -out ca/ca.key 4096

# Certificat racine auto-signé (10 ans)
openssl req -x509 -new -nodes \
  -key ca/ca.key \
  -sha256 -days 3650 \
  -out ca/ca.crt \
  -subj "/C=FR/O=MecaProd/CN=MecaProd Root CA"

# Protéger la clé
chmod 600 ca/ca.key
```

### Étape 3 — Certificat serveur (broker MQTT / SCADA)

```bash
# Clé privée du serveur
openssl genrsa -out server/server.key 2048

# CSR
openssl req -new \
  -key server/server.key \
  -out server/server.csr \
  -subj "/C=FR/O=MecaProd/CN=mqtt.mecaprod.local"

# Signature par la CA (1 an)
openssl x509 -req \
  -in  server/server.csr \
  -CA  ca/ca.crt \
  -CAkey ca/ca.key \
  -CAcreateserial \
  -out server/server.crt \
  -days 365 -sha256

# Vérification
openssl verify -CAfile ca/ca.crt server/server.crt
```

### Étape 4 — Certificats clients (capteurs IIoT)

```bash
for SENSOR in sensor-line1 sensor-line2 sensor-hmi; do
  # Clé privée
  openssl genrsa -out clients/${SENSOR}.key 2048

  # CSR
  openssl req -new \
    -key clients/${SENSOR}.key \
    -out clients/${SENSOR}.csr \
    -subj "/C=FR/O=MecaProd/CN=${SENSOR}"

  # Signature
  openssl x509 -req \
    -in  clients/${SENSOR}.csr \
    -CA  ca/ca.crt \
    -CAkey ca/ca.key \
    -CAcreateserial \
    -out clients/${SENSOR}.crt \
    -days 365 -sha256

  echo "✅ Certificat généré : ${SENSOR}"
done
```

### Étape 5 — Vérifier l'ensemble

```bash
# Vérifier tous les certificats clients d'un coup
for CRT in clients/*.crt; do
  echo -n "${CRT} : "
  openssl verify -CAfile ca/ca.crt "${CRT}"
done

# Vérifier les dates d'expiration
for CRT in clients/*.crt server/server.crt; do
  echo "=== ${CRT} ==="
  openssl x509 -in "${CRT}" -noout -dates
done
```

### Structure finale

```
pki/
├── ca/
│   ├── ca.key          ← CONFIDENTIEL — ne jamais distribuer
│   └── ca.crt          ← À distribuer à tous les équipements
├── server/
│   ├── server.key      ← Confidentiel — broker uniquement
│   ├── server.csr      ← Intermédiaire (peut être supprimé)
│   └── server.crt      ← Certificat public du broker
└── clients/
    ├── sensor-line1.key / .crt
    ├── sensor-line2.key / .crt
    └── sensor-hmi.key  / .crt
```

---

## 9. Bonnes pratiques et points de vigilance

### 9.1 Durées de vie recommandées

| Composant | Durée recommandée | Raison |
|-----------|------------------|--------|
| CA racine | 10 ans | Longue durée, difficile à renouveler |
| Certificat serveur | 1 an | Rotation régulière, limiter l'exposition |
| Certificat client IIoT | 1 à 2 ans | Selon la contrainte de renouvellement terrain |
| Certificat de test | 30 jours | Éviter les oublis en environnement de dev |

### 9.2 Permissions des fichiers

```bash
# Clés privées : lecture seule par le propriétaire
chmod 600 *.key

# Certificats publics : lisibles par tous
chmod 644 *.crt

# Répertoire CA : accès restreint
chmod 700 ca/
```

### 9.3 Ce qu'il ne faut jamais faire

- **Ne jamais partager une clé privée** — si une clé est compromise, révoquer immédiatement le certificat associé et en générer un nouveau.
- **Ne jamais utiliser `ssl.CERT_NONE`** en Python — désactive toute vérification de certificat, rend TLS inutile.
- **Ne jamais ignorer les erreurs de vérification** — `Verify return code: 18` n'est pas « normal » en production.
- **Ne jamais stocker la clé CA sur le broker** — en production, la clé CA doit être hors ligne (air-gapped) après la signature des certificats.

### 9.4 Commandes de diagnostic rapide (mémo)

```bash
# Combien de jours reste-t-il avant expiration ?
openssl x509 -in server.crt -noout -enddate

# Le certificat est-il encore valide aujourd'hui ?
openssl x509 -in server.crt -noout -checkend 0
# → "Certificate will not expire" = valide
# → "Certificate will expire" = expiré

# Dans combien de secondes expire-t-il ? (86400 = 1 jour)
openssl x509 -in server.crt -noout -checkend 86400
```

---

## Récapitulatif des commandes essentielles

| Opération | Commande |
|-----------|---------|
| Générer une clé RSA 2048 | `openssl genrsa -out key.pem 2048` |
| Créer un certificat CA auto-signé | `openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 -out ca.crt` |
| Créer un CSR | `openssl req -new -key server.key -out server.csr` |
| Signer un CSR avec la CA | `openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365 -sha256` |
| Vérifier la chaîne de confiance | `openssl verify -CAfile ca.crt server.crt` |
| Inspecter un certificat | `openssl x509 -in server.crt -text -noout` |
| Tester une connexion TLS | `openssl s_client -connect host:port -CAfile ca.crt` |
| Tester mTLS | `openssl s_client -connect host:port -CAfile ca.crt -cert client.crt -key client.key` |
| Vérifier cohérence clé/cert | `openssl rsa -in server.key -modulus -noout \| openssl md5` |
| Vérifier date d'expiration | `openssl x509 -in server.crt -noout -checkend 0` |

---

*JUNIA XP — 2025/2026 — SEC500 Cybersécurité appliquée à l'industrie 4.0*
*Formateur : Christophe CROISANT*
