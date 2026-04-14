import os
from pyModbusTCP.server import ModbusServer, DataBank

port = int(os.getenv("MODBUS_PORT", "502"))
reg1 = int(os.getenv("REG1", "500"))

DataBank.set_words(0, [reg1, 523, 1, 0])

server = ModbusServer(host="0.0.0.0", port=port, no_block=True)
server.start()

import time
while True:
    time.sleep(1)
