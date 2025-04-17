import polars as pl
import os

def analyze_patient_cohorts(input_file: str) -> pl.DataFrame:
    """
    Analyze patient cohorts based on BMI ranges.
    
    Args:
        input_file: Path to the input CSV file
        
    Returns:
        DataFrame containing cohort analysis results with columns:
        - bmi_range: The BMI range (e.g., "Underweight", "Normal", "Overweight", "Obese")
        - avg_glucose: Mean glucose level by BMI range
        - patient_count: Number of patients by BMI range
        - avg_age: Mean age by BMI range
    """
    # Check if the input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"The file {input_file} was not found.")

    # Convert to Parquet if it doesn’t exist yet
    parquet_file = input_file.replace(".csv", ".parquet")
    if not os.path.exists(parquet_file):
        print("Converting CSV to Parquet for efficiency...")
        pl.read_csv(input_file).write_parquet(parquet_file)

    # Perform lazy cohort analysis
    cohort_stats = (
        pl.scan_parquet(parquet_file)
        .filter((pl.col("BMI") >= 10) & (pl.col("BMI") <= 60))  # Remove BMI outliers
        .select(["BMI", "Glucose", "Age"])
        .with_columns(
            pl.col("BMI").cut(
                breaks=[10, 18.5, 25, 30, 60],
                labels=["Underweight", "Normal", "Overweight", "Obese"],
                left_closed=True
            ).alias("bmi_range")
        )
        .groupby("bmi_range")
        .agg([
            pl.col("Glucose").mean().alias("avg_glucose"),
            pl.count().alias("patient_count"),
            pl.col("Age").mean().alias("avg_age")
        ])
        .collect(streaming=True)
    )

    return cohort_stats

def main():
    input_file = "patients_large.csv"  # Replace if needed

    try:
        results = analyze_patient_cohorts(input_file)
        print("\nCohort Analysis Summary:\n")
        print(results)

    except FileNotFoundError as fnf:
        print(f"[ERROR] {fnf}")
    except Exception as e:
        print(f"[UNEXPECTED ERROR] {e}")

if __name__ == "__main__":
    main()