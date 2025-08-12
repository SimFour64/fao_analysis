import pandas as pd
from .config import RAW_DIR, PROCESSED_DIR, SOURCES, COLUMNS

def load_one_csv(sourcename, processed=False):
    """
    Loads one csv FAO data file based on the sourcename. If processed=True,
    it returns the csv file that has been cleaned. If False, it loads the raw
    dataset

    Args:
        - sourcename (str): name of the source to be loaded
        - processed (bool, opt): indicates if returns the raw or processed csv

    Returns:
        - csv_file (pd.Dataframe): dataframe containing data (raw or processed)
    """
    if processed:
        path = PROCESSED_DIR / f"{sourcename}_processed.csv"
    else:
        path = RAW_DIR / f"{sourcename}.csv"

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    return pd.read_csv(path)

def load_raw():
    """
    Load the required csv files in SOURCES and stores them in pandas DataFrames,
    returns a python dict with csv names as keys and dataframes as values

    Args:
        - None

    Returns:
        - dict_df (dictionnary of pd.Dataframes): dataframes froms csv raw data
    """

    dict_df = {}

    for sourcename in SOURCES:
        try:
            dict_df[sourcename] = load_one_csv(sourcename, processed=False)
            print(f"✅ {sourcename} loaded.")
        except FileNotFoundError as e:
            print(f"Error, file not found ({sourcename}) → {e}")
            raise

    return dict_df


def clean_data(dict_df):
    """
    Returns clean datasets that are passed as dictionnary

    Args:
        - dict_df (dict of pd.Dataframe): dataframes to clean

    Returns:
        - clean_df (dict of pd.Dataframe): clean dataframes
    """
    clean_df = {key: df[COLUMNS[key]] for key, df in dict_df.items()}

    print("✅ Data processed")

    return clean_df

def save_processed(clean_df):
    """
    Save processed datasets in data processed directory

    Args:
        - clean_df (dict of pd.Dataframe): clean dataframes to save

    Returns:
        - None
    """
    for key, df in clean_df.items():
        df.to_csv(PROCESSED_DIR / f"{key}_processed.csv", index=False, encoding="utf-8")
        print(f"✅ {key} processed saved.")


def load_processed(strategy="keep"):
    """
    Load processed CSV files, generating them from raw data if missing.

    Applies a missing-value strategy to each DataFrame:
      - "keep": leave NaN as-is
      - "zero": replace NaN with 0
      - "drop": remove rows with NaN

    Args:
        - strategy : str, default="keep". Missing-value handling method.

    Returns:
        - dict[str, pandas.DataFrame] : processed DataFrames keyed by source name.
    """
    # Process csv files if not done already
    missing_files = [sourcename for sourcename in SOURCES if not (PROCESSED_DIR / f"{sourcename}_processed.csv").exists()]
    if missing_files:
        print("🟠 Missing files → processing raw data.")
        dict_df = load_raw()
        clean_df = clean_data(dict_df)
        save_processed(clean_df)
    else:
        try:
            clean_df = {sourcename: load_one_csv(sourcename, processed=True) for sourcename in SOURCES}
            print("✅ Loaded processed data from disk")
        except FileNotFoundError as e:
            print(f"Error, file not found - {e}")
            raise

    # Applying strategy
    strategies = {
        "keep": lambda df: df,
        "zero": lambda df: df.fillna(0),
        "drop": lambda df: df.dropna()
    }
    if strategy not in strategies:
        raise ValueError(f"Unkown strategy {strategy}, please chose from: {', '.join(strategies)}")

    clean_df = {key: strategies[strategy](df) for key, df in clean_df.items()}

    return clean_df
