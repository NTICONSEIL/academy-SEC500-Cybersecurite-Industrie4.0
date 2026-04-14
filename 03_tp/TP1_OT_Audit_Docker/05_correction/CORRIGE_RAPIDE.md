# Corrigé rapide — TP1

## Expositions attendues
- PLC1 et PLC2 : port 502/tcp
- HMI : port 8080/tcp
- Legacy server : ports 139, 445, 3389
- MQTT broker : port 1883

## Vulnérabilités attendues
- Modbus/TCP sans authentification
- MQTT anonyme sur 1883
- service RDP exposé
- SMB exposé
- absence de segmentation réseau

## Architecture cible attendue
- séparation IT / DMZ / OT
- bastion d'administration
- règles firewall entre zones
- journalisation centralisée
- restriction des flux d'écriture Modbus aux seules sources légitimes
