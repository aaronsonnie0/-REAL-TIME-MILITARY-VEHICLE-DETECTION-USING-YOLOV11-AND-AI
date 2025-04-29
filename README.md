# Venus AQI & Threat Detection System

## Overview
Venus is a robust Air Quality Index (AQI) and threat detection system that leverages advanced computer vision (YOLO), natural language AI (Gemini API), and automated alerting to provide real-time monitoring, analysis, and notifications for environmental and security scenarios. The system is designed for both image and video input, supports chatbot-style AQI queries, and can send immediate email alerts for detected threats.

---

## Features

### 1. YOLO-based Threat Detection
- **Image & Video Support:** Detects objects (e.g., tanks, vehicles) in both images and video streams.
- **Default YOLO Visualization:** Uses YOLO's built-in `plot()` for clean, standard bounding box and label overlays.
- **Threat Level Assessment:** Integrates with Gemini API to classify and summarize threat levels based on detections.

### 2. AQI Monitoring & Chatbot
- **AQI Tracker Page:**
  - Locate user by public IP and estimate AQI for their city using Gemini API.
  - Simple chatbot interface for AQI and environmental queries.
- **No WAQI API Needed:** AQI estimation is now fully handled by Gemini API.

### 3. Email Alert System
- **Automated Alerts:** Sends email notifications for any detected threat (not just high threat levels).
- **Configurable Recipient:** By default, sends to `aaronsonnie@gmail.com`.
- **Security:** Uses Gmail SMTP with app password (recommended for safety).

### 4. Dashboard
- **Detection Log:** Visualizes and stores detection results, threat levels, and feedback.
- **Warning Suppression:** Skips malformed rows silently for a cleaner dashboard experience.

### 5. Customization & Extensibility
- **Configurable Model & Input:** Easily change YOLO model path and input file/video in `main.py`.
- **Easy Style Tweaks:** Can switch between default YOLO plotting or custom overlays for bounding boxes and labels.

---

## Tech Stack

- **Python 3.x**
- **YOLO (Ultralytics):** Object detection
- **OpenCV:** Image and video processing
- **Gemini API:** Natural language feedback and AQI estimation
- **SMTP (smtplib):** Email alerting
- **Tkinter (optional):** For UI components (if used)
- **Other:** dotenv for environment variables, csv for logging

---

## Key Files & Functions

- `main.py`
  - **Main pipeline:** Handles input (image/video), runs YOLO, triggers Gemini feedback, and manages alerts.
  - **get_gemini_feedback:** Processes detection results, queries Gemini API, and triggers email alerts.
- `email_alert.py`
  - **send_alert_email:** Sends formatted email notifications using Gmail SMTP.
- `dashboard.py`
  - **Dashboard logic:** Loads and displays detection logs, suppresses warnings.

---

## Setup & Usage

1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
2. **Configure environment:**
   - Place your YOLO model at the path specified in `main.py` (`YOLO_MODEL_PATH`).
   - Set your Gemini API key and Gmail app password in a `.env` file.
3. **Run detection:**
   ```sh
   python main.py
   ```
   - For image: Set `INPUT_PATH` to an image file.
   - For video: Set `INPUT_PATH` to a video file.
4. **View results:**
   - Annotated output saved in the `outputs/` folder.
   - Alerts sent via email if threats are detected.
   - Dashboard (if enabled) shows detection history.

---

## Security & Notes
- **Email Security:** Always use an app password for Gmail SMTP.
- **API Keys:** Never share your Gemini API key or app password publicly.
- **Extensibility:** The codebase is modular—add more detectors, APIs, or alert channels as needed.

---

## Credits & License
- Built by Aaron Sonnie
- For research, security, and environmental monitoring applications.
- See LICENSE for usage terms.

---

## Contact
For questions, improvements, or bug reports, contact [aaronsonnie@gmail.com](mailto:aaronsonnie@gmail.com)
