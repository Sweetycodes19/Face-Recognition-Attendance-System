## **📸 Face-Recognition-Attendance-System**

  🚀 An AI-powered facial recognition attendance system

## Screenshots
![image alt](https://github.com/Sweetycodes19/Face-Recognition-Attendance-System/blob/main/Images/Screenshot%202025-07-19%20232001.png)
![image alt](https://github.com/Sweetycodes19/Face-Recognition-Attendance-System/blob/main/Images/Screenshot%202025-07-19%20232044.png)



## 📜 About the Project
This project automates the process of taking attendance using a webcam and real-time face recognition. It detects and recognizes faces, records attendance with a timestamp, stores it in a database, and displays the records in a modern Streamlit dashboard with filters and export options.This is ideal for classrooms, offices, or any environment where accurate, contactless attendance is required.

## 🎯 Features
- ✅ **Face Registration** 🧑‍💻
- ✅ **Real-Time Face Detection & Recognition** 📷
- ✅ **Database Integration** 🗂️
- ✅ **Secure & Efficient** 🔒
- ✅ **Streamlit Dashboard** 📊
## 🛠️ Technologies Used
- **Language:** Python 🐍  
- **Libraries:** OpenCV, NumPy, Pandas, PyWin32, Streamlit  
- **Machine Learning:** `face_recognition` library (uses Dlib + CNN for embeddings)  
- **Database:** SQLite  
- **GUI:** OpenCV’s window + Streamlit (web app)
## Installation

1️⃣ **Clone the repository:**

```bash
  https://github.com/Sweetycodes19/Face-Recognition-Attendance-System.git
```
2️⃣ **Navigate to the project directory:**

```bash
cd Face-Recognition-Attendance-System
```
3️⃣ **Install dependencies:**

```bash 
pip install -r requirements.txt
```
    
## 🖥️ How It Works
- **1️⃣ Register Faces** — Store authorized user images in the database.
- **2️⃣ Mark Attendance** — The system matches faces with registered users.
- **3️⃣ Log Data** — Attendance is saved with name, date, and timestamp.
- **4️⃣View Dashboard** — Run app.py with Streamlit to view attendance records.
## 📌 Future Enhancements
- ✅ Add face liveness detection to prevent spoofing.
- ✅ Add admin authentication for managing records.
- ✅ Add photo snapshots with each record.
- ✅ Integrate with cloud storage or Firebase for multi-device syncing.
- ✅ Add email notifications for attendance logs.
- ✅ Deploy Streamlit dashboard online for remote access.
## License

[MIT](https://choosealicense.com/licenses/mit/)

