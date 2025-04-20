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


    
