import pandas as pd
from pathlib import Path
import numpy as np

def load_raw_data():
    data_dir = Path(__file__).parent.parent / 'data' / 'raw'
    return pd.read_csv(data_dir / 'eta_data.csv')

def clean_data(df):
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
    df = df.copy()

    # TODO: dito dapat yung feature engineering logic ko sa susunod
    # time-based features
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.day
    df['month'] = pd.to_datetime(df['timestamp']).dt.month
    df['is_weekend'] = pd.to_datetime(df['day_of_week']).isin([5, 6]).astype(int)

    # time periods
    df['is_rush_hour'] = (
        ((df['hour'] >= 7) & (df['hour'] <= 9)) |  # Morning rush
        ((df['hour'] >= 16) & (df['hour'] <= 19))   # Evening rush
    ).astype(int)

    # time categories
    df['time_of_day'] = pd.cut(
        df['hour'],
        bins=[0, 6, 12, 18, 24],
        labels=['night', 'morning', 'afternoon', 'evening']
    )

    # convert categorial to dummy variables
    df = pd.get_dummies(df, columns=['time_of_day'], prefix='tod')

    #drop original timestamp column
    df = df.drop('timestamp', axis=1)

    # weather features
    df['weather_condition'] = df['weather'].apply(lambda x: x.split(',')[0] if isinstance(x, str) else 'unknown')
    df['weather_condition'] = df['weather_condition'].str.lower()

    # weather conditions
    df['is_rainy'] = df['weather_condition'].str.contains('rain|drizzle|shower', na=False).astype(int)
    df['is_cloudy'] = df['weather_condition'].str.contains('cloud|overcast|fog|mist', na=False).astype(int)
    df['is_sunny'] = df['weather_condition'].str.contains('sun|clear|cast', na=False).astype(int)
    
    # drop original weather column
    df = df.drop(['weather', 'weather_condition'], axis=1)

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
