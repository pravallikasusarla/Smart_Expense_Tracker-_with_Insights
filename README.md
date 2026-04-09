# Smart Expense Tracker

A streamlined **Streamlit** web application designed to track monthly expenses, visualize spending habits, and manage personal budgets effectively.

## Features

* **Monthly Dashboard**: Automatically filters and displays spending for the current month.
* **Budget Management**: Set a monthly limit and track progress with a dynamic visual bar.
* **Smart Insights**: Provides automated financial tips based on your highest spending category.
* **Data Validation**: 
    * Prevents entry of future dates.
    * Ensures valid transaction amounts.
* **Localized Formatting**: Supports **INR (₹)** and uses **DD/MM/YYYY** date formats for better readability.
* **Clean History**: View transactions in a structured table with the latest entries at the top.

## Tech Stack

* **Python 3.10+**
* **Streamlit** (UI Framework)
* **Pandas** (Data Processing)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/smart-expense-tracker.git
   ```
2. Install dependencies:
   ```bash
   pip install streamlit pandas
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```
