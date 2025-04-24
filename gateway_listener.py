import socket
import json
import base64
import time

# Packet Forwarder default LoRa gateway address
UDP_IP = "127.0.0.1"
UDP_PORT = 1700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Listening for LoRaWAN packets on port 1700...\n")

while True:
    try:
        data, addr = sock.recvfrom(4096)
        if data[3] == 0x00:  # PUSH_DATA identifier
            json_start = 12  # skip protocol headers
            try:
                message = json.loads(data[json_start:])
                rxpk_list = message.get("rxpk", [])
                for pkt in rxpk_list:
                    raw = pkt.get("data", "")
                    decoded = base64.b64decode(raw)

                    # Decode to ASCII part + timestamp
                    ascii_part = decoded[:6].decode('ascii')
                    timestamp = int.from_bytes(decoded[6:], byteorder='big')

                    timestamp_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestamp))

                    print(f"[{timestamp_str}] Payload: {ascii_part} | Timestamp: {timestamp}")
            except Exception as e:
                print("Decode error:", e)
    except KeyboardInterrupt:
        break
