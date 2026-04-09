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

# Sidebar Budget Feature
st.sidebar.divider()
st.sidebar.header("Monthly Budget Goal")
budget_limit = st.sidebar.number_input("Set Budget (INR)", min_value=1000.0, value=50000.0, step=1000.0)

total_spent = st.session_state.expenses['Amount'].sum()
progress = min(total_spent / budget_limit, 1.0)

st.sidebar.write(f"Total Spent: INR {total_spent:,.2f}")
st.sidebar.progress(progress)

if total_spent > budget_limit:
    st.sidebar.error(f"Over Budget by INR {total_spent - budget_limit:,.2f}")
elif total_spent > budget_limit * 0.8:
    st.sidebar.warning("80% of budget used")
else:
    st.sidebar.info(f"INR {budget_limit - total_spent:,.2f} remaining")

# --- 4. MAIN DASHBOARD ---
st.title("Smart Expense Tracker")
st.markdown("Monitor your spending habits and get financial tips")

# Top Metrics Row
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Total Expenses", f"INR {total_spent:,.2f}")
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
        st.info("Add data to see the chart")

with col_right:
    st.subheader("History")
    if not st.session_state.expenses.empty:
        # Create a display copy to format the date
        display_df = st.session_state.expenses.copy()
        # Force Date to string format DD/MM/YYYY
        display_df['Date'] = pd.to_datetime(display_df['Date']).dt.strftime('%d/%m/%Y')
        
        # Display with specific column configuration to keep the string format
        st.dataframe(
            display_df.sort_index(ascending=False), 
            use_container_width=True,
            column_config={
                "Date": st.column_config.TextColumn("Date")
            }
        )
    else:
        st.write("No history available")

# --- 6. SMART INSIGHTS ENGINE ---
st.divider()
st.subheader("Smart Insights")

if not st.session_state.expenses.empty:
    insight_col1, insight_col2 = st.columns(2)
    cat_totals = st.session_state.expenses.groupby("Category")["Amount"].sum()
    highest_cat = cat_totals.idxmax()
    
    with insight_col1:
        st.write(f"Analysis: You have spent the most on {highest_cat}")
        if highest_cat == "Food":
            st.info("Tip: Ordering in often adds delivery fees. Try cooking at home to save money")
        elif highest_cat == "Shopping":
            st.info("Tip: Use the 30-Day Rule. Wait before buying non-essentials to avoid impulse spending")
        elif highest_cat == "Bills":
            st.info("Tip: Check for recurring subscriptions you do not use anymore")
        elif highest_cat == "Travel":
            st.info("Tip: Consider using public transport to reduce fuel costs")
        else:
            st.info("Tip: Track your small daily costs as they add up over time")

    with insight_col2:
        if total_spent > budget_limit:
            st.error("Action Required: Your spending has crossed your target. Limit non-essential spending")
        else:
            st.success("Status: You are currently within your budget. Keep it up")
else:
    st.write("Add transactions to generate financial advice")

# --- 7. EXPORT FEATURE ---
st.divider()
if not st.session_state.expenses.empty:
    csv = st.session_state.expenses.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Expense Report (CSV)",
        data=csv,
        file_name=f'Expense_Report_{datetime.date.today().strftime("%d_%m_%Y")}.csv',
        mime='text/csv',
    )
