import json
from flask import Flask, request, jsonify
import joblib
from pathlib import Path
from gemini.gemini_eta import gemini_eta_predict # type: ignore
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

@app.route('/predict_eta_with_gemini', methods=['POST'])

def predict_eta_with_gemini():
    data = request.get_json()
    api_key = os.getenv("GEMINI_API_ML")
    
    if not api_key:
        return jsonify({"error": "API key not found"}), 400
    
    result = gemini_eta_predict(json.dumps(data ["features"]), api_key)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
