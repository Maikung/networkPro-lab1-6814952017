"""
TCP Echo Server (Lab 1 - Computer Network)
------------------------------------------
หลักการทำงาน
  1. สร้าง socket แบบ SOCK_STREAM (TCP)
  2. bind กับ IP/Port ที่ต้องการ แล้ว listen() รอ client เชื่อมต่อ
  3. เมื่อมี client เชื่อมต่อ จะ accept() ออกมาเป็น connection ใหม่
  4. อ่านข้อมูลด้วย recv() แล้วส่งกลับไปให้ client ด้วย sendall() (echo)
  5. ถ้า client พิมพ์ "exit" หรือปิดการเชื่อมต่อ เซิร์ฟเวอร์จะปิด connection นั้น

วิธีรัน
  py -3 tcp_echo_server.py                 # ฟังที่ 0.0.0.0:5000
  py -3 tcp_echo_server.py --port 6000     # เปลี่ยนพอร์ต
"""

import argparse
import socket
import threading
from datetime import datetime

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 5000
BUFFER_SIZE = 1024
EXIT_COMMAND = "exit"


def timestamp() -> str:
    """เวลาปัจจุบันสำหรับใส่ใน log"""
    return datetime.now().strftime("%H:%M:%S")


def handle_client(conn: socket.socket, addr: tuple) -> None:
    """รับ-ส่งข้อมูลกับ client หนึ่งราย (ทำงานใน thread แยก)"""
    print(f"[{timestamp()}] [CONNECT] {addr[0]}:{addr[1]} เชื่อมต่อเข้ามา")
    with conn:
        while True:
            data = conn.recv(BUFFER_SIZE)          # รอรับข้อมูลจาก client
            if not data:                           # client ปิดการเชื่อมต่อ
                break
            message = data.decode("utf-8", errors="replace").strip()
            print(f"[{timestamp()}] [RECV] จาก {addr[1]}: {message}")

            if message.lower() == EXIT_COMMAND:
                conn.sendall(b"Bye! Closing connection.\n")
                print(f"[{timestamp()}] [CLOSE] {addr[0]}:{addr[1]} แจ้งปิดการเชื่อมต่อ")
                break

            reply = f"Echo from TCP server: {message}\n"
            conn.sendall(reply.encode("utf-8"))    # ส่งข้อความเดิมกลับไป (echo)
            print(f"[{timestamp()}] [SEND] กลับไป {addr[1]}: {reply.strip()}")

    print(f"[{timestamp()}] [DISCONNECT] {addr[0]}:{addr[1]} ออกจากระบบ")


def main() -> None:
    parser = argparse.ArgumentParser(description="TCP Echo Server")
    parser.add_argument("--host", default=DEFAULT_HOST, help="IP ที่จะ bind (ค่าเริ่มต้น 0.0.0.0)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="พอร์ตที่ใช้ฟัง (ค่าเริ่มต้น 5000)")
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        # ให้รันซ้ำได้ทันทีหลังปิดโปรแกรม โดยไม่ติด error "Address already in use"
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((args.host, args.port))
        server.listen(5)  # รองรับคิวการเชื่อมต่อสูงสุด 5 ราย

        print("=" * 55)
        print(" TCP ECHO SERVER กำลังทำงาน")
        print(f" ฟังที่ {args.host}:{args.port}  (กด Ctrl+C เพื่อหยุด)")
        print("=" * 55)

        try:
            while True:
                conn, addr = server.accept()  # รอ client รายถัดไป
                # เปิด thread ใหม่เพื่อให้รับ client ได้หลายรายพร้อมกัน
                threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
        except KeyboardInterrupt:
            print(f"\n[{timestamp()}] ปิดเซิร์ฟเวอร์แล้ว")


if __name__ == "__main__":
    main()
