# Guide enseignant détaillé — TP1

## Déroulé recommandé (3h30)

### 00:00–00:15
- rappel des règles d'usage
- présentation du contexte
- objectifs, livrables, barème

### 00:15–00:45
- prise en main du lab Docker
- découverte réseau avec `nmap -sn`
- première cartographie

### 00:45–01:20
- scan ciblé des ports
- qualification des services OT et legacy

### 01:20–02:00
- découverte Modbus via NSE
- lecture / écriture contrôlée de registre
- observation dans `tshark` ou `tcpdump`

### 02:00–02:30
- écoute MQTT
- démonstration d'injection de valeur

### 02:30–03:00
- analyse des vulnérabilités
- préparation du schéma d'architecture cible

### 03:00–03:30
- restitution
- debrief, défense en profondeur, points OT

## Questions de relance
- Pourquoi un réseau plat est-il critique en OT ?
- Quelle différence entre impact IT et impact OT ?
- Pourquoi un simple service exposé sur un poste legacy peut-il mettre en danger un automate ?

## Barème sur 25
- cartographie réseau : 5
- analyse des vulnérabilités : 6
- manipulation protocolaire : 5
- qualité de l'architecture cible : 6
- restitution : 3
