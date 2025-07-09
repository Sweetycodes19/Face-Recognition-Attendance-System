# 🎓 Face-Recognition-Attendance-System

📜 About the Project

This project automates the process of taking attendance using a webcam and real-time face recognition.  It detects and recognizes faces, records attendance with a timestamp, stores it in a database, and displays the records in a modern Streamlit dashboard with filters and export options.This is ideal for classrooms, offices, or any environment where accurate, contactless attendance is required.

🎯 Features

📸 Face Registration 
🧑‍💻 Real-time face detection & recognition 
🗂️ Database integration for attendance logging
🔒 Secure & efficient attendance tracking
📊 Streamlit Dashboard
🔊 Text-to-Speech

🛠️ Technologies Used

Language: Python 🐍
Libraries: OpenCV, NumPy, Pandas , Pywin32 ,Streamlit
Machine Learning: Face Recognition (Dlib), Deep Learning (CNN)
Database: MySQL / SQLite
GUI:Streamlit (web app) ,OpenCV’s window

📂 Installation & Setup

1️⃣ Clone the repository:
https://github.com/Sweetycodes19/Face-Recognition-Attendance-System.git

2️⃣ Navigate to the project directory:
cd face-recognition-attendance

3️⃣Install dependencies:
pip install -r requirements.txt

🖥️ How It Works

1️⃣ Register Faces: Store authorized user images in the database.
2️⃣ Capture Attendance: The system matches faces with registered users.
3️⃣ Log Data: Attendance is saved with timestamps.
4️⃣ View Attendance Dashboard

✨ Future Enhancements

✅ Add face liveness detection to prevent spoofing.
✅ Add admin authentication for managing records.
✅ Add photo snapshots with each record.
✅ Integrate with cloud storage or Firebase for multi-device syncing.
✅ Add email notifications for attendance logs.
✅ Deploy Streamlit dashboard online for remote access.

📂 Folder Structure

📁 data/
  └─ encodings.pkl   # Stores face encodings and names

📄 attendance.db     # SQLite DB with attendance table
📄 add_faces.py      # Register new faces
📄 test.py           # Real-time attendance
📄 app.py            # Streamlit dashboard
📄 requirements.txt  # Python dependencies
📄 README.md         # This file



