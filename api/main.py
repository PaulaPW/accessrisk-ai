import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

MODEL_PATH = "models/accessrisk_model.pkl"

app = FastAPI(title="AccessRisk AI API")

model = joblib.load(MODEL_PATH)

class AccessEvent(BaseModel):
    country: str
    role: str
    app: str
    failed_logins: int
    mfa_failures: int
    new_device: int
    new_country: int
    impossible_travel: int
    after_hours: int
    privileged: int
    sensitive_app: int
    dormant_account: int
    contractor: int
    downloads: int

LABELS = {
    0: "Normal",
    1: "Suspicious",
    2: "High Risk"
}

@app.get("/")
def home():
    return {"message": "AccessRisk AI API is running"}

@app.post("/predict")
def predict(event: AccessEvent):
    event_df = pd.DataFrame([event.model_dump()])

    prediction = model.predict(event_df)[0]
    probabilities = model.predict_proba(event_df)[0]

    risk_level = LABELS[int(prediction)]
    confidence = round(float(max(probabilities)), 4)

    return {
        "risk_level": risk_level,
        "prediction": int(prediction),
        "confidence": confidence
    }
