import socket
import json
import base64
import time

# Default LoRa Packet Forwarder address
UDP_IP = "127.0.0.1"
UDP_PORT = 1700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Listening for LoRaWAN packets on port 1700...\n")

while True:
    try:
        data, addr = sock.recvfrom(4096)

        # 0x00 indicates PUSH_DATA message type from forwarder
        if data[3] == 0x00:
            json_start = 12  # skip protocol header
            try:
                message = json.loads(data[json_start:])
                rxpk_list = message.get("rxpk", [])

                for pkt in rxpk_list:
                    raw = pkt.get("data", "")
                    print(f"\n🔹 Raw Base64 Payload: {raw}")

                    try:
                        decoded = base64.b64decode(raw)
                        print(f"Decoded Bytes (HEX): {decoded.hex()}")
                        print(f"Payload Length: {len(decoded)} bytes")

                        if len(decoded) >= 10:
                            ascii_part = decoded[:6].decode('ascii')
                            timestamp_bytes = decoded[6:10]
                            timestamp = int.from_bytes(timestamp_bytes, byteorder='big')
                            timestamp_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestamp))

                            print(f"Decoded Message: '{ascii_part}' | Timestamp: {timestamp} ({timestamp_str})")
                        else:
                            print("Payload too short to parse (expected 10 bytes)")

                    except Exception as decode_err:
                        print(f"Decode error: {decode_err}")

            except json.JSONDecodeError as json_err:
                print(f"JSON error: {json_err}")

    except KeyboardInterrupt:
        print("\nStopped listener.")
        break
