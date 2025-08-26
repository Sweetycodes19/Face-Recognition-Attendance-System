import streamlit as st
import cv2
import os
import numpy as np
import pickle
import face_recognition
from datetime import datetime
from database import mark_attendance
from speaker import speak
from config import ENCODINGS_PATH, SAMPLES_REQUIRED
from collections import Counter

def is_face_already_registered(new_encoding, known_encodings, threshold=0.45):
    results = face_recognition.compare_faces(known_encodings, new_encoding, tolerance=threshold)
    return any(results)

def register_face():
    st.subheader("➕ Register New Face")
    name = st.text_input("Enter your name:")
    capture_btn = st.button("📷 Capture & Register")

    if capture_btn and name:
        if os.path.exists(ENCODINGS_PATH):
            with open(ENCODINGS_PATH, "rb") as f:
                known_encodings, known_names = pickle.load(f)
                if name in known_names:
                    st.warning(f"⚠️ The name '{name}' is already registered.")
                    speak(f"{name} is already registered. Please use a different name.")
                    return
        else:
            known_encodings, known_names = [], []

        speak(f"Hello {name}, We’ll capture 15 face samples. Please face the camera and stay still until it’s done.")
        video = cv2.VideoCapture(0)
        stframe = st.empty()

        while True:
            ret, frame = video.read()
            if not ret:
                continue
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            if face_locations:
                encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
                if is_face_already_registered(encoding, known_encodings):
                    speak("This face is already registered with another name.")
                    st.error("❌ This face already exists in the system.")
                    video.release()
                    return
                else:
                    break
            stframe.image(frame, channels="BGR", caption="Detecting face...")

        encodings = []
        progress = st.progress(0)

        while len(encodings) < SAMPLES_REQUIRED:
            ret, frame = video.read()
            if not ret:
                continue
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            for (top, right, bottom, left) in face_locations:
                face_encoding = face_recognition.face_encodings(rgb_frame, [(top, right, bottom, left)])[0]
                encodings.append(face_encoding)
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            stframe.image(frame, channels="BGR", caption=f"Samples: {len(encodings)}/{SAMPLES_REQUIRED}")
            progress.progress(len(encodings) / SAMPLES_REQUIRED)

        video.release()
        st.success("✅ Face samples captured.")

        os.makedirs(os.path.dirname(ENCODINGS_PATH), exist_ok=True)

        all_encodings = known_encodings + encodings
        all_names = known_names + [name] * len(encodings)

        with open(ENCODINGS_PATH, "wb") as f:
            pickle.dump((all_encodings, all_names), f)

        # ✅ Admin-specific attendance marking
        admin = st.session_state.get("admin_name", "Unknown")
        mark_attendance(name, admin=admin)
        speak(f"Attendance marked for {name}")
        st.success(f"✅ Attendance marked for {name}")

    elif capture_btn and not name:
        st.error("⚠️ Please enter your name.")

def recognize_faces():
    st.subheader("🎥 Recognize Face & Mark Attendance")
    run_recognition = st.button("▶️ Start Recognition")
    tolerance = st.slider("Face Match Tolerance", 0.3, 0.6, 0.45, 0.01)
    vote_threshold = st.slider("Min Matches to Accept Identity", 3, 15, 5)

    if run_recognition:
        try:
            with open(ENCODINGS_PATH, "rb") as f:
                known_encodings, known_names = pickle.load(f)
        except:
            st.error("❌ No face data found. Please register faces first.")
            return

        video = cv2.VideoCapture(0)
        stframe = st.empty()
        attendance_set = set()
        start_time = datetime.now().timestamp()

        while True:
            ret, frame = video.read()
            if not ret:
                continue

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=tolerance)
                name_votes = [known_names[i] for i, match in enumerate(matches) if match]

                final_name = "Unknown"
                if name_votes:
                    vote_count = Counter(name_votes)
                    most_common_name, count = vote_count.most_common(1)[0]
                    if count >= vote_threshold:
                        final_name = most_common_name

                if final_name != "Unknown":
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, final_name, (left + 6, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

                    if final_name not in attendance_set:
                        # ✅ Admin-specific attendance marking
                        admin = st.session_state.get("admin_name", "Unknown")
                        mark_attendance(final_name, admin=admin)
                        speak(f"Attendance recorded for {final_name}")
                        attendance_set.add(final_name)

            stframe.image(frame, channels="BGR", caption="Face Recognition Running...", use_column_width=True)

            if datetime.now().timestamp() - start_time > 15 or len(attendance_set) > 0:
                break

        video.release()
        if len(attendance_set) == 0:
            speak("No face detected.")
        else:
            st.success("✅ Attendance process complete.")
