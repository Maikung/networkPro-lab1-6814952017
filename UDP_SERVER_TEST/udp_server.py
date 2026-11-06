# udp_server.py
import socket

HOST = '0.0.0.0'  # IP ที่รับการเชื่อมต่อจาก client ทั้งหมด
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind((HOST, PORT))
    print("UDP Server is listening on port", PORT)

    while True:
        data, addr = server_socket.recvfrom(1024)
        print("Received from client:", data.decode())
        server_socket.sendto(data, addr)
