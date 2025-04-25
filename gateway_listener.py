import socket
import json
import base64

UDP_IP = "0.0.0.0"
UDP_PORT = 1700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Listening for LoRaWAN packets on port 1700...\n")

while True:
    try:
        data, addr = sock.recvfrom(4096)

        if data[3] == 0x00:  # PUSH_DATA
            message = json.loads(data[12:])
            for pkt in message.get("rxpk", []):
                raw = pkt.get("data", "")
                print(f"\nBase64 Payload: {raw}")
                try:
                    decoded = base64.b64decode(raw)
                    print(f"Decoded HEX: {decoded.hex()}")
                    if len(decoded) >= 10:
                        hello_part = decoded[:6].decode('ascii', errors='ignore')
                        packet_num = int.from_bytes(decoded[6:10], byteorder='big')
                        print(f"Message: '{hello_part}' | Packet #: {packet_num}")
                    else:
                        print("Payload too short to decode.")
                except Exception as e:
                    print("Decode error:", e)
    except KeyboardInterrupt:
        break
