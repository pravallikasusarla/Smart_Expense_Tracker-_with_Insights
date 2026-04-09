import streamlit as st
import pandas as pd
import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# --- 2. DATA PERSISTENCE ---
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Amount", "Category", "Date", "Note"])

# --- 3. SIDEBAR: INPUT & BUDGET ---
st.sidebar.header("Add New Expense")
with st.sidebar.form("expense_form", clear_on_submit=True):
    amount = st.number_input("Amount (₹)", min_value=0.0, step=100.0, format="%.2f")
    category = st.selectbox("Category", ["Food", "Travel", "Bills", "Entertainment", "Shopping", "Health", "Others"])
    date = st.date_input("Date", datetime.date.today())
    note = st.text_input("Note/Description", placeholder="e.g., Dinner at Taj")
    submit = st.form_submit_button("Save Transaction")

if submit and amount > 0:
    new_entry = pd.DataFrame([[amount, category, date, note]], columns=st.session_state.expenses.columns)
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_entry], ignore_index=True)
    st.sidebar.success("Transaction Saved!")

# Sidebar Budget Feature
st.sidebar.divider()
st.sidebar.header("Monthly Budget Goal")
budget_limit = st.sidebar.number_input("Set Budget (₹)", min_value=1000.0, value=50000.0, step=1000.0)

total_spent = st.session_state.expenses['Amount'].sum()
progress = min(total_spent / budget_limit, 1.0)

st.sidebar.write(f"**Total Spent:** ₹{total_spent:,.2f}")
st.sidebar.progress(progress)

if total_spent > budget_limit:
    st.sidebar.error(f"Over Budget by ₹{total_spent - budget_limit:,.2f}!")
elif total_spent > budget_limit * 0.8:
    st.sidebar.warning("Careful! You've used 80% of your budget.")
else:
    st.sidebar.info(f"✅ ₹{budget_limit - total_spent:,.2f} remaining.")

# --- 4. MAIN DASHBOARD ---
st.title("Smart Expense Tracker")
st.markdown("Monitor your spending habits and get smart financial tips.")

# Top Metrics Row
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Total Expenses", f"₹{total_spent:,.2f}")
with m2:
    if not st.session_state.expenses.empty:
        top_cat = st.session_state.expenses.groupby("Category")["Amount"].sum().idxmax()
        st.metric("Top Category", top_cat)
    else:
        st.metric("Top Category", "N/A")
with m3:
    st.metric("Total Transactions", len(st.session_state.expenses))

st.divider()

# --- 5. VISUALIZATION & HISTORY ---
col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("Spending Breakdown")
    if not st.session_state.expenses.empty:
        cat_data = st.session_state.expenses.groupby("Category")["Amount"].sum()
        st.bar_chart(cat_data)
    else:
        st.info("Add data to see the chart.")

with col_right:
    st.subheader("History")
    st.dataframe(st.session_state.expenses.sort_values(by="Date", ascending=False), use_container_width=True)

# --- 6. SMART INSIGHTS ENGINE ---
st.divider()
st.subheader("AI-Powered Smart Insights")
if not st.session_state.expenses.empty:
