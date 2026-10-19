import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from explain import explain

app = FastAPI(title="Tanglish Scam Shield")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("models/baseline.joblib")


class Message(BaseModel):
    text: str


@app.get("/")
def home():
    return {"status": "ok", "app": "Tanglish Scam Shield"}


@app.post("/predict")
def predict(msg: Message):
    probs = model.predict_proba([msg.text])[0]
    best = int(probs.argmax())
    label = str(model.classes_[best])
    reasons, advice = explain(msg.text, label)

    return {
        "label": label,
        "confidence": round(float(probs[best]), 2),
        "scores": {str(c): round(float(p), 2) for c, p in zip(model.classes_, probs)},
        "reasons_tanglish": [r[0] for r in reasons],
        "reasons_tamil": [r[1] for r in reasons],
        "advice_tanglish": advice[0],
        "advice_tamil": advice[1],
    }
