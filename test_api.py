"""
Automated tests for the Readmission Risk API.

Run: pytest test_api.py -v
"""

from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_valid_input_returns_prediction():
    response = client.post("/predict", json={
        "time_in_hospital": 5,
        "num_medications": 10,
        "num_lab_procedures": 40,
        "number_diagnoses": 6,
        "age": "[50-60)"
    })
    assert response.status_code == 200
    assert "readmission_risk" in response.json()


def test_invalid_input_rejected_safely():
    response = client.post("/predict", json={
        "time_in_hospital": -5,
        "num_medications": 10,
        "num_lab_procedures": 40,
        "number_diagnoses": 6,
        "age": "[50-60)"
    })
    assert response.status_code == 422
