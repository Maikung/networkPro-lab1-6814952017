# echo_server.py
import socket

HOST = '0.0.0.0'  # IP ที่รับการเชื่อมต่อจาก client ทั้งหมด
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("Server is listening on port", PORT)

    conn, addr = server_socket.accept()
    with conn:
        print("Connected by", addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print("Received from client:", data.decode())
            conn.sendall(data)