# udp_client.py
import socket

HOST = 'udp_server'  # ชื่อ container ของ server ใน Docker network
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    print("Connected to UDP server.")

    while True:
        message = input("Enter message to send to server (type 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        client_socket.sendto(message.encode(), (HOST, PORT))
        data, _ = client_socket.recvfrom(1024)
        print("Received from server:", data.decode())
