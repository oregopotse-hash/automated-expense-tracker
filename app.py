import sqlite3
from datetime import datetime

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


def categorise_expense(description):
    description = description.lower()

    categories = {
        "Food": ["food", "restaurant", "takeaway", "groceries", "grocery"],
        "Transport": ["taxi", "uber", "fuel", "petrol", "transport", "bus"],
        "Bills": ["electricity", "water", "internet", "rent", "phone"],
        "Shopping": ["clothes", "shoes", "shopping", "mall"],
        "Entertainment": ["movie", "cinema", "games", "entertainment"]
    }

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in description:
                return category

    return "Other"


def add_expense(description, amount):
    category = categorise_expense(description)
    date = datetime.now().strftime("%Y-%m-%d")

    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses (date, description, amount, category)
        VALUES (?, ?, ?, ?)
    """, (date, description, amount, category))

    connection.commit()
    connection.close()

    print(f"Expense added: {description} - R{amount:.2f} ({category})")


def show_summary():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)

    results = cursor.fetchall()

    print("\nSpending Summary")
    print("----------------")

    total = 0

    for category, amount in results:
        print(f"{category}: R{amount:.2f}")
        total += amount

    print("----------------")
    print(f"Total: R{total:.2f}")

    connection.close()


if __name__ == "__main__":
    create_database()

    add_expense("Groceries", 450)
    add_expense("Petrol", 300)
    add_expense("Internet bill", 699)
    add_expense("New shoes", 800)

    show_summary()
