import base64
import json
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 1730

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Listening for LoRa packets...")

while True:
    data, addr = sock.recvfrom(1024)
    try:
        packet = json.loads(data[12:].decode('utf-8'))
        if "rxpk" in packet:
            for rx in packet["rxpk"]:
                payload = rx.get("data")
                if payload:
                    decoded = base64.b64decode(payload).decode(errors="replace")
                    print(f"Decoded payload: {decoded}")
    except Exception as e:
        continue
