# Commandes essentielles — TP1

## Accès au conteneur analyste
```bash
docker exec -it sec500-analyst bash
```

## Découverte réseau
```bash
nmap -sn 192.168.10.0/24
nmap -sV -p 80,139,445,502,1883,3389,8080 192.168.10.0/24
```

## Modbus
```bash
nmap --script modbus-discover -p 502 192.168.10.110
mbtget -r1 -a1 192.168.10.110
mbtget -w1:9999 -a1 192.168.10.110
mbtget -w1:500 -a1 192.168.10.110
```

## MQTT
```bash
mosquitto_sub -h 192.168.10.200 -t '#' -v
mosquitto_pub -h 192.168.10.200 -t 'usine/four1/temperature' -m '9999'
```

## Capture
```bash
tcpdump -i eth0 -w /tmp/modbus.pcap port 502
tshark -i eth0 -f 'port 502'
tshark -i eth0 -Y modbus
```
