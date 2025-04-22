# main.py

import face_recognition
import cv2
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
import threading

known_face_encodings = []
known_face_names = []
video_capture = None
is_running = False

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
    sender_email = "pernelaxman@gmail.com"
    receiver_email = "laxmanperne123@gmail.com"
    password = "mdcc rtwj qouw gnng"

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
        log.write(f"[{datetime.now()}] Unknown person detected. Alert sent.\n")

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
    global is_running
    is_running = True
    load_known_faces()
    global video_capture
    video_capture = cv2.VideoCapture(0)

    while is_running:
        ret, frame = video_capture.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, locations)

        status = "No face detected"
        for encoding in encodings:
            matches = face_recognition.compare_faces(known_face_encodings, encoding)
            name = "Unknown"
            if True in matches:
                index = matches.index(True)
                name = known_face_names[index]
                status = f"Welcome {name}, Door Unlocked"
            else:
                status = "Unknown person, Door Locked"
                send_alert()

        update_status(status)

    video_capture.release()

def start_camera():
    threading.Thread(target=recognize_faces).start()

def stop_camera():
    global is_running
    is_running = False
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