import sqlite3

DATABASE = "expenses.db"


def connect():
    return sqlite3.connect(DATABASE)


def create_database():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_expense(date, description, amount, category):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses (date, description, amount, category)
        VALUES (?, ?, ?, ?)
    """, (date, description, amount, category))

    connection.commit()
    connection.close()


def get_expenses():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, date, description, amount, category
        FROM expenses
        ORDER BY date DESC
    """)

    expenses = cursor.fetchall()
    connection.close()

    return expenses


def get_summary():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)

    summary = cursor.fetchall()
    connection.close()

    return summary
