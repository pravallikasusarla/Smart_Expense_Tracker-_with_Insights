import streamlit as st
import pandas as pd
import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Smart Expense Tracker",
    layout="wide"
)

# --- 2. DATA PERSISTENCE ---
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Amount", "Category", "Date", "Note"])

# --- 3. SIDEBAR: INPUT & BUDGET ---
st.sidebar.header("Add New Expense")
with st.sidebar.form("expense_form", clear_on_submit=True):
    amount = st.number_input("Amount (INR)", min_value=0.0, step=100.0, format="%.2f")
    category = st.selectbox("Category", ["Food", "Travel", "Bills", "Entertainment", "Shopping", "Health", "Others"])
    date = st.date_input("Date", datetime.date.today())
    note = st.text_input("Note/Description", placeholder="e.g., Dinner")
    submit = st.form_submit_button("Save Transaction")

if submit and amount > 0:
    new_entry = pd.DataFrame([[amount, category, date, note]], columns=st.session_state.expenses.columns)
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_entry], ignore_index=True)
    st.sidebar.success("Transaction Saved")

# --- 4. MONTHLY CALCULATION LOGIC ---
today = datetime.date.today()
current_month = today.month
current_year = today.year

# Convert Date column to datetime objects for filtering
if not st.session_state.expenses.empty:
    st.session_state.expenses['Date'] = pd.to_datetime(st.session_state.expenses['Date']).dt.date

# Filter data for the current month only
monthly_df = st.session_state.expenses[
    (pd.to_datetime(st.session_state.expenses['Date']).dt.month == current_month) & 
    (pd.to_datetime(st.session_state.expenses['Date']).dt.year == current_year)
]

monthly_total = monthly_df['Amount'].sum()
total_all_time = st.session_state.expenses['Amount'].sum()

# Sidebar Budget Feature (Now tracks Monthly Spend)
st.sidebar.divider()
st.sidebar.header(f"Budget for {today.strftime('%B %Y')}")
budget_limit = st.sidebar.number_input("Set Monthly Budget (INR)", min_value=1000.0, value=50000.0, step=1000.0)

progress = min(monthly_total / budget_limit, 1.0)
st.sidebar.write(f"Monthly Spend: INR {monthly_total:,.2f}")
st.sidebar.progress(progress)

if monthly_total > budget_limit:
    st.sidebar.error(f"Over Budget by INR {monthly_total - budget_limit:,.2f}")
else:
    st.sidebar.info(f"INR {budget_limit - monthly_total:,.2f} remaining for this month")

# --- 5. MAIN DASHBOARD ---
st.title("Smart Expense Tracker")
st.subheader(f"Dashboard for {today.strftime('%B %Y')}")

# Top Metrics Row
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("This Month Total", f"INR {monthly_total:,.2f}")
with m2:
    if not monthly_df.empty:
        top_cat = monthly_df.groupby("Category")["Amount"].sum().idxmax()
        st.metric("Monthly Top Category", top_cat)
    else:
        st.metric("Monthly Top Category", "N/A")
with m3:
    st.metric("All-Time Total", f"INR {total_all_time:,.2f}")

st.divider()

# --- 6. VISUALIZATION & HISTORY ---
col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("Monthly Spending Breakdown")
    if not monthly_df.empty:
        cat_data = monthly_df.groupby("Category")["Amount"].sum()
        st.bar_chart(cat_data)
    else:
        st.info("No data for this month yet")

with col_right:
    st.subheader("History (Latest First)")
    if not st.session_state.expenses.empty:
        display_df = st.session_state.expenses.copy()
        # Format date for UI
        display_df['Date'] = pd.to_datetime(display_df['Date']).dt.strftime('%d/%m/%Y')
        st.dataframe(
            display_df.iloc[::-1], # Reverse to show latest first
            use_container_width=True,
            column_config={"Date": st.column_config.TextColumn("Date")}
        )
    else:
        st.write("No history available")

# --- 7. SMART INSIGHTS ---
st.divider()
st.subheader("Monthly Insights")

if not monthly_df.empty:
    highest_cat = monthly_df.groupby("Category")["Amount"].sum().idxmax()
    st.info(f"Analysis: You have spent the most on {highest_cat} this month. Keep an eye on this to stay within your INR {budget_limit:,.2f} limit.")
else:
    st.write("Add transactions to generate monthly insights")
