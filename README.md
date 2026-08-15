# ⚡ AutoMacro Studio - Visual Scratch & Automation Studio

**AutoMacro Studio** เป็นเว็บแอปพลิเคชันสำหรับสร้างสคริปต์ทำงานอัตโนมัติ (Automation Scripts) ผ่านหน้าเว็บอินเตอร์เฟสแบบบล็อก (Visual Block Workspace) คล้ายกับระบบ Scratch ช่วยให้ผู้ใช้งานสามารถคลิกเลือกหรือลากวางคำสั่งทำงานต่าง ๆ เช่น การคลิกเมาส์ตามพิกัด, การกดปุ่มคีย์บอร์ด, การกำหนดเวลาหน่วงหน่วง (Delay), รวมถึงการประยุกต์ใช้เทคโนโลยี Computer Vision และ OCR เพื่อตรวจสอบหน้าจอ จากนั้นระบบจะสร้างสคริปต์อัตโนมัติออกมาในรูปแบบของภาษาต่าง ๆ ที่พร้อมดาวน์โหลดไปรันบนระบบของตนเองได้ทันที

---

## 🚀 คุณสมบัติเด่น (Key Features)

1. **Visual Block Workspace**: อินเตอร์เฟสเพิ่มบล็อกคำสั่ง เช่น เมาส์คลิก (X, Y), ปุ่มกดคีย์บอร์ด, หน่วงเวลา (Delay), ตรวจจับภาพ (Template Match) และสแกนข้อความบนจอ (OCR)
2. **Multi-Language Generation**: สามารถเลือกคอมไพล์สคริปต์อัตโนมัติออกมาได้ 3 ภาษา:
   - 🐍 **Python** (ใช้ไลบรารี `PyAutoGUI`)
   - ⚡ **AutoHotkey** (ไฟล์ `.ahk` สำหรับ Windows)
   - 🐧 **Bash Script** (ใช้เครื่องมือ `xdotool` สำหรับ Linux)
3. **Controlled Web Sandbox & Analytics**: จำลองและทดสอบการทำงานของลำดับคำสั่งที่ตั้งไว้บนหน้าเว็บ Sandbox โดยตรง พร้อมแสดงผล Log แบบเรียลไทม์ และคำนวณประสิทธิภาพความเร็วในการทำงาน (Efficiency Analytics) พร้อมคำแนะนำจาก AI
4. **Computer Vision & OCR Lab**:
   - **Template Matching**: ค้นหาพิกัดของภาพต้นแบบ (Template Image) บนภาพหน้าจอหลัก
   - **OCR Text Extraction**: ดึงข้อความออกมาจากรูปภาพหน้าจอ
   - **Object Counter**: ค้นหาและนับจำนวนอ็อบเจ็กต์/รูปร่างบนภาพหน้าจอ
5. **Desktop Coordinate Inspector**: ระบบแสดงพิกัดเมาส์ของหน้าจอ Desktop จริง ๆ แบบเรียลไทม์ เพื่อช่วยในการกำหนดพิกัด X, Y บนบอร์ด
6. **User Authentication & Auth Security**: ระบบสมัครสมาชิก ล็อกอิน เพื่อความปลอดภัยในการจัดการสคริปต์ด้วย JWT Session token และการแฮชรหัสผ่านด้วย Bcrypt

---

## 📂 โครงสร้างของระบบ (Detailed Directory Structure)

โปรเจ็กต์นี้พัฒนาแบบ Layered Architecture ด้วยเฟรมเวิร์ก **FastAPI** ในส่วนของ Back-end และ **Vanilla CSS/JS** ในส่วนของ Front-end ดังนี้:

```text
AutomaticMacro/
├── app/                             # โค้ดหลักของแอปพลิเคชัน (FastAPI backend & Frontend)
│   ├── api/                         # ส่วนของ API Routes ทั้งหมด
│   │   ├── v1/                      # API เวอร์ชั่น 1
│   │   │   ├── endpoints/           # แยก Router ตามโมดูลของฟังก์ชันการใช้งาน
│   │   │   │   ├── auth_router.py   # จัดการการลงชื่อเข้าใช้งาน (Login) และออกระบบ (Logout)
│   │   │   │   ├── health_router.py # API ตรวจสอบสถานะการเชื่อมต่อของ Server
│   │   │   │   ├── runner_router.py # รับคำสั่งไปรันบน Sandbox และเรียกใช้ Analytics
│   │   │   │   ├── script_router.py # รับบล็อคคำสั่งแล้วแปลงเป็น Source Code (Python, AHK, Bash) และดาวน์โหลด
│   │   │   │   ├── user_router.py   # จัดการข้อมูลโปรไฟล์ผู้ใช้และการสมัครสมาชิก
│   │   │   │   └── vision_router.py # บริการจัดการ Computer Vision, OCR และพิกัดเมาส์เรียลไทม์
│   │   │   └── api_v1.py            # จุดรวมและจัดกลุ่ม Endpoint Router ทั้งหมดของ v1
│   │   └── dependencies.py          # คลาสควบคุม dependency injection เช่น การดึง Current User จาก JWT Token
│   ├── core/                        # การตั้งค่าแกนกลางและระบบรักษาความปลอดภัย
│   │   ├── exceptions.py            # รวบรวม Custom Exception คลาสข้อผิดพลาดที่สร้างขึ้นมาโดยเฉพาะ
│   │   └── security.py              # ระบบแฮชรหัสผ่าน (Bcrypt) และออกตั๋ว JWT Token สำหรับ Session
│   ├── db/                          # ส่วนติดต่อฐานข้อมูล (Database Access Layer)
│   │   ├── models/                  # รวม Database ORM Models
│   │   │   └── user.py              # โมเดลตารางผู้ใช้งาน (User Table Schema) ในระบบ
│   │   ├── base.py                  # การตั้งค่า Declarative Base ของ SQLAlchemy
│   │   └── session.py               # ตัวสร้าง session ในการเขียน/อ่านฐานข้อมูล SQLite
│   ├── engine/                      # โมดูลกลไกการแปลงสคริปต์ ตรวจจับภาพ และประมวลผล
│   │   ├── analytics/               # บริการวิเคราะห์การรันสคริปต์
│   │   │   └── script_analyzer.py   # คลาสประเมินค่า Efficiency และข้อเสนอแนะในการปรับแต่งสคริปต์
│   │   ├── runner/                  # ส่วนจำลองรันสคริปต์บนเว็บ
│   │   │   └── web_runner.py        # รันคำสั่ง Automation (คลิก, คีย์บอร์ด) บนระบบ sandbox และบันทึก Log
│   │   ├── strategies/              # คลาสยุทธวิธี (Strategy Pattern) สำหรับแปลงเป็นภาษาต่างๆ
│   │   │   ├── ahk_generator.py     # ตัวแปลงคำสั่งเป็นภาษา AutoHotkey (.ahk)
│   │   │   ├── bash_generator.py    # ตัวแปลงคำสั่งเป็นสคริปต์ทุบตี Linux (Bash xdotool)
│   │   │   └── python_generator.py  # ตัวแปลงคำสั่งเป็นภาษา Python (PyAutoGUI)
│   │   ├── vision/                  # ระบบตรวจสอบภาพและดึงข้อมูลอักษร
│   │   │   ├── object_counter.py    # ตรวจจับวัตถุและนับจำนวนบนรูปภาพหน้าจอ
│   │   │   ├── ocr_engine.py        # ถอดตัวอักษรและข้อความออกจากรูปภาพ
│   │   │   └── template_matcher.py  # หาพิกัดภาพเล็กที่ซ้อนอยู่ในหน้าจอภาพใหญ่
│   │   ├── base_generator.py        # Interface/Base class สำหรับสคริปต์เจเนอเรเตอร์
│   │   └── script_engine.py         # คลาสประสานงานเลือกใช้ Strategy ในการออกสคริปต์
│   ├── schemas/                     # โครงสร้าง Validation ข้อมูล (Pydantic Models)
│   │   ├── action_schema.py         # โครงสร้างของคำสั่งแต่ละบล็อก (คลิก, คีย์บอร์ด, Delay)
│   │   ├── auth_schema.py           # โครงสร้างสำหรับรับส่งข้อมูล Login และจัดการ JWT Token
│   │   ├── generator_schema.py      # โครงสร้าง payload สำหรับขอเจเนอเรตสคริปต์
│   │   └── user_schema.py           # โครงสร้างข้อมูลสมาชิกและการสมัครบัญชีใหม่
│   ├── services/                    # Business Logic Layer
│   │   └── script_service.py        # บริการประสานงานการเรียก Generator Engine
│   ├── static/                      # ไฟล์หน้าบ้าน (Frontend Static Resources)
│   │   ├── css/                     # โฟลเดอร์เก็บไฟล์ตกแต่งสไตล์เว็บ
│   │   │   └── style.css            # ไฟล์ CSS ตกแต่ง UX/UI สไตล์ดาร์กโหมดนีออน (Glassmorphism)
│   │   ├── js/                      # โฟลเดอร์เก็บไฟล์ตรรกะ JavaScript ฝั่งไคลเอนต์
│   │   │   └── app.js               # Logic หลักในการคุม Block chain, API calls, dynamic Tabs
│   │   ├── desktop_tracker.py       # สคริปต์ไคลเอนต์เสริมสำหรับรันเช็คพิกัดเมาส์
│   │   └── index.html               # หน้า UI Dashboard หลักของเว็บสตูดิโอ
│   └── utils/                       # ฟังก์ชันตัวช่วยอำนวยความสะดวกทั่วไป
│       ├── desktop_tracker.py       # คลาสเสริมในการส่งออกสถานะพิกัดเมาส์
│       └── file_exporter.py         # ตัวเตรียมดาวน์โหลดไฟล์สคริปต์กลับไปยังผู้ใช้
├── tests/                           # ชุดตรวจสอบการทำงานอัตโนมัติ (Automated Tests)
│   ├── test_api.py                  # เทสพาร์ท API ส่วนแปลงโค้ดและส่งออกไฟล์
│   ├── test_engine.py               # เทสเอนจินของ Strategy แต่ละภาษา
│   └── test_full_api.py             # ชุด Integration test ครอบคลุมพฤติกรรม API
├── Dockerfile                       # การตั้งค่า Docker image สำหรับรันระบบ
├── docker-compose.yml               # ตั้งค่า Orchestration รันเว็บและฐานข้อมูล
├── main.py                          # จุดเริ่มทำงานหลัก (Main Entrypoint) ของ FastAPI app
├── requirements.txt                 # รายการไลบรารีที่โปรเจ็กต์ต้องการใช้งาน
├── run_local.bat                    # สคริปต์วินโดวส์เพื่อรัน Server ในเครื่องแบบด่วน
└── run_local.py                     # สคริปต์ไพธอนในการจำลองรัน API Server พร้อมจำลองพิกัด
```

---

## 🛠️ วิธีการติดตั้งและเริ่มใช้งานในเครื่อง (Getting Started)

### 1. โคลนและเตรียม Python Environment
```bash
# ลง dependency จากไฟล์ข้อกำหนด
pip install -r requirements.txt
```

### 2. รันแอปพลิเคชันเครื่องตัวเอง (Local)
คุณสามารถรันแอปพลิเคชันได้หลายวิธี:

- **รันผ่านไฟล์สคริปต์อำนวยความสะดวก:**
  ```bash
  python run_local.py
  ```
  หรือคลิกดับเบิ้ลคลิกไฟล์ `run_local.bat` บนระบบ Windows

- **หรือรันโดยตรงผ่าน uvicorn:**
  ```bash
  uvicorn main:app --reload --port 8000
  ```

หลังจากเซิร์ฟเวอร์เปิดขึ้นมาแล้ว ให้เปิดเว็บบราวเซอร์ไปที่:
- หน้าหลัก **Web UI Studio**: [http://localhost:8000](http://localhost:8000)
- หน้าคู่มือ **Interactive API Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🐳 รันผ่าน Docker

สามารถใช้งานผ่าน Docker / Docker-Compose ได้เช่นเดียวกัน:
```bash
docker-compose up --build
```
ระบบจะเปิดให้บริการที่ [http://localhost:8000](http://localhost:8000)
