import sys
import joblib
from explain import explain

model = joblib.load("models/baseline.joblib")

args = sys.argv[1:]
use_tamil = "--ta" in args
msg = " ".join(a for a in args if a != "--ta")

probs = model.predict_proba([msg])[0]
best = probs.argmax()
label = model.classes_[best]
icon = {"scam": "SCAM", "suspicious": "SUSPICIOUS", "safe": "SAFE"}[label]

print(f"\nResult: {icon} ({probs[best]:.2f})")
for lab, p in zip(model.classes_, probs):
    print(f"  {lab}: {p:.2f}")

reasons, advice = explain(msg, label)
i = 1 if use_tamil else 0

if reasons:
    print("\nYen?")
    for r in reasons:
        print(f"  - {r[i]}")
print(f"\nAdvice: {advice[i]}\n")