import pandas as pd
from pathlib import Path

def load_raw_data():
    data_dir = Path(__file__).parent.parent / 'data' / 'raw'
    return pd.read_csv(data_dir / 'eta_data.csv')

def clean_data(df):
    # TODO: dito dapat yung data cleaning logic ko sa susunod
    df = df.copy()
    df = df.drop_duplicates()
    df = df.dropna()

    # convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # remove outliers
    # using IQR method
    Q1 = df['eta'].quantile(0.25)
    Q3 = df['eta'].quantile(0.75)
    IQR = Q3 - Q1
    df = df[~((df['eta'] < (Q1 - 1.5 * IQR)) | (df['eta'] > (Q3 + 1.5 * IQR)))]
    df = df.reset_index(drop=True)
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