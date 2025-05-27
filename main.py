import face_recognition
import cv2
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import numpy as np

known_face_encodings = []
known_face_names = []
video_capture = None
is_running = False
last_alert_time = None

# Ensure known_faces directory exists
os.makedirs("known_faces", exist_ok=True)

def load_known_faces():
    known_face_encodings.clear()
    known_face_names.clear()
    for filename in os.listdir('known_faces'):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image = face_recognition.load_image_file(f'known_faces/{filename}')
            encoding = face_recognition.face_encodings(image)
            if encoding:
                known_face_encodings.append(encoding[0])
                known_face_names.append(os.path.splitext(filename)[0])

def send_alert():
    global last_alert_time
    now = datetime.now()
    if last_alert_time and (now - last_alert_time).total_seconds() < 60:
        return  # Avoid sending multiple alerts in short time
    last_alert_time = now

    sender_email = "pernelaxman@gmail.com"
    receiver_email = "laxmanperne123@gmail.com"
    password = os.getenv("EMAIL_APP_PASSWORD")  # Use environment variable

    if not password:
        print("Error: EMAIL_APP_PASSWORD not set in environment.")
        return

    msg = MIMEText("Alert: Unknown person tried to enter the house!")
    msg['Subject'] = 'Home Entry Alert'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.send_message(msg)
            print("Alert sent!")
    except Exception as e:
        print("Failed to send alert:", e)

    with open("alert_log.txt", "a") as log:
        log.write(f"[{now}] Unknown person detected. Alert sent.\n")

def add_known_face():
    filepath = filedialog.askopenfilename()
    if filepath:
        filename = os.path.basename(filepath)
        save_path = os.path.join("known_faces", filename)
        with open(filepath, 'rb') as src, open(save_path, 'wb') as dst:
            dst.write(src.read())
        load_known_faces()
        messagebox.showinfo("Face Added", f"{filename} added to known faces.")

def recognize_faces():
    global is_running, video_capture
    is_running = True
    load_known_faces()
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        update_status("Error: Camera not accessible")
        return

    while is_running:
        ret, frame = video_capture.read()
        if not ret:
            update_status("Failed to read from camera")
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, locations)

        status = "No face detected"
        for encoding in encodings:
            matches = face_recognition.compare_faces(known_face_encodings, encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, encoding)
            if face_distances.size > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index] and face_distances[best_match_index] < 0.5:
                    name = known_face_names[best_match_index]
                    status = f"Welcome {name}, Door Unlocked"
                else:
                    status = "Unknown person, Door Locked"
                    send_alert()
            else:
                status = "Unknown person, Door Locked"
                send_alert()

            with open("access_log.txt", "a") as log:
                log.write(f"[{datetime.now()}] Detected: {name}\n")

        update_status(status)

    if video_capture:
        video_capture.release()

def start_camera():
    threading.Thread(target=recognize_faces).start()

def stop_camera():
    global is_running
    is_running = False
    if video_capture:
        video_capture.release()
    update_status("Camera stopped")

def update_status(msg):
    status_label.config(text=msg)

# GUI
app = tk.Tk()
app.title("Smart Identity Detection")
app.geometry("400x250")

status_label = tk.Label(app, text="Status: Idle", font=("Arial", 14))
status_label.pack(pady=20)

tk.Button(app, text="Start Camera", command=start_camera, width=20).pack(pady=5)
tk.Button(app, text="Stop Camera", command=stop_camera, width=20).pack(pady=5)
tk.Button(app, text="Add Known Face", command=add_known_face, width=20).pack(pady=20)

app.protocol("WM_DELETE_WINDOW", lambda: (stop_camera(), app.destroy()))
app.mainloop()
