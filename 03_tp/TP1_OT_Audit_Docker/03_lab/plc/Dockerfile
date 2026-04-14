FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir pyModbusTCP
COPY modbus_server.py /app/modbus_server.py
CMD ["python", "/app/modbus_server.py"]
