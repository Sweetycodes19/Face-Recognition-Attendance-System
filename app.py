import streamlit as st
st.set_page_config(page_title="Face Recognition Attendance", layout="wide")

import json
import hashlib
import os
import time
import sqlite3
from face_utils import register_face, recognize_faces
from database import get_attendance_df
from speaker import speak

ADMIN_FILE = "admin.json"
SESSION_TIMEOUT_MINUTES = 5

# --- Utility Functions ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_admins():
    if os.path.exists(ADMIN_FILE):
        with open(ADMIN_FILE, "r") as f:
            return json.load(f)
    return []

def save_admins(admins):
    with open(ADMIN_FILE, "w") as f:
        json.dump(admins, f)

def admin_exists(name):
    return any(admin["name"] == name for admin in load_admins())

def verify_admin(name, password):
    for admin in load_admins():
        if admin["name"] == name and admin["password"] == hash_password(password):
            return True
    return False

# --- Ensure DB has admin column ---
def ensure_admin_column():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(attendance)")
    columns = [col[1] for col in cursor.fetchall()]
    if "admin" not in columns:
        cursor.execute("ALTER TABLE attendance ADD COLUMN admin TEXT")
        conn.commit()
    conn.close()

ensure_admin_column()

# --- Change Password ---
def change_admin_password_inline():
    st.subheader("🔐 Change Admin Password")
    admin_name = st.text_input("Admin Name", key="change_admin_name")
    current_pass = st.text_input("Current Password", type="password", key="change_current_pass")
    new_pass = st.text_input("New Password", type="password", key="change_new_pass")
    confirm_pass = st.text_input("Confirm New Password", type="password", key="change_confirm_pass")
    if st.button("Update Password"):
        admins = load_admins()
        for admin in admins:
            if admin["name"] == admin_name and admin["password"] == hash_password(current_pass):
                if new_pass == confirm_pass:
                    admin["password"] = hash_password(new_pass)
                    save_admins(admins)
                    st.success("✅ Password updated")
                    speak("Password updated successfully")
                    return
                else:
                    st.error("❌ New passwords do not match")
                    speak("New passwords do not match")
                    return
        st.error("❌ Invalid credentials")
        speak("Invalid credentials")

# --- Reset Admins ---
def reset_admins_inline():
    st.subheader("🧨 Reset Admin & Records")

    reset_name = st.text_input("Enter Admin Name ", key="reset_name")
    reset_pass = st.text_input("Enter Admin Password", type="password", key="reset_pass")

    if st.button("Confirm Remove Admin"):
        admins = load_admins()
        if not admins:
            st.error("⚠️ No admins registered yet.")
            return

        # Verify name + password
        valid = False
        for admin in admins:
            if admin["name"] == reset_name and admin["password"] == hash_password(reset_pass):
                valid = True
                admins.remove(admin)
                break

        if valid:
            # Save updated admins list (without the removed one)
            save_admins(admins)

            # Remove attendance records for that admin
            conn = sqlite3.connect("attendance.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM attendance WHERE admin=?", (reset_name,))
            conn.commit()
            conn.close()

            st.success(f"✅ Admin '{reset_name}' and all their records removed.")
            speak(f"Admin {reset_name} removed successfully")
            st.stop()
        else:
            st.error("❌ Invalid admin name or password. Removal denied.")
            speak("Invalid admin name or password")


# -- Session Setup -
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "admin_name" not in st.session_state:
    st.session_state.admin_name = ""
if "show_login" not in st.session_state:
    st.session_state.show_login = False
if "last_active" not in st.session_state:
    st.session_state.last_active = time.time()
if "date_filter" not in st.session_state:
    st.session_state.date_filter = "All"
if "name_filter" not in st.session_state:
    st.session_state.name_filter = "All"

# --- Auto Logout ---
if st.session_state.logged_in:
    if time.time() - st.session_state.last_active > SESSION_TIMEOUT_MINUTES * 60:
        st.warning("⏳ Session expired")
        speak("Session expired")
        st.session_state.logged_in = False
        st.session_state.admin_name = ""
        st.session_state.show_login = False
        st.stop()
    else:
        st.session_state.last_active = time.time()

admins = load_admins()

# --- Admin Registration/Login Flow ---
if not st.session_state.logged_in:
    st.title("🔐 Admin Registration Panel")
    admin_name = st.text_input("Admin Name")
    admin_pass = st.text_input("Admin Password", type="password")

    if not st.session_state.show_login:
        col1, col2 = st.columns(2)
        with col1:
            register_clicked = st.button("🟠 Register Admin")
        with col2:
            login_clicked = st.button("🔓 Already Registered? Login Here")

        if register_clicked:
            if admin_name and admin_pass:
                if admin_exists(admin_name):
                    st.error("❗ Admin already exists")
                else:
                    admins.append({"name": admin_name, "password": hash_password(admin_pass)})
                    save_admins(admins)
                    st.success("✅ Admin registered and logged in")
                    speak("Admin registration successful")
                    st.session_state.logged_in = True
                    st.session_state.admin_name = admin_name
                    st.session_state.last_active = time.time()
            else:
                st.error("❗ Please fill in both fields")
            st.stop()

        if login_clicked:
            st.session_state.show_login = True

        st.stop()

    st.subheader("👤 Admin Login Panel")
    login_name = st.text_input("Admin Name (Login)", key="login_name")
    login_pass = st.text_input("Admin Password (Login)", type="password", key="login_pass")

    if st.button("Login"):
        if verify_admin(login_name, login_pass):
            st.session_state.logged_in = True
            st.session_state.admin_name = login_name
            st.session_state.last_active = time.time()
            st.success("✅ Login successful")
            speak("Login successful")
        else:
            st.error("❌ Invalid credentials")
            speak("Login failed")

    with st.expander("🔐 Change Admin Password"):
        change_admin_password_inline()
        reset_admins_inline()
    st.stop()

# --- MAIN DASHBOARD ---
st.title("📚 Face Recognition Attendance Dashboard")

with st.sidebar:
    st.header("🧭 Navigation")
    page = st.radio("Go to", ["Dashboard", "Register New Face", "Recognize Face"])
    st.markdown(f"**Logged in as:** `{st.session_state.admin_name}`")

    if page == "Dashboard":
        # ✅ Create df first
        df = get_attendance_df()

        if "admin" in df.columns:
            df = df[df["admin"] == st.session_state.admin_name]

        if not df.empty:
            unique_names = sorted(df["name"].unique()) if "name" in df.columns else []

            # 📅 Calendar input
            date_choice = st.date_input("📅 Select Date", value=None)
            if date_choice:
                st.session_state.date_filter = str(date_choice)
            else:
                st.session_state.date_filter = "All"

            st.session_state.name_filter = st.selectbox("🧑 Select Name", ["All"] + unique_names)

        else:
            st.session_state.date_filter = "All"
            st.session_state.name_filter = "All"

        if st.button("🔓 Logout"):
            st.session_state.logged_in = False
            st.session_state.admin_name = ""
            st.session_state.show_login = False
            st.success("✅ Logged out")
            speak("Logged out")
            st.experimental_rerun()

# --- PAGE CONTENT ---
if page == "Dashboard":
    df = get_attendance_df()
    if "admin" in df.columns:
        df = df[df["admin"] == st.session_state.admin_name]

    if df.empty:
        st.warning("⚠️ No records found.")
    else:
        filtered_df = df.copy()
        if st.session_state.date_filter != "All":
            filtered_df = filtered_df[filtered_df["date"] == st.session_state.date_filter]
        if st.session_state.name_filter != "All":
            filtered_df = filtered_df[filtered_df["name"] == st.session_state.name_filter]

        st.dataframe(filtered_df, use_container_width=True)
        st.download_button("⬇️ Download CSV", filtered_df.to_csv(index=False), "attendance.csv")

        st.subheader("📈 Attendance Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Records", len(df))
        col2.metric("Unique People", df["name"].nunique())
        col3.metric("Filtered Records", len(filtered_df))

elif page == "Register New Face":
    register_face()

elif page == "Recognize Face":
    recognize_faces()
