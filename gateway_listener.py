import socket
import json
import base64
import time

# LoRa packet forwarder settings
UDP_IP = "0.0.0.0"         # Listen on all interfaces
UDP_PORT = 1700            # Default LoRaWAN packet forwarder port

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Listening for LoRaWAN packets on port 1700...\n")

while True:
    try:
        data, addr = sock.recvfrom(4096)

        # Check if packet is a PUSH_DATA (0x00) message from gateway
        if data[3] == 0x00:
            json_start = 12  # Header is 12 bytes
            try:
                message = json.loads(data[json_start:])
                rxpk_list = message.get("rxpk", [])

                for pkt in rxpk_list:
                    raw = pkt.get("data", "")
                    print(f"\nRaw Base64 Payload: {raw}")

                    try:
                        decoded = base64.b64decode(raw)
                        print(f"Decoded Bytes (HEX): {decoded.hex()}")
                        print(f"Payload Length: {len(decoded)} bytes")

                        if len(decoded) >= 10:
                            # Try to decode ASCII + 4-byte timestamp
                            try:
                                ascii_part = decoded[:6].decode('ascii')
                            except UnicodeDecodeError:
                                ascii_part = "<non-ascii>"

                            timestamp_bytes = decoded[6:10]
                            timestamp = int.from_bytes(timestamp_bytes, byteorder='big')
                            timestamp_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestamp))

                            print(f"Decoded Message: '{ascii_part}' | Timestamp: {timestamp} ({timestamp_str})")
                        else:
                            print("Warning: Payload too short to decode expected format")

                    except Exception as decode_err:
                        print(f"Payload decode error: {decode_err}")

            except json.JSONDecodeError as json_err:
                print(f"JSON parse error: {json_err}")

    except KeyboardInterrupt:
        print("\nListener stopped by user.")
        break
