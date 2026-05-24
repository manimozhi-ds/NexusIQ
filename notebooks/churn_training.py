import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score
from sklearn.ensemble import RandomForestClassifier

os.makedirs("models", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

df = pd.read_csv("data/raw/telco.csv")

print("Shape:", df.shape)
print(df.head())
print(df.info())

# Clean TotalCharges
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df.dropna(inplace=True)

# Drop ID
df.drop("customerID", axis=1, inplace=True)

# Target encoding
df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

# One-hot encoding
df_encoded = pd.get_dummies(df, drop_first=True)

X = df_encoded.drop("Churn", axis=1)
y = df_encoded["Churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

pred = model.predict(X_test)
proba = model.predict_proba(X_test)[:, 1]

print("\nAccuracy:", accuracy_score(y_test, pred))
print("ROC-AUC:", roc_auc_score(y_test, proba))
print("\nClassification Report:\n", classification_report(y_test, pred))

# Save files
joblib.dump(model, "models/churn_model.pkl")
joblib.dump(X.columns.tolist(), "models/churn_columns.pkl")

df_encoded.to_csv("data/processed/telco_processed.csv", index=False)

print("\nModel saved successfully!")