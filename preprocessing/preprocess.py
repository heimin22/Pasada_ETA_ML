# import necessary libraries and modules
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from pathlib import Path
import joblib
import json

def load_processed_data():
    # load processed data from data/processed/processed_data.json
    data_path = Path(__file__).parent.parent / 'data' / 'processed' / 'processed_data.json'
    return pd.read_json(data_path)

def split_features_target(df, target_col='eta'):
    # split features and target column from the dataframe
    x = df.drop(target_col, axis=1)
    y = df[target_col]
    return x, y

def scale_features(X, scaler_type='standard'):
    # scale features using the specified scaler type (standard or minmax) and save the scaler to a file
    if scaler_type == 'standard':
        scaler = StandardScaler()
    elif scaler_type == 'minmax':
        scaler = MinMaxScaler()
    else:
        raise ValueError(f"Invalid scaler type: {scaler_type}")
    
    x_scaled = scaler.fit_transform(X)
    x_scaled = pd.DataFrame(x_scaled, columns=X.columns)

    # save the scaler to a file
    scaler_path = Path(__file__).parent.parent / 'models' / f'{scaler_type}_scaler.pkl'
    joblib.dump(scaler, scaler_path)

    return x_scaled

def split_data(X, y, test_size=0.2, val_size=0.2, random_state=42):
    # split data into train, validation, and test sets with specified sizes and random state, and return the splits as dataframes
    X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    # adjust validation size based on test size
    val_size_adjusted = val_size / (1 - test_size)
    X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=val_size_adjusted, random_state=random_state)

    return X_train, X_val, X_test, y_train, y_val, y_test

def save_splits(x_train, x_val, x_test, y_train, y_val, y_test):
    # save the splits to a file
    output_dir = Path(__file__).parent.parent / 'data' / 'splits'
    output_dir.mkdir(exist_ok=True)

    # save features 
    x_train.to_json(output_dir / 'x_train.json', orient='records')
    x_val.to_json(output_dir / 'x_val.json', orient='records')
    x_test.to_json(output_dir / 'x_test.json', orient='records')

    # save target values
    # convert series to dataframe for consistent JSON format
    pd.DataFrame(y_train).to_json(output_dir / 'y_train.json', orient='records')
    pd.DataFrame(y_val).to_json(output_dir / 'y_val.json', orient='records')
    pd.DataFrame(y_test).to_json(output_dir / 'y_test.json', orient='records')

    print("Splits saved successfully.")

def preprocess_data(scaler_type='standard', test_size=0.2, val_size=0.2, random_state=42):
    # load processed data
    df = load_processed_data()
    print("Loaded processed data.")

    # split features and target
    x, y = split_features_target(df)
    print("Split features and target.")

    # scale features
    x_scaled = scale_features(x, scaler_type)
    print("Scaled features.")

    # split data into train, validation, and test sets
    x_train, x_val, x_test, y_train, y_val, y_test = split_data(x_scaled, y, test_size, val_size, random_state)
    print("Split data into train, validation, and test sets.")

    # save splits
    save_splits(x_train, x_val, x_test, y_train, y_val, y_test)
    print("Splits saved successfully.")

    return x_train, x_val, x_test, y_train, y_val, y_test

if __name__ == "__main__":
    preprocess_data()
    
    
    
