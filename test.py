import cv2
import face_recognition
import pickle
import numpy as np
import os
import sqlite3
import time
from datetime import datetime
from win32com.client import Dispatch
import pythoncom

def speak(text):
    pythoncom.CoInitialize()
    speaker = Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

# Load known encodings
with open('data/encodings.pkl', 'rb') as f:
    known_encodings, known_names = pickle.load(f)

# Initialize webcam
video = cv2.VideoCapture(0)

# SQLite DB
conn = sqlite3.connect('attendance.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        UNIQUE(name, date)
    )
''')
conn.commit()

attendance_marked = False
face_detected = False
start_time = time.time()

while True:
    ret, frame = video.read()
    if not ret:
        continue

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    if len(face_locations) > 0:
        face_detected = True

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_names[best_match_index]

            print(f"Encoding for {name}:")
            print(face_encoding)

            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, top - 40), (right, top), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (left + 5, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            ts = datetime.now()
            date = ts.strftime("%d-%m-%Y")
            time_str = ts.strftime("%H:%M:%S")

            try:
                c.execute('INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)',
                          (name, date, time_str))
                conn.commit()
                speak(f"Attendance recorded for {name}")
                attendance_marked = True
            except sqlite3.IntegrityError:
                speak(f"Attendance already marked for  {name} for today")
                attendance_marked = True

    cv2.imshow("Face Recognition Attendance", frame)

    if attendance_marked or (time.time() - start_time > 30):
        break

    if cv2.waitKey(1) == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
conn.close()

if not face_detected:
    speak("No face detected.")
