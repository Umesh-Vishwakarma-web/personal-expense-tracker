import sqlite3


DATABASE_NAME = "expenses.db"


# --------------------------------------------------
# Database Connection
# --------------------------------------------------

def create_connection():
    return sqlite3.connect(DATABASE_NAME)


# --------------------------------------------------
# Create Expenses Table
# --------------------------------------------------

def create_table():

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# --------------------------------------------------
# Add Expense
# --------------------------------------------------

def add_expense(date, category, description, amount):

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (date, category, description, amount)
        VALUES (?, ?, ?, ?)
    """, (
        date,
        category,
        description,
        amount
    ))

    connection.commit()
    connection.close()


# --------------------------------------------------
# Get All Expenses
# --------------------------------------------------

def get_expenses():

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            date,
            category,
            description,
            amount
        FROM expenses
        ORDER BY date DESC, id DESC
    """)

    expenses = cursor.fetchall()

    connection.close()

    return expenses


# --------------------------------------------------
# Get Category-wise Expenses
# --------------------------------------------------

def get_category_expenses():

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            category,
            SUM(amount)
        FROM expenses
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)

    category_expenses = cursor.fetchall()

    connection.close()

    return category_expenses


# --------------------------------------------------
# Get Monthly Expenses
# --------------------------------------------------

def get_monthly_expenses():

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            SUBSTR(date, 1, 7) AS month,
            SUM(amount)
        FROM expenses
        GROUP BY month
        ORDER BY month
    """)

    monthly_expenses = cursor.fetchall()

    connection.close()

    return monthly_expenses


# --------------------------------------------------
# Delete Expense
# --------------------------------------------------

def delete_expense(expense_id):

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE id = ?
    """, (expense_id,))

    connection.commit()
    connection.close()


# --------------------------------------------------
# Update Expense
# --------------------------------------------------

def update_expense(
    expense_id,
    date,
    category,
    description,
    amount
):

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE expenses
        SET
            date = ?,
            category = ?,
            description = ?,
            amount = ?
        WHERE id = ?
    """, (
        date,
        category,
        description,
        amount,
        expense_id
    ))

    connection.commit()
    connection.close()


# --------------------------------------------------
# Get Expense by ID
# --------------------------------------------------

def get_expense_by_id(expense_id):

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            date,
            category,
            description,
            amount
        FROM expenses
        WHERE id = ?
    """, (expense_id,))

    expense = cursor.fetchone()

    connection.close()

    return expense


# --------------------------------------------------
# Initialize Database
# --------------------------------------------------

create_table()