import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report, confusion_matrix

manual = pd.read_csv("data/raw/messages.csv", encoding="utf-8")
generated = pd.read_csv("data/raw/generated.csv", encoding="utf-8")

# Test = manual rows only. Generated rows go only into training.
train_manual, test = train_test_split(
    manual, test_size=0.3, random_state=42, stratify=manual["label"]
)
train = pd.concat([train_manual, generated], ignore_index=True)

model = make_pipeline(
    TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), lowercase=True),
    LogisticRegression(max_iter=1000, class_weight="balanced"),
)
model.fit(train["text"], train["label"])

pred = model.predict(test["text"])
print(classification_report(test["label"], pred, zero_division=0))

labels = ["scam", "suspicious", "safe"]
print("Confusion matrix (rows=actual, cols=predicted):", labels)
print(confusion_matrix(test["label"], pred, labels=labels))

os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/baseline.joblib")
print("Model saved to models/baseline.joblib")