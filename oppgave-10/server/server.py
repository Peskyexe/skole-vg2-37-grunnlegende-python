import socket
import cv2

# Bind to 0.0.0.0 to listen on all Local network adapters
HOST = "0.0.0.0"
PORT = 9006

# Initialize UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))
print(f"Server is listening for a client on port {PORT}...")

# Wait for an initial "ping" packet from the client to get their address
_, client_address = server_socket.recvfrom(1024)
print(f"Client connected from: {client_address}. Starting stream...")

# Open webcam 
camera = cv2.VideoCapture(0)

# Set lower resolution to ensure compressed frames easily fit within UDP limits
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

try:
    while camera.isOpened():
        success, frame = camera.read()
        if not success:
            break

        # Compress the frame into JPEG format (0-100 quality)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
        result, encoded_image = cv2.imencode('.jpg', frame, encode_param)
        
        # Convert the encoded image array into raw bytes
        data = encoded_image.tobytes()
        
        # Check size rule before sending
        if len(data) > 65000:
            print(f"Frame too large ({len(data)} bytes). Skipping to prevent fragmentation.")
            continue

        # Send the compressed image payload to the client
        server_socket.sendto(data, client_address)

except KeyboardInterrupt:
    print("\nStopping server stream...")

finally:
    camera.release()
    server_socket.close()
    print("Resources cleaned up.")