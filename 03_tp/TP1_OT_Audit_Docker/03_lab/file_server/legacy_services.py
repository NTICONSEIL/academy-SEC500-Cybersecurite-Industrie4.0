import socket, threading, time

BANNER = b"SEC500 legacy service\r\n"

def serve(port):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", port))
    s.listen(5)
    while True:
        conn, _ = s.accept()
        try:
            conn.sendall(BANNER)
            time.sleep(0.2)
        finally:
            conn.close()

for p in (139, 445, 3389):
    threading.Thread(target=serve, args=(p,), daemon=True).start()

while True:
    time.sleep(1)
