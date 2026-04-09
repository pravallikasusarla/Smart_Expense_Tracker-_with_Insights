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

# --- 3. SIDEBAR: INPUT ---
st.sidebar.header("Add New Expense")
with st.sidebar.form("expense_form", clear_on_submit=True):
    amount = st.number_input("Amount (INR)", min_value=0.0, step=100.0, format="%.2f")
    category = st.selectbox("Category", ["Food", "Travel", "Bills", "Entertainment", "Shopping", "Health", "Others"])
    date = st.date_input("Date", datetime.date.today())
    note = st.text_input("Note/Description")
    submit = st.form_submit_button("Save Transaction")

if submit and amount > 0:
    new_entry = pd.DataFrame([[amount, category, date, note]], columns=st.session_state.expenses.columns)
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_entry], ignore_index=True)
    st.sidebar.success("Transaction Saved")

# --- 4. SIDEBAR: DATE RANGE FILTER ---
st.sidebar.divider()
st.sidebar.header("Filter by Date Range")

# This creates the "From" and "To" selection in one box
today = datetime.date.today()
start_of_month = today.replace(day=1)

date_range = st.sidebar.date_input(
    "Select Range",
    value=(start_of_month, today),
    max_value=today
)

# --- 5. FILTERING LOGIC ---
if not st.session_state.expenses.empty:
    # Ensure Date column is datetime objects
    st.session_state.expenses['Date'] = pd.to_datetime(st.session_state.expenses['Date']).dt.date
    
    # Check if user selected both start and end dates
    if len(date_range) == 2:
        start_date, end_date = date_range
        mask = (st.session_state.expenses['Date'] >= start_date) & (st.session_state.expenses['Date'] <= end_date)
        filtered_df = st.session_state.expenses[mask]
    else:
        filtered_df = st.session_state.expenses
else:
    filtered_df = st.session_state.expenses

# Calculations based on Filtered Data
filtered_total = filtered_df['Amount'].sum()

# --- 6. MAIN DASHBOARD ---
st.title("Smart Expense Tracker")

# Metrics Row
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Total in Selected Range", f"INR {filtered_total:,.2f}")
with m2:
    if not filtered_df.empty:
        top_cat = filtered_df.groupby("Category")["Amount"].sum().idxmax()
        st.metric("Top Category (Filtered)", top_cat)
    else:
        st.metric("Top Category (Filtered)", "N/A")
with m3:
    st.metric("Transactions Found", len(filtered_df))

st.divider()

# --- 7. VISUALIZATION & HISTORY ---
col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("Spending Breakdown (Selected Range)")
    if not filtered_df.empty:
        cat_data = filtered_df.groupby("Category")["Amount"].sum()
        st.bar_chart(cat_data)
    else:
        st.info("No data found for this date range")

with col_right:
    st.subheader("History (DD/MM/YYYY)")
    if not filtered_df.empty:
        display_df = filtered_df.copy()
        # Formatting Date to DD/MM/YYYY
        display_df['Date'] = pd.to_datetime(display_df['Date']).dt.strftime('%d/%m/%Y')
        st.dataframe(
            display_df.sort_values(by="Date", ascending=False), 
            use_container_width=True,
            column_config={"Date": st.column_config.TextColumn("Date")}
        )
    else:
        st.write("No history available for this range")

# --- 8. SMART INSIGHTS ---
st.divider()
st.subheader("Range Insights")
if not filtered_df.empty:
    st.info(f"Between {date_range[0].strftime('%d/%m/%Y')} and {date_range[1].strftime('%d/%m/%Y') if len(date_range)>1 else ''}, you spent INR {filtered_total:,.2f}.")
