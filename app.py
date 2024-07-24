from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import joblib
import numpy as np

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load your trained model and scaler
model = joblib.load("random_forest_model.pkl")
scaler = joblib.load("scaler.pkl")

# Dummy in-memory storage for users
users = {}

def predict_scam(features: dict) -> str:
    # Prepare the feature array
    feature_values = np.array([
        features.get('time', 0),
        features.get('amount', 0),
        features.get('V1', 0),
        features.get('V2', 0),
        features.get('V3', 0),
        features.get('V4', 0),
        features.get('V5', 0),
        features.get('V6', 0),
        features.get('V7', 0),
        features.get('V8', 0),
        features.get('V9', 0),
        features.get('V10', 0),
        features.get('V11', 0),
        features.get('V12', 0),
        features.get('V13', 0),
        features.get('V14', 0),
        features.get('V15', 0),
        features.get('V16', 0),
        features.get('V17', 0),
        features.get('V18', 0),
        features.get('V19', 0),
        features.get('V20', 0),
        features.get('V21', 0),
        features.get('V22', 0),
        features.get('V23', 0),
        features.get('V24', 0),
        features.get('V25', 0),
        features.get('V26', 0),
        features.get('V27', 0),
        features.get('V28', 0)
    ]).reshape(1, -1)
    
    # Scale the features
    scaled_features = scaler.transform(feature_values)
    
    # Predict using the model
    prediction = model.predict(scaled_features)[0]
    return "Scam" if prediction == 1 else "Not a Scam"

@app.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup", response_class=HTMLResponse)
async def signup_post(request: Request, username: str = Form(...), password: str = Form(...), confirm_password: str = Form(...), email: str = Form(...)):
    if username in users:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Username already exists"})
    if password != confirm_password:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Passwords do not match"})
    users[username] = {"password": password, "email": email}
    return templates.TemplateResponse("login.html", {"request": request, "message": "Signup successful! Please login."})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    user = users.get(username)
    if user is None or user['password'] != password:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    return templates.TemplateResponse("predict.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request,
                   time: float = Form(...),
                   amount: float = Form(...),
                   V1: float = Form(...),
                   V2: float = Form(...),
                   V3: float = Form(...),
                   V4: float = Form(...),
                   V5: float = Form(...),
                   V6: float = Form(...),
                   V7: float = Form(...),
                   V8: float = Form(...),
                   V9: float = Form(...),
                   V10: float = Form(...),
                   V11: float = Form(...),
                   V12: float = Form(...),
                   V13: float = Form(...),
                   V14: float = Form(...),
                   V15: float = Form(...),
                   V16: float = Form(...),
                   V17: float = Form(...),
                   V18: float = Form(...),
                   V19: float = Form(...),
                   V20: float = Form(...),
                   V21: float = Form(...),
                   V22: float = Form(...),
                   V23: float = Form(...),
                   V24: float = Form(...),
                   V25: float = Form(...),
                   V26: float = Form(...),
                   V27: float = Form(...),
                   V28: float = Form(...)):
    features = {
        'time': time,
        'amount': amount,
        'V1': V1,
        'V2': V2,
        'V3': V3,
        'V4': V4,
        'V5': V5,
        'V6': V6,
        'V7': V7,
        'V8': V8,
        'V9': V9,
        'V10': V10,
        'V11': V11,
        'V12': V12,
        'V13': V13,
        'V14': V14,
        'V15': V15,
        'V16': V16,
        'V17': V17,
        'V18': V18,
        'V19': V19,
        'V20': V20,
        'V21': V21,
        'V22': V22,
        'V23': V23,
        'V24': V24,
        'V25': V25,
        'V26': V26,
        'V27': V27,
        'V28': V28
    }
    result = predict_scam(features)
    return templates.TemplateResponse("predict.html", {"request": request, "result": result})
