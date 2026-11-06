"""
UDP Echo Server (Lab 1 - Computer Network)
------------------------------------------
หลักการทำงาน
  1. สร้าง socket แบบ SOCK_DGRAM (UDP) ซึ่งไม่ต้องสร้างการเชื่อมต่อ (connectionless)
  2. bind กับ IP/Port ที่ต้องการ
  3. รอรับ datagram ด้วย recvfrom() ซึ่งจะได้ข้อมูลและที่อยู่ผู้ส่งมาด้วย
  4. ส่งข้อมูลเดิมกลับไปยังผู้ส่งด้วย sendto() (echo)
  5. ข้อความ "exit" ใช้แจ้งปิดการสนทนาฝั่ง client

วิธีรัน
  py -3 udp_echo_server.py
  py -3 udp_echo_server.py --port 5001
"""

import argparse
import socket
from datetime import datetime

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 5001
BUFFER_SIZE = 1024
EXIT_COMMAND = "exit"


def timestamp() -> str:
    return datetime.now().strftime("%H:%M:%S")


def main() -> None:
    parser = argparse.ArgumentParser(description="UDP Echo Server")
    parser.add_argument("--host", default=DEFAULT_HOST, help="IP ที่จะ bind (ค่าเริ่มต้น 0.0.0.0)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="พอร์ตที่ใช้ฟัง (ค่าเริ่มต้น 5001)")
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((args.host, args.port))
        print("=" * 55)
        print(" UDP ECHO SERVER กำลังทำงาน")
        print(f" ฟังที่ {args.host}:{args.port}  (กด Ctrl+C เพื่อหยุด)")
        print("=" * 55)

        try:
            while True:
                data, addr = server.recvfrom(BUFFER_SIZE)  # รอรับ datagram
                message = data.decode("utf-8", errors="replace").strip()
                print(f"[{timestamp()}] [RECV] จาก {addr[0]}:{addr[1]} -> {message}")

                if message.lower() == EXIT_COMMAND:
                    server.sendto(b"Bye! UDP session closed.\n", addr)
                    print(f"[{timestamp()}] [CLOSE] {addr[0]}:{addr[1]} แจ้งปิดการสนทนา")
                    continue

                reply = f"Echo from UDP server: {message}\n"
                server.sendto(reply.encode("utf-8"), addr)   # ส่งกลับผู้ส่งเดิม
                print(f"[{timestamp()}] [SEND] กลับไป {addr[1]}: {reply.strip()}")
        except KeyboardInterrupt:
            print(f"\n[{timestamp()}] ปิดเซิร์ฟเวอร์แล้ว")


if __name__ == "__main__":
    main()
