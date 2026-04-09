import streamlit as st
import pd as pd
import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Monthly Expense Tracker",
    layout="wide"
)

# --- 2. DATA PERSISTENCE ---
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Amount", "Category", "Date"])

# --- 3. SIDEBAR: ADD EXPENSE ---
st.sidebar.header("Add New Expense")
with st.sidebar.form("expense_form", clear_on_submit=True):
    amount = st.number_input("Amount (INR)", min_value=0.0, step=100.0, format="%.2f")
    category = st.selectbox("Category", ["Food", "Travel", "Bills", "Entertainment", "Shopping", "Health", "Others"])
    
    # --- CHANGED DATE FORMAT HERE ---
    date = st.date_input("Date", datetime.date.today(), format="DD/MM/YYYY")
    
    submit = st.form_submit_button("Save Transaction")

if submit:
    if amount <= 0:
        st.sidebar.error("Please enter an amount greater than 0.")
    elif date > datetime.date.today():
        st.sidebar.error("Error: Future dates are not allowed!")
    else:
        new_data = {"Amount": [amount], "Category": [category], "Date": [date]}
        new_entry = pd.DataFrame(new_data)
        st.session_state.expenses = pd.concat([st.session_state.expenses, new_entry], ignore_index=True)
        st.sidebar.success("Transaction Saved!")

# --- 4. MONTHLY CALCULATION LOGIC ---
today = datetime.date.today()
current_month = today.month
current_year = today.year

if not st.session_state.expenses.empty:
    st.session_state.expenses['Date'] = pd.to_datetime(st.session_state.expenses['Date']).dt.date
    monthly_mask = (pd.to_datetime(st.session_state.expenses['Date']).dt.month == current_month) & \
                   (pd.to_datetime(st.session_state.expenses['Date']).dt.year == current_year)
    monthly_df = st.session_state.expenses[monthly_mask]
else:
    monthly_df = st.session_state.expenses

monthly_total = monthly_df['Amount'].sum()

# --- 5. SIDEBAR: MONTHLY BUDGET ---
st.sidebar.divider()
st.sidebar.header(f"Budget: {today.strftime('%B %Y')}")
budget_limit = st.sidebar.number_input("Monthly Limit (INR)", min_value=1000.0, value=20000.0)
progress = min(monthly_total / budget_limit, 1.0)
st.sidebar.progress(progress)
st.sidebar.write(f"Spent: INR {monthly_total:,.2f} / INR {budget_limit:,.2f}")

# --- 6. MAIN DASHBOARD ---
st.title(f"Expense Dashboard: {today.strftime('%B %Y')}")

m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Monthly Spending", f"INR {monthly_total:,.2f}")
with m2:
    if not monthly_df.empty:
        top_cat = monthly_df.groupby("Category")["Amount"].sum().idxmax()
        st.metric("Top Category", top_cat)
    else:
        st.metric("Top Category", "N/A")
with m3:
    st.metric("Monthly Transactions", len(monthly_df))

st.divider()

# --- 7. VISUALS & HISTORY ---
col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("Monthly Analysis")
    if not monthly_df.empty:
        cat_data = monthly_df.groupby("Category")["Amount"].sum()
        st.bar_chart(cat_data)
    else:
        st.info("No expenses recorded this month")

with col_right:
    st.subheader("Recent Activity")
    if not monthly_df.empty:
        display_df = monthly_df.copy()
        display_df['Date'] = pd.to_datetime(display_df['Date']).dt.strftime('%d/%m/%Y')
        st.dataframe(
            display_df.sort_index(ascending=False), 
            use_container_width=True,
            column_config={"Date": st.column_config.TextColumn("Date")}
        )
    else:
        st.write("No transactions for this month")

# --- 8. SMART TIPS ---
st.divider()
st.subheader("Smart Financial Tips")
if not monthly_df.empty:
    highest_cat = monthly_df.groupby("Category")["Amount"].sum().idxmax()
    st.info(f"Tip: You are spending the most on **{highest_cat}**. Try to keep an eye on this to save more this month!")
