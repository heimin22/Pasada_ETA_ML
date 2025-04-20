import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from pathlib import Path
import json

def evaluate_model():
    model_path = Path(__file__).parent.parent / 'models' / 'eta_model.pkl'
    data_path = Path(__file__).parent.parent / 'data' / 'processed' / 'processed_data.json'

    model = joblib.load(model_path)
    df = pd.read_json(data_path)

    x = df.drop('eta', axis = 1)
    y = df['eta']

    predictions = model.predict(x)
    
    # calculate metrics
    metrics = {
        'mae': mean_absolute_error(y, predictions),
        'rmse': mean_squared_error(y, predictions, squared=False),
        'r2': r2_score(y, predictions),
        'mse': mean_squared_error(y, predictions)
    }

    # save metrics to a json file
    metrics_path = Path(__file__).parent.parent / 'metrics' / 'metrics.json'
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=4)
        
    for metric, value in metrics.items():
        print(f"{metric.upper()}: {value:.2f}")

    return metrics

if __name__ == '__main__':
    print('Evaluating model...')
    evaluate_model()
