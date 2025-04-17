"""
# Patient Cohort Analysis Report

## Analysis Approach
- Analyzed patient data by BMI categories using Polars.
- Converted input CSV to Parquet.
- Filtered out BMI outliers (values < 10 or > 60).
- Grouped patients into four BMI ranges: Underweight, Normal, Overweight, and Obese.
- Calculated average glucose, patient count, and average age of each cohort. 

## Observations & Patterns
- Higher BMI groups had higher average glucose levels
- Normal and Overweight cohorts had the largest patient counts
- Average age varied across cohorts, older patients more likely to have higher BMIs.

## Efficiency with Polars
- Lazy evaluation in Polars allowed for efficient, on-demand query execution.
- Streaming enabled handling large datasets with minimal memory usage.
"""