import pandas as pd
from pathlib import Path

def load_raw_data():
    data_dir = Path(__file__).parent.parent / 'data' / 'raw'
    return pd.read_csv(data_dir / 'eta_data.csv')

def clean_data(df):
    # TODO: dito dapat yung data cleaning logic ko sa susunod
    df = df.dropna()
    return df

