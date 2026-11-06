# echo_client.py
import socket

HOST = 'echo_server'  # ชื่อ container ของ server ใน Docker network
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    print("Connected to server.")

    while True:
        message = input("Enter message to send to server (type 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)
        print("Received from server:", data.decode())