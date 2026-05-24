import pandas as pd
import joblib
import os

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

os.makedirs("models", exist_ok=True)

df = pd.read_csv("data/raw/telco.csv")

# Clean TotalCharges
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df.dropna(inplace=True)

# Select features
features = [
    "tenure",
    "MonthlyCharges",
    "TotalCharges"
]

X = df[features]

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# KMeans
kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

clusters = kmeans.fit_predict(X_scaled)

df["Cluster"] = clusters

# Save
joblib.dump(kmeans, "models/segment_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")

df.to_csv("data/processed/segmented_customers.csv", index=False)

print("Segmentation completed successfully!")