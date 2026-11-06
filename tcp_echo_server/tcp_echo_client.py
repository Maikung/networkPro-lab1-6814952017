"""
TCP Echo Client (Lab 1 - Computer Network)
------------------------------------------
ใช้ทดสอบ TCP Echo Server: เชื่อมต่อ, ส่งข้อความ, รับข้อความตอบกลับ

วิธีรัน
  py -3 tcp_echo_client.py
  py -3 tcp_echo_client.py --host 127.0.0.1 --port 5000
"""

import argparse
import socket

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5000
BUFFER_SIZE = 1024


def main() -> None:
    parser = argparse.ArgumentParser(description="TCP Echo Client")
    parser.add_argument("--host", default=DEFAULT_HOST, help="IP ของเซิร์ฟเวอร์ (ค่าเริ่มต้น 127.0.0.1)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="พอร์ตของเซิร์ฟเวอร์ (ค่าเริ่มต้น 5000)")
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((args.host, args.port))
        print(f"เชื่อมต่อ TCP server ที่ {args.host}:{args.port} สำเร็จ")
        print("พิมพ์ข้อความแล้วกด Enter (พิมพ์ exit เพื่อออก)\n")

        while True:
            try:
                message = input("ข้อความที่ต้องการส่ง: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if not message:
                continue

            client.sendall(message.encode("utf-8"))      # ส่งข้อมูล
            reply = client.recv(BUFFER_SIZE).decode("utf-8")  # รับข้อมูลตอบกลับ
            print(f"ตอบกลับจากเซิร์ฟเวอร์: {reply.strip()}")

            if message.lower() == "exit":
                break

    print("ปิดการเชื่อมต่อแล้ว")


if __name__ == "__main__":
    main()
