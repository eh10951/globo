from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
CORS(app) # Permitir llamadas desde Flutter Web/Desktop

# Configuración del modelo
MODEL_PATH = r'C:\Users\eh109\OneDrive\Escritorio\proyecto_agro_3d\modelo_vacas_completo.pkl'

try:
    data_bundle = joblib.load(MODEL_PATH)
    model = data_bundle['model']
    le = data_bundle['label_encoder']
    features = data_bundle['features']
    print("✅ IA: Modelo cargado correctamente para el Diagnosticador Manual.")
except Exception as e:
    print(f"❌ IA Error: {e}")
    model = None

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({"error": "Modelo no cargado"}), 500
    
    data = request.json
    # Los síntomas vienen del Flutter como una lista o dict
    # Ejemplo: {"Temperatura_Corporal": 40.5, "Tos_Sí": 1, ...}
    
    df = pd.DataFrame([data])
    
    # Asegurar todas las columnas
    for col in features:
        if col not in df.columns:
            df[col] = 0
            
    df = df[features]
    
    try:
        pred = model.predict(df)[0]
        prob = model.predict_proba(df)[0]
        
        label = le.inverse_transform([pred])[0]
        confidence = float(np.max(prob)) * 100
        
        return jsonify({
            "diagnosis": label,
            "confidence": confidence,
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # Ejecutar en el puerto 5000 para que Flutter pueda consultarlo
    app.run(host='0.0.0.0', port=5000)
