import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Face Attendance Dashboard", layout="wide")

st.title("🎓 Face Recognition Attendance Dashboard")

conn = sqlite3.connect('attendance.db')
c = conn.cursor()

try:
    df = pd.read_sql_query("SELECT * FROM attendance", conn)
except Exception as e:
    st.error(f"Error reading database: {e}")
    df = pd.DataFrame()

if df.empty:
    st.warning("⚠️ No attendance records found yet. Run test.py to mark attendance first.")
else:
    with st.sidebar:
        st.header("🔍 Filters")
        unique_dates = sorted(df['date'].unique())
        selected_date = st.selectbox("Select Date", options=["All"] + unique_dates)

        unique_names = sorted(df['name'].unique())
        selected_name = st.selectbox("Select Name", options=["All"] + unique_names)

    filtered_df = df.copy()
    if selected_date != "All":
        filtered_df = filtered_df[filtered_df['date'] == selected_date]
    if selected_name != "All":
        filtered_df = filtered_df[filtered_df['name'] == selected_name]

    st.subheader("📋 Attendance Records")
    st.dataframe(filtered_df, use_container_width=True)

    st.subheader("📊 Summary Stats")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", len(df))
    col2.metric("Unique People", df['name'].nunique())
    col3.metric("Filtered Records", len(filtered_df))

    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv,
        file_name='filtered_attendance.csv',
        mime='text/csv',
    )

conn.close()
