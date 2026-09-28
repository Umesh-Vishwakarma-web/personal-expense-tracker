import streamlit as st
import pandas as pd

from database import (
    create_table,
    add_expense,
    get_expenses,
    get_category_expenses,
    get_monthly_expenses,
    delete_expense,
    update_expense,
    get_expense_by_id
)


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)


# --------------------------------------------------
# Initialize Database
# --------------------------------------------------

create_table()


# --------------------------------------------------
# Constants
# --------------------------------------------------

CATEGORIES = [
    "Food",
    "Travel",
    "Shopping",
    "Bills",
    "Entertainment",
    "Health",
    "Education",
    "Other"
]


# --------------------------------------------------
# Helper Function
# --------------------------------------------------

def load_expenses():

    expenses = get_expenses()

    columns = [
        "ID",
        "Date",
        "Category",
        "Description",
        "Amount"
    ]

    return pd.DataFrame(expenses, columns=columns)


# --------------------------------------------------
# Application Title
# --------------------------------------------------

st.title("💰 Personal Expense Tracker")

st.write(
    "Track, manage and analyze your daily expenses."
)


# --------------------------------------------------
# Load Data
# --------------------------------------------------

expenses_df = load_expenses()


if not expenses_df.empty:

    expenses_df["Date"] = pd.to_datetime(
        expenses_df["Date"]
    )


# --------------------------------------------------
# Dashboard
# --------------------------------------------------

st.subheader("📊 Dashboard")


if not expenses_df.empty:

    total_expense = expenses_df["Amount"].sum()

    number_of_expenses = len(expenses_df)

    average_expense = (
        total_expense / number_of_expenses
    )

else:

    total_expense = 0

    number_of_expenses = 0

    average_expense = 0


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Total Expenses",
        f"₹{total_expense:,.2f}"
    )


with col2:

    st.metric(
        "Number of Expenses",
        number_of_expenses
    )


with col3:

    st.metric(
        "Average Expense",
        f"₹{average_expense:,.2f}"
    )


st.divider()


# --------------------------------------------------
# Add Expense
# --------------------------------------------------

st.subheader("➕ Add Expense")


with st.form("expense_form"):

    col1, col2 = st.columns(2)

    with col1:

        expense_date = st.date_input(
            "Date"
        )

        category = st.selectbox(
            "Category",
            CATEGORIES
        )

    with col2:

        description = st.text_input(
            "Description",
            placeholder="Example: Lunch"
        )

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.0,
            step=1.0,
            format="%.2f"
        )


    submitted = st.form_submit_button(
        "➕ Add Expense"
    )


    if submitted:

        if amount <= 0:

            st.error(
                "Please enter an amount greater than ₹0."
            )

        else:

            add_expense(
                str(expense_date),
                category,
                description,
                amount
            )

            st.success(
                "Expense added successfully! 🎉"
            )

            st.rerun()


st.divider()


# --------------------------------------------------
# Expense Filters
# --------------------------------------------------

st.subheader("🔎 Filter Expenses")


if not expenses_df.empty:

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:

        selected_category = st.selectbox(
            "Category",
            ["All"] + CATEGORIES
        )

    with filter_col2:

        min_date = expenses_df["Date"].min().date()

        max_date = expenses_df["Date"].max().date()

        selected_dates = st.date_input(
            "Date Range",
            value=(min_date, max_date)
        )


    # --------------------------------------------------
    # Apply Filters
    # --------------------------------------------------

    filtered_df = expenses_df.copy()


    if selected_category != "All":

        filtered_df = filtered_df[
            filtered_df["Category"]
            == selected_category
        ]


    # Date range handling

    if isinstance(selected_dates, tuple):

        if len(selected_dates) == 2:

            start_date = pd.Timestamp(
                selected_dates[0]
            )

            end_date = pd.Timestamp(
                selected_dates[1]
            )

            filtered_df = filtered_df[
                (
                    filtered_df["Date"]
                    >= start_date
                )
                &
                (
                    filtered_df["Date"]
                    <= end_date
                )
            ]


    # --------------------------------------------------
    # Filtered Summary
    # --------------------------------------------------

    st.write("### Filtered Summary")


    filtered_col1, filtered_col2, filtered_col3 = st.columns(3)


    filtered_total = filtered_df["Amount"].sum()

    filtered_count = len(filtered_df)

    if filtered_count > 0:

        filtered_average = (
            filtered_total / filtered_count
        )

    else:

        filtered_average = 0


    with filtered_col1:

        st.metric(
            "Filtered Total",
            f"₹{filtered_total:,.2f}"
        )


    with filtered_col2:

        st.metric(
            "Filtered Expenses",
            filtered_count
        )


    with filtered_col3:

        st.metric(
            "Filtered Average",
            f"₹{filtered_average:,.2f}"
        )


    st.divider()


    # --------------------------------------------------
    # Filtered Expense Table
    # --------------------------------------------------

    st.write("### 📋 Filtered Expense History")


    display_df = filtered_df.copy()

    display_df["Date"] = display_df[
        "Date"
    ].dt.strftime("%Y-%m-%d")


    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------
    # CSV Download
    # --------------------------------------------------

    csv_data = display_df.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(
        label="⬇️ Download Filtered Expenses",
        data=csv_data,
        file_name="filtered_expenses.csv",
        mime="text/csv"
    )


else:

    st.info(
        "Add expenses to use filters."
    )


st.divider()


# --------------------------------------------------
# Spending Analysis
# --------------------------------------------------

st.subheader("📈 Spending Analysis")


analysis_col1, analysis_col2 = st.columns(2)


# --------------------------------------------------
# Category Chart
# --------------------------------------------------

with analysis_col1:

    st.write("### 📊 Spending by Category")


    category_data = get_category_expenses()


    if category_data:

        category_df = pd.DataFrame(
            category_data,
            columns=[
                "Category",
                "Amount"
            ]
        )


        st.bar_chart(
            category_df,
            x="Category",
            y="Amount"
        )

    else:

        st.info(
            "Add expenses to see category analysis."
        )


# --------------------------------------------------
# Monthly Chart
# --------------------------------------------------

with analysis_col2:

    st.write("### 📅 Monthly Spending")


    monthly_data = get_monthly_expenses()


    if monthly_data:

        monthly_df = pd.DataFrame(
            monthly_data,
            columns=[
                "Month",
                "Amount"
            ]
        )


        st.line_chart(
            monthly_df,
            x="Month",
            y="Amount"
        )

    else:

        st.info(
            "Add expenses to see monthly analysis."
        )


st.divider()


# --------------------------------------------------
# Edit Expense
# --------------------------------------------------

st.subheader("✏️ Edit Expense")


if not expenses_df.empty:

    expense_ids = expenses_df["ID"].tolist()


    selected_id = st.selectbox(
        "Select Expense ID",
        expense_ids,
        key="edit_id"
    )


    selected_expense = get_expense_by_id(
        selected_id
    )


    if selected_expense:

        (
            expense_id,
            old_date,
            old_category,
            old_description,
            old_amount
        ) = selected_expense


        edit_col1, edit_col2 = st.columns(2)


        with edit_col1:

            new_date = st.date_input(
                "Date",
                value=pd.to_datetime(
                    old_date
                ).date(),
                key="edit_date"
            )


            category_index = (
                CATEGORIES.index(old_category)
                if old_category in CATEGORIES
                else 0
            )


            new_category = st.selectbox(
                "Category",
                CATEGORIES,
                index=category_index,
                key="edit_category"
            )


        with edit_col2:

            new_description = st.text_input(
                "Description",
                value=old_description or "",
                key="edit_description"
            )


            new_amount = st.number_input(
                "Amount (₹)",
                min_value=0.0,
                value=float(old_amount),
                step=1.0,
                key="edit_amount"
            )


        if st.button(
            "💾 Update Expense"
        ):

            if new_amount <= 0:

                st.error(
                    "Amount must be greater than ₹0."
                )

            else:

                update_expense(
                    selected_id,
                    str(new_date),
                    new_category,
                    new_description,
                    new_amount
                )

                st.success(
                    "Expense updated successfully! ✅"
                )

                st.rerun()


else:

    st.info(
        "There are no expenses available to edit."
    )


st.divider()


# --------------------------------------------------
# Delete Expense
# --------------------------------------------------

st.subheader("🗑️ Delete Expense")


if not expenses_df.empty:

    delete_ids = expenses_df["ID"].tolist()


    delete_id = st.selectbox(
        "Select Expense ID to Delete",
        delete_ids,
        key="delete_id"
    )


    if st.button(
        "🗑️ Delete Selected Expense"
    ):

        delete_expense(
            delete_id
        )

        st.success(
            "Expense deleted successfully."
        )

        st.rerun()


else:

    st.info(
        "There are no expenses available to delete."
    )


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "Personal Expense Tracker | "
    "Built with Python, Streamlit, SQLite and Pandas"
)