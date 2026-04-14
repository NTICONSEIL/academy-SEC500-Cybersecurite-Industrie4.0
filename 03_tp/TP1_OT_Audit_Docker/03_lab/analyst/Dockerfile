FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends     nmap tcpdump tshark iputils-ping netcat-openbsd curl mosquitto-clients     && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pyModbusTCP mbtget

CMD ["bash", "-lc", "sleep infinity"]
