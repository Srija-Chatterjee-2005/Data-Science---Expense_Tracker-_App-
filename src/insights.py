import os
import pandas as pd


def generate_insights(df: pd.DataFrame, output_path: str = "outputs/reports/insights.txt") -> list[str]:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    insights = []
    expense_df = df[df["Type"] == "Expense"].copy()
    income_df = df[df["Type"] == "Income"].copy()

    total_income = income_df["Amount"].sum()
    total_expense = expense_df["Amount"].sum()
    net_balance = total_income - total_expense

    insights.append(f"Total income recorded: ₹{total_income:,.2f}")
    insights.append(f"Total expenses recorded: ₹{total_expense:,.2f}")
    insights.append(f"Net balance: ₹{net_balance:,.2f}")

    if not expense_df.empty:
        top_category = expense_df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
        top_cat_name = top_category.index[0]
        top_cat_amount = top_category.iloc[0]
        top_cat_share = (top_cat_amount / total_expense) * 100 if total_expense > 0 else 0
        insights.append(
            f"Highest spending category is {top_cat_name} with ₹{top_cat_amount:,.2f}, contributing {top_cat_share:.2f}% of total expenses."
        )

        monthly_expense = expense_df.groupby(["Year", "Month_Num", "Month"])["Amount"].sum().reset_index()
        max_month = monthly_expense.sort_values("Amount", ascending=False).iloc[0]
        insights.append(
            f"Highest spending month is {max_month['Month']} {int(max_month['Year'])} with ₹{max_month['Amount']:,.2f}."
        )

        subcategory_spend = expense_df.groupby(["Category", "Subcategory"])["Amount"].sum().reset_index()
        max_sub = subcategory_spend.sort_values("Amount", ascending=False).iloc[0]
        insights.append(
            f"Top subcategory spending is {max_sub['Subcategory']} under {max_sub['Category']} with ₹{max_sub['Amount']:,.2f}."
        )

        payment_method = expense_df.groupby("Payment_Method")["Amount"].sum().sort_values(ascending=False)
        insights.append(
            f"Most-used payment channel by spending value is {payment_method.index[0]} with ₹{payment_method.iloc[0]:,.2f}."
        )

        city_spend = expense_df.groupby("City")["Amount"].sum().sort_values(ascending=False)
        insights.append(
            f"Highest expense city is {city_spend.index[0]} with total spend of ₹{city_spend.iloc[0]:,.2f}."
        )

        expense_df["Z_Score_Base"] = (expense_df["Amount"] - expense_df["Amount"].mean()) / (expense_df["Amount"].std(ddof=0) + 1e-9)
        anomalies = expense_df[expense_df["Z_Score_Base"] > 2.5]

        insights.append(f"Detected {len(anomalies)} unusually high-value transactions based on z-score analysis.")

        weekday_spend = expense_df.groupby("Weekend_Flag")["Amount"].sum()
        if "Weekend" in weekday_spend.index and "Weekday" in weekday_spend.index:
            insights.append(
                f"Weekend spending is ₹{weekday_spend['Weekend']:,.2f} versus weekday spending of ₹{weekday_spend['Weekday']:,.2f}."
            )

        # Overspending rule: categories above average category spend
        category_totals = expense_df.groupby("Category")["Amount"].sum()
        avg_category_spend = category_totals.mean()
        overspending_categories = category_totals[category_totals > avg_category_spend].index.tolist()

        if overspending_categories:
            insights.append(
                "Potential overspending categories: " + ", ".join(overspending_categories) + "."
            )

    if total_income > 0:
        savings_rate = (net_balance / total_income) * 100
        insights.append(f"Estimated savings rate: {savings_rate:.2f}% of income.")

    with open(output_path, "w", encoding="utf-8") as f:
        for item in insights:
            f.write(f"- {item}\n")

    return insights