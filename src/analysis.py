import os
import pandas as pd


def run_analysis(df: pd.DataFrame, output_dir: str = "outputs/reports") -> dict:
    os.makedirs(output_dir, exist_ok=True)

    expense_df = df[df["Type"] == "Expense"].copy()
    income_df = df[df["Type"] == "Income"].copy()

    results = {}

    # Category analysis
    category_spend = expense_df.groupby("Category", as_index=False)["Amount"].sum().sort_values("Amount", ascending=False)
    results["category_spend"] = category_spend
    category_spend.to_csv(f"{output_dir}/category_spending.csv", index=False)

    # Subcategory analysis
    subcategory_spend = expense_df.groupby(["Category", "Subcategory"], as_index=False)["Amount"].sum()
    subcategory_spend = subcategory_spend.sort_values("Amount", ascending=False)
    results["subcategory_spend"] = subcategory_spend
    subcategory_spend.to_csv(f"{output_dir}/subcategory_spending.csv", index=False)

    # Monthly trend
    monthly_summary = df.groupby(["Year", "Month_Num", "Month", "Type"], as_index=False)["Amount"].sum()
    monthly_summary = monthly_summary.sort_values(["Year", "Month_Num", "Type"])
    results["monthly_summary"] = monthly_summary
    monthly_summary.to_csv(f"{output_dir}/monthly_summary.csv", index=False)

    # Monthly expense only
    monthly_expense = expense_df.groupby(["Year", "Month_Num", "Month"], as_index=False)["Amount"].sum()
    monthly_expense = monthly_expense.sort_values(["Year", "Month_Num"])
    results["monthly_expense"] = monthly_expense
    monthly_expense.to_csv(f"{output_dir}/monthly_expense.csv", index=False)

    # Payment method analysis
    payment_analysis = expense_df.groupby("Payment_Method", as_index=False)["Amount"].sum().sort_values("Amount", ascending=False)
    results["payment_analysis"] = payment_analysis
    payment_analysis.to_csv(f"{output_dir}/payment_method_analysis.csv", index=False)

    # City analysis
    city_analysis = expense_df.groupby("City", as_index=False)["Amount"].sum().sort_values("Amount", ascending=False)
    results["city_analysis"] = city_analysis
    city_analysis.to_csv(f"{output_dir}/city_analysis.csv", index=False)

    # Weekday analysis
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_analysis = expense_df.groupby("Weekday", as_index=False)["Amount"].sum()
    weekday_analysis["Weekday"] = pd.Categorical(weekday_analysis["Weekday"], categories=weekday_order, ordered=True)
    weekday_analysis = weekday_analysis.sort_values("Weekday")
    results["weekday_analysis"] = weekday_analysis
    weekday_analysis.to_csv(f"{output_dir}/weekday_analysis.csv", index=False)

    # Weekend vs Weekday
    weekend_analysis = expense_df.groupby("Weekend_Flag", as_index=False)["Amount"].sum().sort_values("Amount", ascending=False)
    results["weekend_analysis"] = weekend_analysis
    weekend_analysis.to_csv(f"{output_dir}/weekend_analysis.csv", index=False)

    # Category-month pivot
    category_month = expense_df.pivot_table(
        values="Amount",
        index="Category",
        columns="Month_Num",
        aggfunc="sum",
        fill_value=0
    )
    results["category_month"] = category_month
    category_month.to_csv(f"{output_dir}/category_month_pivot.csv")

    # Income vs expense summary
    total_income = income_df["Amount"].sum()
    total_expense = expense_df["Amount"].sum()
    net_balance = total_income - total_expense

    summary = pd.DataFrame([{
        "Total_Income": round(total_income, 2),
        "Total_Expense": round(total_expense, 2),
        "Net_Balance": round(net_balance, 2)
    }])
    results["summary"] = summary
    summary.to_csv(f"{output_dir}/overall_summary.csv", index=False)

    return results