# 🪻 SmartGreen AI: Intelligent Greenhouse Management System

<div align="center">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/AI-Computer_Vision-8A2BE2?style=for-the-badge" />
  <img src="https://img.shields.io/badge/IoT-ESP_Microcontrollers-00BFFF?style=for-the-badge" />
  <br><br>
  <i>💜 A next-generation, AI-powered IoT platform for real-time greenhouse monitoring, automated sensor control, and live plant identification. 💙</i>
</div>

---

## 🌌 Overview

**SmartGreen AI** is a comprehensive Django-based web application designed to revolutionize greenhouse management. It seamlessly integrates **IoT sensor networks** with **Advanced Computer Vision AI**. 

Featuring a stunning, modern **Purple & Blue UI theme**, the dashboard provides real-time insights, live video feeds with AI object detection, and complete plant identification capabilities.

### ✨ Core Features
- 🎨 **Stunning UI/UX:** A sleek, modern dashboard built with a mesmerizing **Purple & Blue** gradient theme.
- 🌡️ **IoT Sensor Management:** Real-time monitoring of temperature, humidity, soil moisture, and light. Control actuators (pumps, fans) manually or via AI auto-mode.
- 🧠 **Full AI Plant Identification:** Upload or capture images to identify plant species, health status, and growth stages using deep learning.
- 📹 **Live AI Detection:** Real-time video streaming from greenhouse cameras with live bounding-box object detection.
- 📊 **Analytics & Logs:** Historical data tracking, event logging, and statistical insights for optimal crop yield.

---

## 🚀 Getting Started

Follow these steps to set up the project locally. 

### 1️⃣ Clone the Repository

```
git clone https://github.com/YasinSamooei/SmartGreenhouse.git
cd SmartGreenhouse/Dashboard
```

### 2️⃣ Create & Activate Virtual Environment

```
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Requirements
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
*(Note: If you are using AI/CV features, ensure you have the necessary system dependencies like `opencv-python`, `pytorch`, etc., installed).*

### 4️⃣ Environment Variables
Create a `.env` file in the root directory and add your configurations:
```env
SECRET_KEY=your_super_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
# Add Camera/API keys if necessary
```

### 5️⃣ Database Migrations
Apply the initial migrations to set up the database schema:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Create the First Admin User (Superuser)
To access the admin panel and dashboard, create your first user:
```bash
python manage.py createsuperuser
```
*Follow the prompts to enter a username, email, and strong password.*

### 7️⃣ Run the Development Server
```bash
python manage.py runserver
```
🌐 **Access the application:** Open your browser and navigate to `http://127.0.0.1:8000/`

---

## 🗺️ URL Routing & API Endpoints

The project is modularized into three main Django apps. Below is the complete routing map.

### 🎛️ 1. Control Panel (`app_name = "panel"`)
The main dashboard and UI for greenhouse administrators.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | **Admin Dashboard Home** (Main UI) |
| `GET/POST`| `/panel/login` | **Login Page** for authentication |
| `GET` | `/logout/` | **Logout** and redirect to home |
| `GET` | `/plant/list` | **Plant List** (View all identified plants) |
| `GET` | `/plant/detail/<int:pk>` | **Plant Detail** (Specific plant info & AI data) |
| `POST/GET`| `/plant/delete/<int:pk>` | **Delete Plant** record from database |

### 📡 2. Embedded / IoT System (`app_name = "embedded"`)
Handles communication between the Django server, the web dashboard, and the ESP/Microcontrollers.

#### Dashboard & Data Fetching (For the Web UI)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/display/sensors/page` | **Sensor Display Page** (Visual UI for sensors) |
| `GET` | `/get/sensor/data` | Fetch **current live sensor values** |
| `GET` | `/get/sensor/history/` | Fetch **historical sensor data** (for charts) |
| `GET` | `/get/log/stats/` | Fetch **system logs and statistics** |
| `GET` | `/get/events/` | Fetch **system events/alerts** |
| `POST` | `/api/events/mark-seen/` | Mark an event/alert as **read/seen** |
| `POST` | `/toggle-actuator/` | **Toggle actuators** (e.g., water pump, fan) from UI |

#### Microcontroller Communication (For ESP/IoT Devices)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/send/sensor/value` | ESP sends **live sensor readings** to server |
| `POST` | `/api/send-command/` | Send **direct commands** to the ESP |
| `GET` | `/api/get-actuator-status/`| ESP sends **current actuator states** |
| `POST` | `/api/send-auto-mode/` | Toggle **Auto-Mode** (Server controls actuators based on Manual/Sensors) |

### 🧠 3. AI Plant Detection (`app_name = "plant"`)
Handles the computer vision, live video streaming, and plant identification logic.

#### Detection & Statistics
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET/POST`| `/detect/plants` | **Detect Plants** (Process image and identify) |
| `GET` | `/plant-count/` | Get **total count** of detected/identified plants |

#### Live Video & Camera Streaming
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/video-stream/` | **Live Detection Page** (HTML page with video player) |
| `GET` | `/video-feed/` | **MJPEG Video Feed** (Raw stream for `<img>` tags) |

#### AI & Camera APIs
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/get-frame/` | Fetch a **single processed frame** with AI bounding boxes |
| `GET` | `/api/camera-status/` | Check if the **camera is online/offline** |
| `POST` | `/api/save-detection/` | **Save a specific detection** result to the database |
| `GET` | `/api/get-frame-batch/` | Fetch a **batch of frames** for batch processing |

---

## 🎨 UI Theme & Design

The frontend embraces a **Cyber-Botanical** aesthetic. 
- **Primary Colors:** Deep Space Purple (`#2D1B4E`) and Neon Blue (`#00BFFF`).
- **Accents:** Glowing gradients, glassmorphism cards, and smooth transitions.
- **Experience:** Dark-mode native, reducing eye strain for 24/7 greenhouse monitoring.

---

## 🛠️ Tech Stack

- **Backend:** Django, Django REST Framework (DRF)
- **Frontend:** HTML5, CSS3, JavaScript (with Purple/Blue custom theme)
- **AI/CV:** OpenCV, PyTorch (for plant identification & live detection)
- **IoT:** MQTT / HTTP REST APIs for ESP32/ESP8266 communication
- **Database:** SQLite (Dev) / PostgreSQL (Production)

---

<div align="center">
  <i>💜 Cultivating the future with code and AI 💙</i>
  <br>
  <b>Made with 🧠 by YasinSamooei</b>
</div>





