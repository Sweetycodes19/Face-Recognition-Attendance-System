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
- **1️⃣ Admin Login/Register** — Secure access via password-protected admin panel. Only registered admins can proceed.
- **2️⃣ Register Faces** — Store authorized user images in the database.
- **3️⃣ Mark Attendance** — The system matches faces with registered users.
- **4️⃣ Log Data** — Records are saved with name, time, date, and the admin who logged them.
- **5️⃣ View Dashboard** — Admin can filter, view, and download attendance logs directly through the Streamlit dashboard.


## 📌 Future Enhancements
- ☁️ Cloud sync with Firebase
- 👤 Face login for admins
- 📧 Email/SMS attendance alerts
- 📊 Attendance analytics and charts
- 🔔 Real-time notifications and logs
- 🧠 AI-based spoof detection for better security


## License

[MIT](https://choosealicense.com/licenses/mit/)

