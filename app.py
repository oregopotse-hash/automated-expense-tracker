import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(
    page_title="AI Automation Portfolio",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Database setup
# -----------------------------

DB_NAME = "automation.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS automation_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_task(task):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO automation_tasks (task, status, created_at)
        VALUES (?, ?, ?)
        """,
        (task, "Pending", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    conn.commit()
    conn.close()


def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, task, status, created_at
        FROM automation_tasks
        ORDER BY id DESC
    """)

    tasks = cursor.fetchall()
    conn.close()

    return tasks


def update_task(task_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE automation_tasks
        SET status = ?
        WHERE id = ?
        """,
        (status, task_id)
    )

    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM automation_tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()


# Create database table
create_table()


# -----------------------------
# Application interface
# -----------------------------

st.title("🤖 AI Automation Portfolio")

st.write(
    "A simple Streamlit web application for managing automation tasks."
)

st.divider()

# Add task
st.subheader("➕ Add Automation Task")

with st.form("task_form"):
    task = st.text_input(
        "Task description",
        placeholder="Example: Send automated weekly report"
    )

    submitted = st.form_submit_button("Add Task")

    if submitted:
        if task.strip():
            add_task(task.strip())
            st.success("Task added successfully.")
            st.rerun()
        else:
            st.warning("Please enter a task.")


st.divider()

# Dashboard
st.subheader("📊 Automation Dashboard")

tasks = get_tasks()

total_tasks = len(tasks)
completed_tasks = len(
    [task for task in tasks if task[2] == "Completed"]
)
pending_tasks = total_tasks - completed_tasks

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Tasks", total_tasks)

with col2:
    st.metric("Completed", completed_tasks)

with col3:
    st.metric("Pending", pending_tasks)


st.divider()

# Task list
st.subheader("📋 Automation Tasks")

if not tasks:
    st.info("No automation tasks have been added yet.")
else:
    for task_id, task_name, status, created_at in tasks:

        with st.container(border=True):
            col1, col2, col3 = st.columns([5, 2, 1])

            with col1:
                st.write(f"**{task_name}**")
                st.caption(f"Created: {created_at}")

            with col2:
                new_status = st.selectbox(
                    "Status",
                    ["Pending", "Completed"],
                    index=0 if status == "Pending" else 1,
                    key=f"status_{task_id}"
                )

                if new_status != status:
                    update_task(task_id, new_status)
                    st.rerun()

            with col3:
                if st.button(
                    "Delete",
                    key=f"delete_{task_id}"
                ):
                    delete_task(task_id)
                    st.rerun()


st.divider()

st.caption(
    "Built with Python, SQLite and Streamlit."
)
