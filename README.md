# รายงานผลการทดลอง: Network Programming Lab 1

### ข้อมูลผู้จัดทำ

| รายการ | ข้อมูล |
| --- | --- |
| ชื่อ-นามสกุล | สกุลธเนศ กรรณฉวี |
| รหัสนักศึกษา | 6814952017 |
| รายวิชา | Computer Network — LAB 1 |
| GitHub | [Maikung](https://github.com/Maikung) |
| Repository | `networkPro-lab1-6814952017` |
| ภาษา / เครื่องมือ | Python 3.12.4 (`socket`), Git Command Line, Docker (เวอร์ชันคอนเทนเนอร์) |

---

### 🖥️ ผลการทดสอบการส่งข้อความ

#### รูปที่ 1: ภาพหน้าจอ Terminal ตอนทดสอบส่งข้อความระหว่าง Client-Server ของ TCP Echo
<img width="1518" height="363" alt="tcpserver" src="https://github.com/user-attachments/assets/6b2aa006-bef7-4e2d-8a0d-88d7a758f122" />

#### รูปที่ 2: ภาพหน้าจอ Terminal ตอนทดสอบส่งข้อความระหว่าง Client-Server ของ UDP Echo
<img width="1599" height="110" alt="udpserver" src="https://github.com/user-attachments/assets/e8566c01-cdc2-4735-8e65-97b7a28fd46b" />

---

## โครงสร้าง Repository

```
networkPro-lab1-6814952017/
├── tcp_echo_server/                 # เวอร์ชันรันบนเครื่อง (TCP)
│   ├── tcp_echo_server.py
│   └── tcp_echo_client.py
├── udp_server_test/                 # เวอร์ชันรันบนเครื่อง (UDP)
│   ├── udp_echo_server.py
│   └── udp_echo_client.py
├── ECHO_SERVER_TEST/                # เวอร์ชันรันผ่าน Docker (TCP)
│   ├── Dockerfile.server
│   ├── Dockerfile.client
│   ├── echo_server.py
│   └── echo_client.py
├── UDP_SERVER_TEST/                 # เวอร์ชันรันผ่าน Docker (UDP)
│   ├── Dockerfile.server
│   ├── Dockerfile.client
│   ├── udp_server.py
│   └── udp_client.py
├── screenshots/
│   ├── tcp_test.png                 # ภาพผลทดสอบ TCP (แนบใน README ด้านบน)
│   └── udp_test.png                 # ภาพผลทดสอบ UDP (แนบใน README ด้านบน)
├── .gitignore
└── README.md
```

## สภาพแวดล้อมที่ใช้ทดสอบ

| รายการ | ค่า |
| --- | --- |
| ระบบปฏิบัติการ | Windows |
| Python | 3.12.4 |
| TCP endpoint (รันบนเครื่อง) | `127.0.0.1:5000` |
| UDP endpoint (รันบนเครื่อง) | `127.0.0.1:5001` |
| TCP / UDP endpoint (Docker) | port `65432` ภายใน Docker network |

---

## ส่วนที่ 1 : TCP Echo Server

### หลักการทำงาน

1. สร้าง socket ด้วย `socket.socket(AF_INET, SOCK_STREAM)` (TCP)
2. `bind()` กับ IP/Port ที่ต้องการ แล้ว `listen()` เพื่อรอการเชื่อมต่อ
3. `accept()` รับ connection ใหม่ (เวอร์ชันรันบนเครื่องจะแยก thread ให้รองรับ client หลายราย)
4. `recv()` รับข้อความ แล้ว `sendall()` ส่งข้อความเดิมกลับไป (echo)
5. เมื่อ client ส่ง `exit` หรือปิด connection เซิร์ฟเวอร์จะปิดเฉพาะ connection นั้น

### วิธีรัน (บนเครื่อง)

```bash
# Terminal 1 : เริ่มเซิร์ฟเวอร์
py -3 tcp_echo_server/tcp_echo_server.py --port 5000

# Terminal 2 : เริ่ม client แล้วพิมพ์ข้อความ
py -3 tcp_echo_server/tcp_echo_client.py --port 5000
```

### ผลการทดสอบ

| ลำดับ | ข้อความที่ client ส่ง | ข้อความตอบกลับจากเซิร์ฟเวอร์ |
| --- | --- | --- |
| 1 | `Hello TCP Echo Server` | `Echo from TCP server: Hello TCP Echo Server` |
| 2 | `Network Lab 1 - message 2` | `Echo from TCP server: Network Lab 1 - message 2` |
| 3 | `Protocol: TCP works!` | `Echo from TCP server: Protocol: TCP works!` |
| 4 | `exit` | `Bye! Closing connection.` |

ข้อความตอบกลับตรงกับข้อความที่ส่งทุกครั้ง และเมื่อส่ง `exit` เซิร์ฟเวอร์ปิด connection ตามลำดับที่ถูกต้อง

`tcp_echo_server` แสดง log ฝั่งเซิร์ฟเวอร์ ([CONNECT] → [RECV] → [SEND] → [CLOSE] → [DISCONNECT]) และผลฝั่ง client ครบทุกข้อความ

---

## ส่วนที่ 2 : UDP Echo Server (udp_server_test)

### หลักการทำงาน

1. สร้าง socket ด้วย `socket.socket(AF_INET, SOCK_DGRAM)` (UDP)
2. `bind()` กับ IP/Port ที่ต้องการ — **ไม่ต้อง** `listen()` / `accept()` เพราะ UDP ไม่สร้าง connection
3. `recvfrom()` รับ datagram พร้อมที่อยู่ผู้ส่ง `(ip, port)`
4. `sendto()` ส่งข้อมูลเดิมกลับไปยังที่อยู่ผู้ส่งนั้น (echo)
5. ฝั่ง client ใช้ `settimeout()` กำหนดเวลารอ 5 วินาที เพื่อไม่ให้รอค้างหากไม่มีผู้ตอบกลับ

### วิธีรัน (บนเครื่อง)

```bash
# Terminal 1 : เริ่มเซิร์ฟเวอร์
py -3 udp_server_test/udp_echo_server.py --port 5001

# Terminal 2 : เริ่ม client แล้วพิมพ์ข้อความ
py -3 udp_server_test/udp_echo_client.py --port 5001
```

### ผลการทดสอบ

| ลำดับ | datagram ที่ client ส่ง | ข้อความตอบกลับจากเซิร์ฟเวอร์ |
| --- | --- | --- |
| 1 | `Hello UDP Echo Server` | `Echo from UDP server: Hello UDP Echo Server` |
| 2 | `Datagram 1 - no connection` | `Echo from UDP server: Datagram 1 - no connection` |
| 3 | `Protocol: UDP works!` | `Echo from UDP server: Protocol: UDP works!` |
| 4 | `exit` | `Bye! UDP session closed.` |

datagram ส่งถึงเซิร์ฟเวอร์และได้รับการตอบกลับครบทุกครั้ง โดยไม่มีการสร้าง connection ก่อนส่งข้อมูล

---

## เปรียบเทียบ TCP กับ UDP ที่ได้จากการทดลอง

| หัวข้อ | TCP (`SOCK_STREAM`) | UDP (`SOCK_DGRAM`) |
| --- | --- | --- |
| การเชื่อมต่อ | ต้อง `connect` / `accept` ก่อนส่งข้อมูล | ไม่ต้องเชื่อมต่อ ส่ง datagram ได้ทันที |
| ฟังก์ชันที่ใช้ | `listen`, `accept`, `recv`, `sendall` | `recvfrom`, `sendto` |
| ความน่าเชื่อถือ | มีลำดับและตรวจสอบความครบถ้วนของข้อมูล | ไม่รับประกันการถึงปลายทาง/ลำดับ |
| ลักษณะงานที่เหมาะ | งานที่ต้องถูกต้องครบถ้วน เช่น ไฟล์ เว็บ | งานที่เน้นความเร็ว/เรียลไทม์ เช่น วิดีโอ เกม |

---

## Screenshots

| หัวข้อ | ไฟล์ภาพใน Repository | URL ภาพจาก GitHub Issue |
| --- | --- | --- |
| ทดสอบ TCP Echo สำเร็จ | [`screenshots/tcp_test.png`](screenshots/tcp_test.png) | [รูปที่ 1](https://github.com/user-attachments/assets/6b2aa006-bef7-4e2d-8a0d-88d7a758f122) |
| ทดสอบ UDP Echo สำเร็จ | [`screenshots/udp_test.png`](screenshots/udp_test.png) | [รูปที่ 2](https://github.com/user-attachments/assets/e8566c01-cdc2-4735-8e65-97b7a28fd46b) |

> ภาพทั้งสองรูปอัปโหลดผ่าน GitHub ฟอร์ม (Issue/attachments) แล้วนำ URL มาใส่ใน README ตามหัวข้อ "ผลการทดสอบการส่งข้อความ" ด้านบน

---

## การส่งงาน / การตรวจงาน (Pull / Clone)

อาจารย์สามารถดาวน์โหลดโค้ดไปตรวจได้ด้วยคำสั่ง

```bash
git clone https://github.com/Maikung/networkPro-lab1-6814952017.git
cd networkPro-lab1-6814952017
```

ตรวจสอบไฟล์ที่ส่ง

```bash
ls -R
python --version   # ต้องมี Python 3.8 ขึ้นไป
```

## ขั้นตอนการส่งงานด้วย Git Command Line ที่ใช้จริง

```bash
git init
git add .
git commit -m "Lab 1: TCP echo server และ UDP echo server test"
git branch -M main
git remote add origin https://github.com/Maikung/networkPro-lab1-6814952017.git
git push -u origin main
```

## เวอร์ชันรันผ่าน Docker (ทางเลือก)

```bash
# TCP
docker build -f ECHO_SERVER_TEST/Dockerfile.server -t tcp-echo-server ECHO_SERVER_TEST
docker build -f ECHO_SERVER_TEST/Dockerfile.client -t tcp-echo-client ECHO_SERVER_TEST
docker network create echo-net
docker run -d --name echo_server --network echo-net tcp-echo-server
docker run -it --network echo-net tcp-echo-client
```
