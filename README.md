# Readmission Risk API — ML Engineering Project

A production-style deployment of a machine learning model: a validated REST
API, containerized with Docker, backed by automated tests.

This project is the engineering counterpart to
[readmission-risk-prediction](../readmission-risk-prediction) (the modeling
project). That project answers "can this problem be predicted?" — this one
answers "can the model be served reliably to other systems?" They're
deliberately kept separate, because those are two different skills.

## What this demonstrates

- Wrapping a trained scikit-learn model in a REST API (FastAPI)
- Input validation that rejects malformed requests before they reach the
  model, rather than crashing or silently returning bad predictions
- Containerizing the service with Docker so it runs identically on any
  machine, not just the one it was built on
- Automated tests proving the validation behavior, not just manually
  checked once

## Architecture

```
Client request (JSON)
      │
      ▼
Pydantic validation (api.py)  ──reject──▶  422 error, model never touched
      │ (valid)
      ▼
Loaded model (readmission_model.pkl)
      │
      ▼
JSON response: { "readmission_risk": 0.xxxx }
```

## Repo structure

```
├── README.md
├── requirements.txt
├── Dockerfile
├── api.py                   # FastAPI service
├── test_api.py               # automated tests
├── readmission_model.pkl     # trained model (from the modeling project)
└── model_columns.pkl         # expected input column structure
```

## Running locally (without Docker)

```bash
pip install -r requirements.txt
uvicorn api:app --reload
```

Visit `http://127.0.0.1:8000/docs` for interactive API documentation.

## Running with Docker

```bash
docker build -t readmission-api .
docker run -p 8000:8000 readmission-api
```

Same `/docs` URL, now running inside an isolated, portable container.

## Example request

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "time_in_hospital": 5,
    "num_medications": 10,
    "num_lab_procedures": 40,
    "number_diagnoses": 6,
    "age": "[50-60)"
  }'
```

Response:
```json
{ "readmission_risk": 0.3421 }
```

An invalid request (e.g. `"time_in_hospital": -5`) returns a `422` error
instead of a prediction — the API fails safely rather than returning a
result computed from nonsensical input.

## Running the tests

```bash
pip install pytest httpx
pytest test_api.py -v
```

Two tests:
- a valid request returns a prediction
- an invalid request is rejected with a `422` status, confirming the
  validation layer works automatically rather than relying on manual
  checking

## Limitations & next steps

This is a portfolio-scale deployment, not a production clinical system.
A real deployment would additionally need:

- Authentication/authorization on the endpoint
- Request logging and monitoring (e.g. tracking prediction drift over time)
- A model versioning strategy (what happens when the model is retrained?)
- Load testing beyond a single local container
- HTTPS termination and a reverse proxy (e.g. nginx) in front of the API

## Author

Abdul-Hakeem Adeoye Adediran, medical doctor and Machine learning engineer building the engineering skills to deploy models reliably, not just build them.
