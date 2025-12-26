from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import pickle

from api.database import SessionLocal, engine
from api.models import Base, User, Prediction
from api.schemas import Register, Login, WeatherInput
from api.auth import hash_password, verify_password

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Load ML model
with open("model/weather_model.pkl", "rb") as f:
    model = pickle.load(f)

# --- Pages ---
@app.get("/")
def home():
    return FileResponse("frontend/index.html")

@app.get("/register")
def register_page():
    return FileResponse("frontend/register.html")

@app.get("/dashboard")
def dashboard_page():
    return FileResponse("frontend/dashboard.html")

# --- Auth ---
@app.post("/register")
def register(user: Register, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(400, "User already exists")
    new_user = User(
        username=user.username,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    return {"message": "Registered successfully"}

@app.post("/login")
def login(user: Login, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(401, "Invalid credentials")
    return {"message": "Login successful", "username": db_user.username}

# --- Prediction ---
@app.post("/predict")
def predict(data: WeatherInput, username: str, db: Session = Depends(get_db)):
    # Make prediction
    result = model.predict([[data.temp, data.humidity, data.wind]])[0]

    # Save prediction in DB
    record = Prediction(
        username=username,
        temp=data.temp,
        humidity=data.humidity,
        wind=data.wind,
        result=float(result)
    )
    db.add(record)
    db.commit()

    return {"predicted_temperature": float(result)}

