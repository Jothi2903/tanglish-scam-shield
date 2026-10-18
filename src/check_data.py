import pandas as pd

df = pd.read_csv("data/raw/messages.csv", encoding="utf-8")
print(df.shape)
print(df["label"].value_counts())