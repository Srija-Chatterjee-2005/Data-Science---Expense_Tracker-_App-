import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


sns.set_style("whitegrid")


def save_visualizations(df: pd.DataFrame, output_dir: str = "outputs/charts") -> None:
    os.makedirs(output_dir, exist_ok=True)

    expense_df = df[df["Type"] == "Expense"].copy()
    income_df = df[df["Type"] == "Income"].copy()

    # 1. Category spending bar chart
    category_spend = expense_df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=category_spend.values, y=category_spend.index)
    plt.title("Category-wise Expense Spending")
    plt.xlabel("Amount")
    plt.ylabel("Category")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/category_spending_bar.png")
    plt.close()

    # 2. Expense distribution pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(category_spend.values, labels=category_spend.index, autopct="%1.1f%%", startangle=90)
    plt.title("Expense Share by Category")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/category_spending_pie.png")
    plt.close()

    # 3. Monthly income vs expense line chart
    monthly_expense = expense_df.groupby(["Year", "Month_Num", "Month"])["Amount"].sum().reset_index()
    monthly_income = income_df.groupby(["Year", "Month_Num", "Month"])["Amount"].sum().reset_index()

    plt.figure(figsize=(12, 6))
    if not monthly_expense.empty:
        plt.plot(monthly_expense["Month_Num"], monthly_expense["Amount"], marker="o", label="Expense")
    if not monthly_income.empty:
        plt.plot(monthly_income["Month_Num"], monthly_income["Amount"], marker="o", label="Income")
    plt.title("Monthly Income vs Expense")
    plt.xlabel("Month Number")
    plt.ylabel("Amount")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{output_dir}/monthly_income_vs_expense.png")
    plt.close()

    # 4. Payment method chart
    payment_spend = expense_df.groupby("Payment_Method")["Amount"].sum().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=payment_spend.index, y=payment_spend.values)
    plt.title("Spending by Payment Method")
    plt.xlabel("Payment Method")
    plt.ylabel("Amount")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/payment_method_spending.png")
    plt.close()

    # 5. Weekday spending
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_spend = expense_df.groupby("Weekday")["Amount"].sum().reindex(weekday_order)
    plt.figure(figsize=(10, 5))
    sns.barplot(x=weekday_spend.index, y=weekday_spend.values)
    plt.title("Weekday-wise Spending")
    plt.xlabel("Weekday")
    plt.ylabel("Amount")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/weekday_spending.png")
    plt.close()

    # 6. Category-month heatmap
    category_month = expense_df.pivot_table(
        values="Amount",
        index="Category",
        columns="Month_Num",
        aggfunc="sum",
        fill_value=0
    )
    plt.figure(figsize=(12, 6))
    sns.heatmap(category_month, annot=True, fmt=".0f", cmap="YlGnBu")
    plt.title("Category vs Month Spending Heatmap")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/category_month_heatmap.png")
    plt.close()

    # 7. Transaction distribution boxplot
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=expense_df, x="Category", y="Amount")
    plt.title("Transaction Amount Distribution by Category")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/category_boxplot.png")
    plt.close()