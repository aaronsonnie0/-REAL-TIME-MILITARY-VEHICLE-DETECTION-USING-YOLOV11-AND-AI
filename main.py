import cv2
import os
import numpy as np
import pyttsx3
from ultralytics import YOLO
import google.generativeai as genai

# -----------------------------------
# CONFIGURATION
# -----------------------------------

YOLO_MODEL_PATH = "C:\\Users\\aaron.sonnie\\OneDrive - GEP\\Desktop\\11 yolo\\Yolov11.pt"
INPUT_PATH = r"C:\Users\aaron.sonnie\Downloads\venus\q.png"
GEMINI_API_KEY = "AIzaSyD55ijNQYc58WCeChvC24b4MpUEgMHJBVg"
VOICE_SPEED = 150

# -----------------------------------
# Initialize YOLO and Gemini
# -----------------------------------

yolo_model = YOLO(YOLO_MODEL_PATH)

genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# -----------------------------------
# Voice Alert Function
# -----------------------------------

def speak(text, speed=VOICE_SPEED):
    engine = pyttsx3.init()
    engine.setProperty('rate', speed)
    engine.say(text)
    engine.runAndWait()

# -----------------------------------
# Gemini Feedback Generator
# -----------------------------------

def get_gemini_feedback(results, output_path, input_type):
    import csv
    from datetime import datetime
    frame = results[0]
    detected_objects = []
    classes = []
    confidences = []
    for box in frame.boxes:
        class_id = int(box.cls[0])
        class_name = frame.names[class_id]
        conf = float(box.conf[0])
        detected_objects.append(f"{class_name} ({conf*100:.1f}%)")
        classes.append(class_name)
        confidences.append(f"{conf*100:.1f}")
    if not detected_objects:
        print("No objects detected.")
        return ""
    # Multi-object prompt
    prompt = (
        f"You are a military alert system providing real-time intelligence. "
        f"Detected units: {', '.join(detected_objects)}. "
        f"Generate a concise, actionable alert covering all units, threat level (Low/Medium/High), and any relevant movement/location info."
    )
    response = gemini_model.generate_content(prompt)
    feedback = response.text.strip()
    print(f" Detected: {', '.join(detected_objects)}")
    print(f" Gemini Feedback: {feedback}")
    speak(feedback)
    # Extract threat level if present
    threat_level = ""
    for level in ["high", "medium", "low"]:
        if level in feedback.lower():
            threat_level = level.capitalize()
            break
    # Log to CSV
    log_path = os.path.join(os.path.dirname(__file__), "detection_log.csv")
    with open(log_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            input_type,
            len(classes),
            ";".join(classes),
            ";".join(confidences),
            feedback,
            threat_level,
            output_path
        ])
    # Send email alert for ANY threat level
    try:
        from email_alert import send_alert_email
        subject = f"⚠️ THREAT DETECTED: {threat_level.upper()}"
        body = f"Gemini Feedback: {feedback}\nThreat Level: {threat_level}\nOutput File: {output_path}"
        send_alert_email(subject, body, "aaronsonnie@gmail.com")
    except Exception as e:
        print(f"[Email Alert Error] {e}")
    return threat_level

# -----------------------------------
# Drawing function (newly added)
# -----------------------------------

def draw_detection(overlay, frame):
    # Draw label ONCE in top left with tank name and accuracy
    if len(frame.boxes) > 0:
        box = frame.boxes[0]
        class_id = int(box.cls[0])
        class_name = frame.names[class_id]
        conf = float(box.conf[0])
        label = f"{class_name.upper()} {conf:.2f}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.0
        thickness = 3
        text_color = (0, 0, 0)  # Black
        bg_color = (230, 216, 173)  # #ADD8E6
        (text_width, text_height), baseline = cv2.getTextSize(label, font, font_scale, thickness)
        # Draw background rectangle in top left
        cv2.rectangle(
            overlay,
            (15, 15),
            (15 + text_width + 20, 15 + text_height + 20),
            bg_color,
            -1
        )
        # Soft shadow/outline effect
        shadow_color = (180, 180, 180)
        for dx, dy in [(-2, -2), (2, 2), (2, -2), (-2, 2)]:
            cv2.putText(
                overlay,
                label,
                (25 + dx, 15 + text_height + dy),
                font,
                font_scale,
                shadow_color,
                thickness + 2,
                cv2.LINE_AA
            )
        # Draw main text
        cv2.putText(
            overlay,
            label,
            (25, 15 + text_height),
            font,
            font_scale,
            text_color,
            thickness,
            cv2.LINE_AA
        )
    # Draw bounding boxes for all detections
    box_color = (235, 206, 135)  # BGR for #87CEEB
    for box in frame.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cv2.rectangle(overlay, (x1, y1), (x2, y2), box_color, 4)

# -----------------------------------
# Main Logic: Image or Video
# -----------------------------------

outputs_dir = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(outputs_dir, exist_ok=True)

if os.path.splitext(INPUT_PATH)[1].lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
    image = cv2.imread(INPUT_PATH)
    if image is not None:
        results = yolo_model(image)
        base_name = os.path.splitext(os.path.basename(INPUT_PATH))[0]
        output_path = os.path.join(outputs_dir, f"{base_name}_annotated.jpg")
        threat_level = get_gemini_feedback(results, output_path, "image")
        frame = results[0]
        overlay = image.copy()
        plotted = frame.plot()
        cv2.imwrite(output_path, plotted)
        cv2.imshow("YOLO Detection", plotted)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("❌ Error: Unable to load image.")
else:
    cap = cv2.VideoCapture(INPUT_PATH)
    if not cap.isOpened():
        print("❌ Error: Unable to open video.")
    else:
        frame_idx = 0
        while cap.isOpened():
            success, frame = cap.read()
            if success:
                results = yolo_model(frame)
                output_path = os.path.join(outputs_dir, f"frame_{frame_idx:05d}_annotated.jpg")
                threat_level = get_gemini_feedback(results, output_path, "video")
                frame0 = results[0]
                overlay = frame.copy()
                plotted = frame0.plot()
                resized = cv2.resize(plotted, (plotted.shape[1]//2, plotted.shape[0]//2), interpolation=cv2.INTER_AREA)
                cv2.imwrite(output_path, resized)
                cv2.imshow("YOLO Detection", resized)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                frame_idx += 1
            else:
                break
        cap.release()
        cv2.destroyAllWindows()
