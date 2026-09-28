Personal Expense Tracker

Show Image Show Image Show Image

A simple, interactive expense management web app built with Python, Streamlit, SQLite, and Pandas. Add, edit, filter, chart, and export personal expenses, all through a browser-based UI, with no separate database setup required.

Table of Contents
Features
Tech Stack
Project Structure
How to Run
Database
What I Learned
Limitations
Future Improvements
Author
Features

Manage expenses

➕ Add new expenses
📋 View expense history
✏️ Edit existing expenses
🗑️ Delete expenses

Analyze spending

📊 View total expenses
🔢 View number of expenses
💰 Calculate average expense
📊 Category-wise spending chart
📈 Monthly spending chart

Filter and export

🏷️ Filter expenses by category
📅 Filter expenses by date range
⬇️ Export filtered expenses to CSV

Storage

💾 All data persisted locally in a SQLite database (no external database server needed)
Tech Stack
Layer	Tool
UI	Streamlit
Data handling	Pandas
Charts	Matplotlib
Storage	SQLite
Language	Python
Project Structure
text
personal-expense-tracker/
├── app.py            # Streamlit UI: add/edit/delete expenses, filters, charts, CSV export
├── database.py        # SQLite connection and queries (create, read, update, delete)
├── requirements.txt   # Python dependencies
├── .gitignore
└── README.md
How to Run
1. Clone the repository
bash
git clone https://github.com/Umesh-Vishwakarma-web/personal-expense-tracker.git
cd personal-expense-tracker
2. (Recommended) Create a virtual environment
bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
3. Install dependencies
bash
pip install -r requirements.txt
4. Run the app
bash
streamlit run app.py

Streamlit will open the app in your browser automatically (usually at http://localhost:8501). The SQLite database file is created automatically on first run, so no manual database setup is needed.

Database

Expenses are stored locally in a SQLite database file, managed through database.py. Each expense record is expected to include at least: date, category, amount, and description/note.

If your schema has additional or different fields, update this section with the exact column names from database.py so the README matches the code.

What I Learned
Building a full CRUD (create, read, update, delete) flow with Streamlit as the front end and SQLite as the backend.
Structuring a small app into separate UI (app.py) and data-access (database.py) layers instead of one file.
Using Pandas to filter and summarize data (totals, averages, category and monthly breakdowns) for display.
Generating charts from live data with Matplotlib inside a Streamlit app.
Exporting filtered results back out to CSV for the user.
Limitations
Built as a personal learning project, not hardened for multi-user or production use.
No authentication — anyone with access to the app can view and edit all data.
Data is stored in a local SQLite file, so it isn't backed up or synced anywhere by default.
No input validation details are documented yet (e.g. handling of duplicate entries, currency formatting, or invalid dates).
Future Improvements
Add user authentication for multi-user use
Add input validation and error handling for edge cases
Support multiple currencies
Add recurring expense tracking
Deploy a live demo (e.g. Streamlit Community Cloud) and link it here
Add automated tests for database.py
Author

Umesh Vishwakarma GitHub: Umesh-Vishwakarma-web