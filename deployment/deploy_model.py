from flask import Flask, request, jsonify
import joblib
from pathlib import Path

app = Flask(__name__)

# load na agad yung model on startup
model_path = Path(__file__)