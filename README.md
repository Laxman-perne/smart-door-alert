Smart Door Alert System

A Python-based face recognition system to protect children at home by preventing entry of unknown people and alerting parents.

Features

Real-time face recognition using webcam

Email alert to parents when unknown faces are detected

GUI built with Tkinter for ease of use

Option to add known faces via GUI

Status display for door lock/unlock


Requirements

Python 3.7+

OpenCV

face_recognition

Pillow


Installation

pip install face_recognition opencv-python Pillow

Setup

1. Create a folder named known_faces/ in your project root

Add images of family members (e.g., dad.jpg, mom.png)



2. Enable 2-Step Verification on your Gmail account

Visit https://myaccount.google.com/security



3. Generate an App Password

Visit https://myaccount.google.com/apppasswords

Use that 16-character password in your script under send_alert()




Running the Project

python main.py

How It Works

Starts webcam when "Start Camera" is clicked

Compares detected face with known faces

If unknown, it sends an email alert and locks the virtual door
