#!/usr/bin/env python3
"""
Patient Data Cleaner

This script standardizes and filters patient records according to specific rules:

Data Cleaning Rules:
1. Names: Capitalize each word (e.g., "john smith" -> "John Smith")
2. Ages: Convert to integers, set invalid ages to 0
3. Filter: Remove patients under 18 years old
4. Remove any duplicate records

Input JSON format:
    [
        {
            "name": "john smith",
            "age": "32",
            "gender": "male",
            "diagnosis": "hypertension"
        },
        ...
    ]

Output:
- Cleaned list of patient dictionaries
- Each patient should have:
  * Properly capitalized name
  * Integer age (≥ 18)
  * Original gender and diagnosis preserved
- No duplicate records
- Prints cleaned records to console

Example:
    Input: {"name": "john smith", "age": "32", "gender": "male", "diagnosis": "flu"}
    Output: {"name": "John Smith", "age": 32, "gender": "male", "diagnosis": "flu"}

Usage:
    python patient_data_cleaner.py
"""

import json
import os
import pdb  # Used for debugging
import pandas as pd  # Used for deduplication and data cleaning
import sys

def load_patient_data(filepath):
    """
    Load patient data from a JSON file.
    
    Args:
        filepath (str): Path to the JSON file
        
    Returns:
        list: List of patient dictionaries
    """
    # BUG: No error handling for file not found
    # FIX: Added try-except block for FileNotFoundError
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("File not found!")
        sys.exit(1)
    except json.JSONDecodeError:
        # BUG: No handling for bad JSON
        # FIX: Added JSON decoding error check
        print("Error decoding JSON!")
        sys.exit(1)

def clean_patient_data(patients):
    """
    Clean patient data using pandas:
    - Capitalize names
    - Convert ages to integers
    - Filter out patients under 18
    - Remove duplicates

    Args:
        patients (list): List of patient dictionaries

    Returns:
        list: Cleaned list of patient dictionaries
    """
    # Convert list of dicts to DataFrame
    df = pd.DataFrame(patients)

    # BUG: No validation for required columns
    # FIX: Fill missing columns if necessary
    required_cols = ['name', 'age', 'gender', 'diagnosis']
    for col in required_cols:
        if col not in df.columns:
            df[col] = None

    # BUG: No capitalization of names
    # FIX: Capitalize each word in name
    df['name'] = df['name'].fillna('').apply(lambda x: x.title())

    # BUG: Age strings not always valid integers
    # FIX: Convert to numeric, invalid entries become NaN, then fill with 0
    df['age'] = pd.to_numeric(df['age'], errors='coerce').fillna(0).astype(int)

    # BUG: No age filtering
    # FIX: Filter out underage patients
    df = df[df['age'] >= 18]

    # Optional: Uncomment for step-through debugging
    # pdb.set_trace()

    # BUG: Duplicate entries not removed
    # FIX: Drop duplicate rows
    df = df.drop_duplicates()

    # Convert DataFrame back to list of dictionaries
    return df.to_dict(orient='records')

def main():
    """Main function to run the script."""
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to the data file
    data_path = os.path.join(script_dir, 'data', 'raw', 'patients.json')
    
    # Load the data
    patients = load_patient_data(data_path)

    # Clean the patient data
    cleaned_patients = clean_patient_data(patients)

    if not cleaned_patients:
        print("No valid patient records found.")
        return []

    # Print the cleaned patient data
    print("Cleaned Patient Data:")
    for patient in cleaned_patients:
        print(f"Name: {patient['name']}, Age: {patient['age']}, Gender: {patient['gender']}, Diagnosis: {patient['diagnosis']}")

    return cleaned_patients

if __name__ == "__main__":
    main()