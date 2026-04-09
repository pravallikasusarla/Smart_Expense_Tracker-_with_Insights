import streamlit as st
import pandas as pd
import datetime

# --- Page Configuration ---
st.set_page_config(page_title="Smart Expense Tracker", page_icon="💰", layout="wide")

st.title("Smart Expense Tracker")

if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Amount", "Category", "Date", "Note"])

# Sidebar: Add Expense
st.sidebar.header("Add New Expense")
with st.sidebar.form("expense_form", clear_on_submit=True):
    amount = st.number_input("Amount (₹)", min_value=0.0, step=1.0, format="%.2f")
    category = st.selectbox("Category", ["Food", "Travel", "Bills", "Entertainment", "Shopping", "Others"])
    date = st.date_input("Date", datetime.date.today())
    note = st.text_input("Note")
    submit = st.form_submit_button("Save")

if submit and amount > 0:
    new_entry = pd.DataFrame([[amount, category, date, note]], columns=st.session_state.expenses.columns)
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_entry], ignore_index=True)
    st.sidebar.success("Saved!")

# Dashboard
total_spent = st.session_state.expenses['Amount'].sum()
st.metric("Total Spending", f"₹{total_spent:,.2f}")

if not st.session_state.expenses.empty:
    st.dataframe(st.session_state.expenses, use_container_width=True)
    st.subheader("Insights")
    cat_data = st.session_state.expenses.groupby("Category")["Amount"].sum()
    st.bar_chart(cat_data)
else:
    st.info("Add an expense to start!")
