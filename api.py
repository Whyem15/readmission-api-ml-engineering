"""
Readmission Risk API

Serves a trained readmission-risk model as a REST endpoint, with input
validation that rejects malformed requests before they reach the model.

Run locally: uvicorn api:app --reload
Run in Docker: see Dockerfile / README.md
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import pandas as pd

app = FastAPI(title="Readmission Risk API")

model = joblib.load("readmission_model.pkl")
model_columns = joblib.load("model_columns.pkl")


class PatientInput(BaseModel):
    time_in_hospital: int = Field(ge=0, le=365)
    num_medications: int = Field(ge=0, le=100)
    num_lab_procedures: int = Field(ge=0, le=200)
    number_diagnoses: int = Field(ge=0, le=30)
    age: str


@app.post("/predict")
def predict(patient: PatientInput):
    row = pd.DataFrame([dict.fromkeys(model_columns, 0)])
    row["time_in_hospital"] = patient.time_in_hospital
    row["num_medications"] = patient.num_medications
    row["num_lab_procedures"] = patient.num_lab_procedures
    row["number_diagnoses"] = patient.number_diagnoses

    age_col = f"age_{patient.age}"
    if age_col in row.columns:
        row[age_col] = 1

    prob = model.predict_proba(row)[0][1]
    return {"readmission_risk": round(float(prob), 4)}
