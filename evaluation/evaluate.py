import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error
from pathlib import Path

def evaluate_model():
    model_path = Path(__file__).parent.parent / 'models' / 'eta_model.pkl'
    data_path = Path(__file__).parent.parent / 'data' / 'processed' / 'processed_data.csv'

    model = joblib.load(model_path)
    df = pd.read_csv(data_path)

    x = df.drop('eta', axis = 1)
    y = df['eta']

    predictions = model.predict(x)

    mae = mean_absolute_error(y, predictions)
    rmse = mean_squared_error(y, predictions, squared=False)

    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")

if __name__ == '__main__':
    print('Evaluating model...')
    evaluate_model()
