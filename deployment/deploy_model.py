from flask import Flask, request, jsonify
import joblib
from pathlib import Path

app = Flask(__name__)

# load na agad yung model on startup
model_path = Path(__file__) / 'models' / 'eta_model.pkl'
model = joblib.load(model_path)

@app.route('/predict_eta', methods=['POST'])
def predict_eta():
    data = request.get_json()
    prediction = model.predict([data['features']])
    return jsonify({'eta_prediction': prediction[0]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)