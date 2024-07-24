from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from typing import List, Dict
from sklearn.metrics import classification_report, confusion_matrix

app = FastAPI()

# Load the saved model and scaler
model = joblib.load('random_forest_model.pkl')
scaler = joblib.load('scaler.pkl')

class Transaction(BaseModel):
    features: List[float]

class Transactions(BaseModel):
    transactions: List[Transaction]
    true_labels: List[int]

@app.post("/predict")
def predict(transaction: Transaction):
    try:
        # Convert the input data to a numpy array and reshape it appropriately
        input_data = np.array(transaction.features).reshape(1, -1)
        
        # Scale the input data
        input_data = scaler.transform(input_data)
        
        # Make prediction
        prediction = model.predict(input_data)
        probability = model.predict_proba(input_data)[0][1]  # Assuming binary classification
        
        return {"is_fraud": bool(prediction[0]), "probability": float(probability)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/evaluate")
def evaluate(transactions: Transactions):
    try:
        # Extract features and true labels
        features = [t.features for t in transactions.transactions]
        true_labels = transactions.true_labels

        # Convert to numpy arrays
        features = np.array(features)
        true_labels = np.array(true_labels)

        # Scale the input data
        features = scaler.transform(features)

        # Make predictions
        predictions = model.predict(features)
        probabilities = model.predict_proba(features)[:, 1]  # Assuming binary classification

        # Calculate evaluation metrics
        report = classification_report(true_labels, predictions, output_dict=True)
        conf_matrix = confusion_matrix(true_labels, predictions).tolist()

        return {"classification_report": report, "confusion_matrix": conf_matrix}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
