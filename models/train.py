import pandas as pd
from pathlib import Path

def load_raw_data():
    data_dir = Path(__file__).parent.parent / 'data' / 'raw'
    return pd.read_csv(data_dir / 'eta_data.csv')

def clean_data(df):
    # TODO: dito dapat yung data cleaning logic ko sa susunod
    df = df.dropna()
    return df

def engineer_features(df):
    # TODO: dito dapat yung feature engineering logic ko sa susunod
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    return df

def save_processed_data(df):
    output_path = Path(__file__).parent.parent / 'data' / 'processed' / 'processed_data.csv'
    df.to_csv(output_path, index=False)

if __name__ == '__main__':
    print("Preprocessing data ")
    raw_df = load_raw_data()
    cleaned_df = clean_data(raw_df)
    processed_df = engineer_features(cleaned_df)
    save_processed_data(processed_df)
    print("Data preprocessing completed!")