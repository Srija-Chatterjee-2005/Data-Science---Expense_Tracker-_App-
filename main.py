import os
from src.generate_data import save_raw_data
from src.preprocess import preprocess_expense_data
from src.analysis import run_analysis
from src.insights import generate_insights
from src.visualize import save_visualizations


def ensure_directories() -> None:
    folders = [
        "data/raw",
        "data/processed",
        "outputs/charts",
        "outputs/reports",
        "outputs/logs"
    ]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)


def main() -> None:
    ensure_directories()

    print("Step 1: Generating synthetic expense data...")
    raw_path = save_raw_data(output_path="data/raw/expenses_raw.csv", num_rows=1500)
    print(f"Raw data saved: {raw_path}")

    print("Step 2: Cleaning and preprocessing data...")
    df = preprocess_expense_data(raw_path, output_path="data/processed/expenses_cleaned.csv")
    print("Cleaned data saved to data/processed/expenses_cleaned.csv")

    print("Step 3: Running analysis...")
    run_analysis(df, output_dir="outputs/reports")
    print("Analysis reports generated in outputs/reports")

    print("Step 4: Generating insights...")
    insights = generate_insights(df, output_path="outputs/reports/insights.txt")
    print("Insights saved to outputs/reports/insights.txt")

    print("Step 5: Creating charts...")
    save_visualizations(df, output_dir="outputs/charts")
    print("Charts saved to outputs/charts")

    print("\nProject completed successfully.\n")
    print("Top generated insights:")
    for item in insights[:5]:
        print("-", item)


if __name__ == "__main__":
    main()