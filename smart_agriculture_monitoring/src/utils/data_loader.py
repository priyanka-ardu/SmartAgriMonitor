import pandas as pd

def load_data(file):
    """Load CSV or Excel data into a DataFrame."""
    try:
        if file.type == "application/vnd.ms-excel" or file.name.endswith(".xlsx"):
            return pd.read_excel(file)
        elif file.type == "text/csv" or file.name.endswith(".csv"):
            return pd.read_csv(file)
        else:
            raise ValueError("Unsupported file type. Please upload a CSV or Excel file.")
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def get_basic_stats(df):
    """Get basic statistics for a DataFrame."""
    return df.describe()

def check_missing_values(df):
    """Check for missing values in the DataFrame."""
    return df.isnull().sum()

def clean_data(df):
    """Clean the dataset by handling missing values and other preprocessing tasks."""
    # Example: Drop rows with missing values (you can modify as needed)
    return df.dropna()
