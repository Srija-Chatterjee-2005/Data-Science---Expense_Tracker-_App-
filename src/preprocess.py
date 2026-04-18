import os
import pandas as pd


def preprocess_expense_data(input_path: str, output_path: str = "data/processed/expenses_cleaned.csv") -> pd.DataFrame:
    df = pd.read_csv(input_path)

    # Remove duplicates
    df = df.drop_duplicates()

    # Clean column names
    df.columns = [col.strip() for col in df.columns]

    # Handle missing values
    df["Category"] = df["Category"].fillna("Unknown").astype(str).str.strip().str.title()
    df["Subcategory"] = df["Subcategory"].fillna("Unknown").astype(str).str.strip().str.title()
    df["Type"] = df["Type"].fillna("Expense").astype(str).str.strip().str.title()
    df["Payment_Method"] = df["Payment_Method"].fillna("Unknown").astype(str).str.strip().str.title()
    df["City"] = df["City"].fillna("Unknown").astype(str).str.strip().str.title()
    df["Merchant"] = df["Merchant"].fillna("Unknown").astype(str).str.strip()
    df["Notes"] = df["Notes"].fillna("").astype(str).str.strip()

    # Convert data types
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    # Drop invalid critical rows
    df = df.dropna(subset=["Date", "Amount", "Category", "Type"])

    # Remove negative or zero values if needed
    df = df[df["Amount"] > 0].copy()

    # Feature engineering
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month_name()
    df["Month_Num"] = df["Date"].dt.month
    df["Quarter"] = "Q" + df["Date"].dt.quarter.astype(str)
    df["Weekday"] = df["Date"].dt.day_name()
    df["Day"] = df["Date"].dt.day
    df["Weekend_Flag"] = df["Weekday"].isin(["Saturday", "Sunday"]).map({True: "Weekend", False: "Weekday"})

    # Expense bucket
    def bucketize(amount):
        if amount < 500:
            return "Low"
        elif amount < 3000:
            return "Medium"
        else:
            return "High"

    df["Expense_Bucket"] = df["Amount"].apply(bucketize)

    # Sort
    df = df.sort_values("Date").reset_index(drop=True)

    # Save processed data
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    return df


if __name__ == "__main__":
    cleaned = preprocess_expense_data("data/raw/expenses_raw.csv")
    print(cleaned.head())