import os
import numpy as np
import pandas as pd


def generate_expense_data(num_rows: int = 1200, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)

    categories = {
        "Food": ["Groceries", "Dining Out", "Snacks", "Coffee"],
        "Travel": ["Cab", "Bus", "Train", "Flight"],
        "Rent": ["House Rent", "Hostel Rent", "PG Rent"],
        "Bills": ["Electricity", "Internet", "Water", "Mobile Recharge"],
        "Shopping": ["Clothes", "Electronics", "Accessories", "Books"],
        "Entertainment": ["Movies", "OTT", "Games", "Concert"],
        "Health": ["Medicine", "Doctor", "Gym", "Insurance"],
        "Education": ["Course", "Books", "Exam Fee", "Stationery"],
        "Salary": ["Monthly Salary", "Freelance", "Internship Stipend"],
        "Savings": ["Emergency Fund", "Investment", "Fixed Deposit"]
    }

    payment_methods = ["UPI", "Credit Card", "Debit Card", "Cash", "Net Banking"]
    cities = ["Kolkata", "Delhi", "Mumbai", "Bengaluru", "Pune"]
    merchants = [
        "Amazon", "Flipkart", "Swiggy", "Zomato", "Uber", "Ola",
        "Big Bazaar", "DMart", "BookMyShow", "Apollo", "Local Store"
    ]

    start_date = pd.Timestamp("2025-01-01")
    end_date = pd.Timestamp("2025-12-31")
    random_dates = pd.to_datetime(
        np.random.randint(start_date.value // 10**9, end_date.value // 10**9, num_rows),
        unit="s"
    )

    rows = []

    for _ in range(num_rows):
        category = np.random.choice(list(categories.keys()))

        if category in ["Salary", "Savings"]:
            txn_type = "Income" if category == "Salary" else "Expense"
        else:
            txn_type = "Expense"

        subcategory = np.random.choice(categories[category])
        date = np.random.choice(random_dates)
        payment_method = np.random.choice(payment_methods)
        city = np.random.choice(cities)
        merchant = np.random.choice(merchants)

        amount_ranges = {
            "Food": (80, 1800),
            "Travel": (50, 8000),
            "Rent": (4000, 25000),
            "Bills": (200, 5000),
            "Shopping": (300, 12000),
            "Entertainment": (100, 5000),
            "Health": (150, 10000),
            "Education": (200, 15000),
            "Salary": (15000, 60000),
            "Savings": (500, 15000),
        }

        low, high = amount_ranges[category]
        amount = round(np.random.uniform(low, high), 2)

        notes = f"{subcategory} payment via {payment_method}"

        rows.append({
            "Date": date,
            "Category": category,
            "Subcategory": subcategory,
            "Amount": amount,
            "Type": txn_type,
            "Payment_Method": payment_method,
            "City": city,
            "Merchant": merchant,
            "Notes": notes
        })

    df = pd.DataFrame(rows).sort_values("Date").reset_index(drop=True)

    return df


def save_raw_data(output_path: str = "data/raw/expenses_raw.csv", num_rows: int = 1200) -> str:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = generate_expense_data(num_rows=num_rows)
    df.to_csv(output_path, index=False)
    return output_path


if __name__ == "__main__":
    path = save_raw_data()
    print(f"Raw synthetic dataset saved to: {path}")