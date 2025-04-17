"""
# Patient Cohort Analysis Report

## Analysis Approach
We analyzed patient data by BMI categories using Polars for efficient large-scale data processing. The input CSV was converted to a Parquet file for faster querying. We used Polars' lazy evaluation and streaming capabilities to filter out BMI outliers (values < 10 or > 60) and group patients into cohorts: Underweight, Normal, Overweight, and Obese.

## Observations & Patterns
Across cohorts, average glucose levels and patient age showed distinct trends. For example, higher BMI groups generally had elevated glucose levels, suggesting potential metabolic concerns. The Normal and Overweight groups had the largest patient counts.

## Efficiency with Polars
Polars' lazy evaluation allowed for query optimization by chaining transformations without executing them until needed. Streaming further enabled processing large datasets with minimal memory usage, making it well-suited for scalable cohort analysis.
"""