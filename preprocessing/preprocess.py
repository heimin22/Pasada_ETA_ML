import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from pathlib import Path
import joblib
import json

def load_processed_data():
    data_path = Path(__file__).parent.parent / 'data' / 'processed' / 'processed_data.json'
    return pd.read_json(data_path)

def split_features_target(df, target_col='eta'):
    x = df.drop(target_col, axis=1)
    y = df[target_col]
    return x, y

def scale_features(X, scaler_type='standard'):
    if scaler_type == 'standard':
        scaler = StandardScaler()
    elif scaler_type == 'minmax':
        scaler = MinMaxScaler()
    else:
        raise ValueError(f"Invalid scaler type: {scaler_type}")
    
    x_scaled = scaler.fit_transform(X)
    x_scaled = pd.DataFrame(x_scaled, columns=X.columns)

    scaler_path = Path(__file__).parent.parent / 'models' / f'{scaler_type}_scaler.pkl'
    joblib.dump(scaler, scaler_path)

    return x_scaled

def split_data(X, y, test_size=0.2, val_size=0.2, random_state=42):
    X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    val_size_adjusted = val_size / (1 - test_size)
    X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=val_size_adjusted, random_state=random_state)

    return X_train, X_val, X_test, y_train, y_val, y_test


