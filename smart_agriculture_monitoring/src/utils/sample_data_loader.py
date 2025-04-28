import pandas as pd

def load_data(uploaded_file):
    """
    Load a CSV or Excel file into a pandas DataFrame.

    Parameters:
    - uploaded_file: Uploaded file object (Streamlit file_uploader)

    Returns:
    - pd.DataFrame or None
    """
    try:
        if uploaded_file.name.lower().endswith('.csv'):
            df = pd.read_csv(uploaded_file)  # supports chunking and various delimiters :contentReference[oaicite:6]{index=6}
        elif uploaded_file.name.lower().endswith(('.xls', '.xlsx')):
            df = pd.read_excel(uploaded_file)  # supports xls, xlsx, xlsm, odf, ods :contentReference[oaicite:7]{index=7}
        else:
            raise ValueError("Unsupported file type: must be .csv, .xls, or .xlsx")
        return df
    except Exception as e:
        print(f"[data_loader] Error loading file: {e}")
        return None

def check_missing_values(df):
    """
    Return a Series with count of missing values per column.

    Parameters:
    - df: pd.DataFrame

    Returns:
    - pd.Series
    """
    return df.isna().sum()

def get_basic_stats(df):
    """
    Return basic EDA outputs: head(), info(), and describe().

    Parameters:
    - df: pd.DataFrame

    Returns:
    - dict with keys: head, info, describe
    """
    stats = {}
    stats['head'] = df.head()
    stats['describe'] = df.describe()

    from io import StringIO
    buffer = StringIO()
    df.info(buf=buffer)
    stats['info'] = buffer.getvalue()
    return stats
