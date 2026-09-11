mport cv2
import numpy as np
import socket

SERVER_IP = "10.1.120.56" 
SERVER_PORT = 9006
server_address = (SERVER_IP, SERVER_PORT)

# Initialize UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send initial packet so the server knows our IP and port
print(f"Connecting to server at {SERVER_IP}:{SERVER_PORT}...")
client_socket.sendto(b"START_STREAM", server_address)

print("Receiving video stream. Press 'q' in the video window to exit.")

try:
    while True:
        # Receive the compressed JPEG bytes
        packet, _ = client_socket.recvfrom(65535)
        
        # Convert raw packet bytes back into a NumPy array
        np_array = np.frombuffer(packet, dtype=np.uint8)
        
        # Decode the JPEG array back into a viewable image frame
        frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        
        # If the packet was corrupted or partial, decoding might fail
        if frame is not None:
            # Display the video frame
            cv2.imshow("Live UDP Video Stream", frame)
        
        # Break loop if the user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\nStopping client...")

finally:
    client_socket.close()
    cv2.destroyAllWindows()
    print("Resources closed.")
