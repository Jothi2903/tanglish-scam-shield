import sys
import joblib

model = joblib.load("models/baseline.joblib")
msg = " ".join(sys.argv[1:])
probs = model.predict_proba([msg])[0]
for label, p in zip(model.classes_, probs):
    print(f"{label}: {p:.2f}")