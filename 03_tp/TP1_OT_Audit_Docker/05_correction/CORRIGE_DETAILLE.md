# Corrigé détaillé — TP1

## 1. Inventaire minimal
| IP | Rôle | Ports attendus |
|---|---|---|
| 192.168.10.110 | PLC1 | 502 |
| 192.168.10.111 | PLC2 | 502 |
| 192.168.10.120 | HMI | 8080 |
| 192.168.10.130 | Legacy | 139,445,3389 |
| 192.168.10.200 | MQTT broker | 1883 |

## 2. Analyse sécurité
- Modbus n'apporte ni authentification ni chiffrement.
- MQTT anonyme permet la lecture et l'injection de messages.
- 3389 et 445 exposés sur un hôte legacy représentent un risque élevé de compromission initiale et de mouvement latéral.
- Le réseau plat augmente le rayon d'impact.

## 3. Mesures prioritaires
1. segmentation IT / OT avec DMZ industrielle
2. suppression ou isolement des services legacy exposés
3. bastion + VPN + MFA pour l'accès distant
4. filtrage strict des flux Modbus
5. remplacement de MQTT par MQTTs avec authentification
