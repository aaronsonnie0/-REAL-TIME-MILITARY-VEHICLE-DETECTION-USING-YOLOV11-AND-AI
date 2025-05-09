# REAL-TIME MILITARY VEHICLE DETECTION AND CONTEXTUAL ALERT SYSTEM USING YOLOV11 AND CONVERSATIONAL AI

## Overview
This project is a real-time military vehicle detection and contextual alert system that leverages YOLOv11 for object detection and integrates conversational AI (Gemini API) for generating actionable, context-aware alerts. The system processes images or video streams, detects military vehicles, assesses threat levels, and issues both on-screen and email alerts. A Streamlit dashboard visualizes detection history and threat assessments.

---

## Features

- **YOLOv11-based Military Vehicle Detection:**
  - Detects and classifies military vehicles in images and videos.
  - Supports real-time and batch processing.
- **Contextual Alerts with Conversational AI:**
  - Uses Gemini API to summarize detections and assess threat levels (Low/Medium/High).
  - Generates human-readable, actionable feedback for operators.
- **Automated Voice and Email Alerts:**
  - Text-to-speech voice alerts for immediate feedback.
  - Sends email notifications for any detected threat.
- **Detection Logging and Dashboard:**
  - Logs detections, threat levels, and AI feedback to CSV.
  - Streamlit dashboard displays detection history and recent annotated images.
- **Configurable and Extensible:**
  - Easily update model paths, input sources, and alert recipients.
  - Modular design for adding new detectors or alert channels.

---

## Tech Stack
- **Python 3.x**
- **YOLOv11 (Ultralytics)** for object detection
- **OpenCV** for image/video processing
- **Gemini API** for contextual AI feedback
- **pyttsx3** for voice alerts
- **Streamlit** for dashboard UI
- **smtplib** for email notifications

---

## Key Files
- `main.py`: Main pipeline for detection, feedback generation, and alerting.
- `email_alert.py`: Handles sending email notifications.
- `dashboard.py`: Streamlit dashboard for log visualization.
- `detection_log.csv`: Stores detection events and threat assessments.
- `outputs/`: Annotated output images and frames.
- `requirements.txt`: Python dependencies.

---

## Setup & Usage

1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
2. **Configure environment:**
   - Place your YOLOv11 model (`Yolov11.pt`) at the path specified by `YOLO_MODEL_PATH` in `main.py`.
   - Set your Gemini API key and Gmail app password (for alerts) in the code or a `.env` file.
3. **Run detection:**
   ```sh
   python main.py
   ```
   - Edit `INPUT_PATH` in `main.py` to point to your image or video file.
4. **View dashboard:**
   ```sh
   streamlit run dashboard.py
   ```
5. **Check outputs:**
   - Annotated images/frames saved in `outputs/`.
   - Detection logs in `detection_log.csv`.
   - Email alerts sent to configured recipients.

---

## Security & Notes
- **Email Security:** Use an app password for Gmail SMTP.
- **API Keys:** Do not share your Gemini API key or email credentials.
- **Extensibility:** Modular code—add new detectors, APIs, or alert methods as needed.

---

## Credits & License
- Developed by Aaron Sonnie
- For research, security, and military monitoring applications.
- See LICENSE for terms.

---

## Contact
For questions or suggestions, contact [aaronsonnie@gmail.com](mailto:aaronsonnie@gmail.com)
