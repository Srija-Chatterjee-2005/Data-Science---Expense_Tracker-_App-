import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Expense Tracker Dashboard", layout="wide")

# =========================
# DARK THEME (BLACK UI)
# =========================
st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #0e1117;
        color: white;
    }

    /* Text color */
    html, body, [class*="css"] {
        color: #ffffff;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    /* Cards (metrics look better) */
    div[data-testid="metric-container"] {
        background-color: #1f2937;
        border: 1px solid #374151;
        padding: 10px;
        border-radius: 10px;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: #1f2937;
        color: white;
    }

    /* Tabs */
    button[role="tab"] {
        background-color: #1f2937;
        color: white;
        border-radius: 8px;
        padding: 8px;
    }

    button[role="tab"][aria-selected="true"] {
        background-color: #2563eb;
        color: white;
    }

    /* Dataframe */
    .stDataFrame {
        background-color: #111827;
    }

    /* Buttons */
    .stButton>button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
    }

    /* Download button */
    .stDownloadButton>button {
        background-color: #10b981;
        color: white;
        border-radius: 8px;
    }

</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/expenses_cleaned.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

st.title("💰 Expense Tracker Analytics Dashboard")
st.markdown("A finance analytics dashboard for tracking expenses, patterns, trends, and business insights.")

# =========================
# FILTER SECTION
# =========================
with st.expander("🔍 Filter Transactions", expanded=True):
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        category_options = sorted(df["Category"].unique().tolist())
        selected_categories = st.multiselect(
            "Category",
            category_options,
            default=category_options
        )

    with c2:
        city_options = sorted(df["City"].unique().tolist())
        selected_cities = st.multiselect(
            "City",
            city_options,
            default=city_options
        )

    with c3:
        type_options = sorted(df["Type"].unique().tolist())
        selected_types = st.multiselect(
            "Transaction Type",
            type_options,
            default=type_options
        )

    with c4:
        min_date = df["Date"].min().date()
        max_date = df["Date"].max().date()
        date_range = st.date_input(
            "Date Range",
            [min_date, max_date]
        )

filtered_df = df[
    (df["Category"].isin(selected_categories)) &
    (df["City"].isin(selected_cities)) &
    (df["Type"].isin(selected_types))
].copy()

if len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered_df = filtered_df[
        (filtered_df["Date"] >= start_date) &
        (filtered_df["Date"] <= end_date)
    ]

expense_df = filtered_df[filtered_df["Type"] == "Expense"]
income_df = filtered_df[filtered_df["Type"] == "Income"]

# =========================
# KPI SECTION
# =========================
total_income = income_df["Amount"].sum()
total_expense = expense_df["Amount"].sum()
net_balance = total_income - total_expense
avg_transaction = filtered_df["Amount"].mean() if not filtered_df.empty else 0

top_category = "N/A"
if not expense_df.empty:
    top_category = expense_df.groupby("Category")["Amount"].sum().sort_values(ascending=False).index[0]

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Income", f"₹{total_income:,.2f}")
k2.metric("Total Expense", f"₹{total_expense:,.2f}")
k3.metric("Net Balance", f"₹{net_balance:,.2f}")
k4.metric("Avg Transaction", f"₹{avg_transaction:,.2f}")
k5.metric("Top Category", top_category)

st.divider()

# =========================
# TABS
# =========================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "🗂 Category Analysis",
    "📈 Trend Analysis",
    "💡 Insights",
    "🧾 Transactions"
])

# =========================
# TAB 1 - OVERVIEW
# =========================
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Expense Share by Category")
        if not expense_df.empty:
            pie_data = expense_df.groupby("Category")["Amount"].sum()
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(pie_data.values, labels=pie_data.index, autopct="%1.1f%%", startangle=90)
            ax.axis("equal")
            st.pyplot(fig)
        else:
            st.info("No expense data available.")

    with col2:
        st.subheader("Payment Method Spend")
        if not expense_df.empty:
            payment_spend = expense_df.groupby("Payment_Method")["Amount"].sum().sort_values(ascending=False)
            st.bar_chart(payment_spend)
        else:
            st.info("No expense data available.")

# =========================
# TAB 2 - CATEGORY ANALYSIS
# =========================
with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Category-wise Spending")
        if not expense_df.empty:
            category_spend = expense_df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(x=category_spend.values, y=category_spend.index, ax=ax)
            ax.set_xlabel("Amount")
            ax.set_ylabel("Category")
            st.pyplot(fig)
        else:
            st.info("No expense data available.")

    with col2:
        st.subheader("Subcategory Spending")
        if not expense_df.empty:
            subcategory_spend = expense_df.groupby("Subcategory")["Amount"].sum().sort_values(ascending=False).head(10)
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(x=subcategory_spend.values, y=subcategory_spend.index, ax=ax)
            ax.set_xlabel("Amount")
            ax.set_ylabel("Subcategory")
            st.pyplot(fig)
        else:
            st.info("No expense data available.")

# =========================
# TAB 3 - TREND ANALYSIS
# =========================
with tab3:
    st.subheader("Monthly Spending Trend")
    if not filtered_df.empty:
        monthly = filtered_df.groupby(filtered_df["Date"].dt.to_period("M"))["Amount"].sum()
        monthly.index = monthly.index.astype(str)
        st.line_chart(monthly)
    else:
        st.info("No data available.")

    st.subheader("Weekday Spending Pattern")
    if not expense_df.empty:
        weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        weekday_spend = expense_df.groupby("Weekday")["Amount"].sum().reindex(weekday_order)
        fig, ax = plt.subplots(figsize=(9, 4))
        sns.barplot(x=weekday_spend.index, y=weekday_spend.values, ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=25)
        st.pyplot(fig)
    else:
        st.info("No expense data available.")

# =========================
# TAB 4 - INSIGHTS
# =========================
with tab4:
    st.subheader("Generated Business Insights")

    if not expense_df.empty:
        top_category_series = expense_df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
        top_cat_name = top_category_series.index[0]
        top_cat_amount = top_category_series.iloc[0]

        monthly_expense = expense_df.groupby(expense_df["Date"].dt.to_period("M"))["Amount"].sum().sort_values(ascending=False)
        top_month = monthly_expense.index[0]
        top_month_amount = monthly_expense.iloc[0]

        payment_spend = expense_df.groupby("Payment_Method")["Amount"].sum().sort_values(ascending=False)
        top_payment = payment_spend.index[0]

        city_spend = expense_df.groupby("City")["Amount"].sum().sort_values(ascending=False)
        top_city = city_spend.index[0]

        st.success(f"Highest spending category: {top_cat_name} (₹{top_cat_amount:,.2f})")
        st.info(f"Highest spending month: {top_month} (₹{top_month_amount:,.2f})")
        st.warning(f"Most-used payment channel: {top_payment}")
        st.error(f"Highest spending city: {top_city}")

        if total_income > 0:
            savings_rate = (net_balance / total_income) * 100
            st.write(f"Estimated savings rate: **{savings_rate:.2f}%**")

        st.subheader("Category Summary Table")
        summary_table = expense_df.groupby("Category", as_index=False)["Amount"].sum().sort_values("Amount", ascending=False)
        st.dataframe(summary_table, use_container_width=True)
    else:
        st.info("No insights available.")

# =========================
# TAB 5 - TRANSACTIONS
# =========================
with tab5:
    st.subheader("Filtered Transaction Data")
    st.dataframe(filtered_df, use_container_width=True)

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_expense_data.csv",
        mime="text/csv"
    )