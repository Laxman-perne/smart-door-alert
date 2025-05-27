# Smart Identity Detection System

## Description
The Smart Identity Detection System is a real-time facial recognition application designed to secure home entry by identifying known individuals and alerting users if an unknown person is detected. The system automatically locks the door and sends email alerts, enhancing safety for families and children.

---

## Features
- Real-time face recognition via webcam.
- Add known faces dynamically using a GUI.
- Alerts via email when unknown persons are detected (rate-limited).
- Logs all recognized faces and alert events with timestamps.
- User-friendly interface built with Tkinter.
- Avoids multiple alert emails within short periods.

---

## Technologies Used
- Python 3.x
- face_recognition for face detection and encoding
- OpenCV for video capture and processing
- Tkinter for the graphical user interface
- smtplib for sending alert emails
- NumPy for numeric operations

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/smart-identity-detection.git
   cd smart-identity-detection
   ```

2. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set your email password in environment variables:
   ```bash
   export EMAIL_APP_PASSWORD='your_email_app_password'
   ```
   Windows CMD:
   ```cmd
   set EMAIL_APP_PASSWORD=your_email_app_password
   ```

5. Create a folder named `known_faces` in your project directory and add images of authorized people there.

---

## Usage

1. Run the program:
   ```bash
   python your_script_name.py
   ```

2. Use the GUI buttons:
   - **Start Camera**: Start live face recognition.
   - **Stop Camera**: Stop recognition and video capture.
   - **Add Known Face**: Add a new face image to known faces.

3. If an unknown face is detected:
   - The system locks the door (logic to be integrated).
   - Sends an alert email (no more than one alert per minute).
   - Logs the event in `alert_log.txt`.

4. All detected faces are logged in `access_log.txt` with timestamps.

---

## Security Notes
- Use environment variables for sensitive data like email passwords.
- Make sure to use Gmail app passwords or other secure methods for SMTP authentication.
- Hardware integration for actual door locking is required separately.

---

## Contributing
Feel free to fork, report issues, or submit pull requests!

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact
For questions or feedback, contact: [pernelaxman@gmaail.com]
