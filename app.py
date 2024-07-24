from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Dummy in-memory storage for users and predictions
users = {}

# Dummy prediction logic for demonstration purposes
def predict_scam(features: dict) -> str:
    credit_score = features.get('credit_score', 0)
    amount = features.get('amount', 0)
    # Implement your prediction logic here
    return "Scam" if amount > 1000 or credit_score < 500 else "Not a Scam"

@app.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup", response_class=HTMLResponse)
async def signup_post(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
    if password != confirm_password:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Passwords do not match"})
    if username in users:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Username already exists"})
    users[username] = {"password": password, "email": email}
    return templates.TemplateResponse("login.html", {"request": request, "message": "Signup successful! Please login."})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    user = users.get(username)
    if not user or user["password"] != password:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    return templates.TemplateResponse("predict.html", {"request": request})

@app.get("/predict", response_class=HTMLResponse)
async def predict(request: Request):
    return templates.TemplateResponse("predict.html", {"request": request, "result": None})

@app.post("/predict", response_class=HTMLResponse)
async def predict_post(request: Request, credit_score: int = Form(...), amount: float = Form(...)):
    result = predict_scam({"credit_score": credit_score, "amount": amount})
    return templates.TemplateResponse("predict.html", {"request": request, "result": result})
