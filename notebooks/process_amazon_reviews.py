import bz2
import pandas as pd
import os

os.makedirs("data/processed", exist_ok=True)

file_path = "data/raw/train.ft.txt.bz2"

reviews = []
sentiments = []

with bz2.open(file_path, "rt", encoding="utf-8", errors="ignore") as f:
    for i, line in enumerate(f):
        if i >= 20000:
            break

        line = line.strip()

        if line.startswith("__label__1"):
            sentiments.append("Negative")
            reviews.append(line.replace("__label__1 ", "", 1))

        elif line.startswith("__label__2"):
            sentiments.append("Positive")
            reviews.append(line.replace("__label__2 ", "", 1))

df = pd.DataFrame({
    "review": reviews,
    "sentiment": sentiments
})

df.to_csv("data/processed/amazon_reviews_processed.csv", index=False)

print(df.head())
print(df["sentiment"].value_counts())
print("Saved successfully!")