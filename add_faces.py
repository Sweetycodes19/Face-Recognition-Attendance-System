import cv2
import face_recognition
import pickle
import os
import pythoncom
from win32com.client import Dispatch

def speak(text):
    pythoncom.CoInitialize()
    speaker = Dispatch("SAPI.SpVoice")
    speaker.Speak(text)


video = cv2.VideoCapture(0)

name = input("Enter Your Name: ")
speak(f"Hello {name}, please look at the camera.")

encodings = []

while True:
    ret, frame = video.read()
    if not ret:
        continue

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = face_recognition.face_locations(rgb_frame)

    for (top, right, bottom, left) in faces:
        face_encoding = face_recognition.face_encodings(rgb_frame, [(top, right, bottom, left)])[0]
        encodings.append(face_encoding)

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, f"Samples: {len(encodings)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Register Face", frame)

    if cv2.waitKey(1) == ord('q') or len(encodings) >= 20:
        break

video.release()
cv2.destroyAllWindows()


if not os.path.exists('data'):
    os.makedirs('data')

if os.path.exists('data/encodings.pkl'):
    with open('data/encodings.pkl', 'rb') as f:
        loaded = pickle.load(f)
        if isinstance(loaded, tuple) and len(loaded) == 2:
            all_encodings, all_names = loaded
        else:
            print("⚠️ Warning: old encodings.pkl is invalid. Resetting.")
            all_encodings, all_names = [], []
else:
    all_encodings, all_names = [], []

all_encodings.extend(encodings)
all_names.extend([name] * len(encodings))

with open('data/encodings.pkl', 'wb') as f:
    pickle.dump((all_encodings, all_names), f)

#speak(f"Saved {len(encodings)} samples for {name}")
print(f"✅ Saved {len(encodings)} encodings for {name}")
