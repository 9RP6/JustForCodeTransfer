import socket
import base64
import json

def process_payload(raw_b64):
    print(f"Base64 Payload: {raw_b64}")

    decoded = base64.b64decode(raw_b64)
    
    print("Decoded HEX:", decoded.hex())
    print("Raw Bytes (as list):", list(decoded))

    try:
        message = decoded[:6].decode('utf-8')
        counter_bytes = decoded[6:]
        counter = int.from_bytes(counter_bytes, byteorder='big')
        
        print(f"Decoded Message: {message}")
        print(f"Packet Counter: {counter}")
    except Exception as e:
        print("Error decoding:", e)

def listen_gateway():
    UDP_IP = "0.0.0.0"  # Listen on all interfaces
    UDP_PORT = 1700     # Port 1700 for Semtech UDP packet forwarder

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    print(f"Listening on {UDP_IP}:{UDP_PORT}...")

    while True:
        data, addr = sock.recvfrom(4096)  # Buffer size
        print(f"\nReceived packet from {addr}")

        try:
            # Parse packet
            json_start = data.find(b'{')
            if json_start == -1:
                print("No JSON found in packet")
                continue

            json_data = json.loads(data[json_start:])

            # LoRaWAN packets are in "rxpk" list
            if 'rxpk' in json_data:
                for pkt in json_data['rxpk']:
                    if 'data' in pkt:
                        raw_b64 = pkt['data']
                        process_payload(raw_b64)
                    else:
                        print("No 'data' field in rxpk")
            else:
                print("No 'rxpk' field in packet")

        except Exception as e:
            print(f"Failed to parse packet: {e}")

if __name__ == "__main__":
    listen_gateway()
