"""
UDP Echo Client (Lab 1 - Computer Network)
------------------------------------------
ใช้ทดสอบ UDP Echo Server: ส่ง datagram ไปแล้วรอรับ datagram ตอบกลับ
จุดสังเกต: UDP ไม่มีการ connect จริง จึงต้องกำหนด timeout เองเพื่อไม่ให้รอค้าง

วิธีรัน
  py -3 udp_echo_client.py
  py -3 udp_echo_client.py --host 127.0.0.1 --port 5001
"""

import argparse
import socket

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5001
BUFFER_SIZE = 1024
TIMEOUT_SECONDS = 5.0


def main() -> None:
    parser = argparse.ArgumentParser(description="UDP Echo Client")
    parser.add_argument("--host", default=DEFAULT_HOST, help="IP ของเซิร์ฟเวอร์ (ค่าเริ่มต้น 127.0.0.1)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="พอร์ตของเซิร์ฟเวอร์ (ค่าเริ่มต้น 5001)")
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.settimeout(TIMEOUT_SECONDS)  # กันรอค้างถ้าไม่มีใครตอบกลับ
        print(f"พร้อมส่ง UDP datagram ไปที่ {args.host}:{args.port}")
        print("พิมพ์ข้อความแล้วกด Enter (พิมพ์ exit เพื่อออก)\n")

        while True:
            try:
                message = input("ข้อความที่ต้องการส่ง: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if not message:
                continue

            client.sendto(message.encode("utf-8"), (args.host, args.port))  # ส่งข้อมูล
            try:
                reply, server_addr = client.recvfrom(BUFFER_SIZE)          # รอรับตอบกลับ
                print(f"ตอบกลับจากเซิร์ฟเวอร์ {server_addr[0]}:{server_addr[1]}: {reply.decode('utf-8').strip()}")
            except socket.timeout:
                print(f"ไม่ได้รับการตอบกลับภายใน {TIMEOUT_SECONDS} วินาที")

            if message.lower() == "exit":
                break

    print("ปิดการสนทนา UDP แล้ว")


if __name__ == "__main__":
    main()
