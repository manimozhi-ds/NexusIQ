from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI(title="Customer Intelligence API")

model = joblib.load("models/churn_model.pkl")
model_columns = joblib.load("models/churn_columns.pkl")

class CustomerInput(BaseModel):
    SeniorCitizen: int
    tenure: int
    MonthlyCharges: float
    TotalCharges: float
    gender_Male: int = 0
    Partner_Yes: int = 0
    Dependents_Yes: int = 0
    PhoneService_Yes: int = 1
    InternetService_Fiber_optic: int = 0
    InternetService_No: int = 0
    Contract_One_year: int = 0
    Contract_Two_year: int = 0
    PaperlessBilling_Yes: int = 0
    PaymentMethod_Electronic_check: int = 0
    PaymentMethod_Mailed_check: int = 0

@app.get("/")
def home():
    return {"message": "AI-Powered Customer Intelligence API is running"}

@app.post("/predict-churn")
def predict_churn(data: CustomerInput):
    input_dict = data.dict()

    # Match model column names exactly
    input_dict = {
        key.replace("_Fiber_optic", "_Fiber optic")
           .replace("_One_year", "_One year")
           .replace("_Two_year", "_Two year")
           .replace("_Electronic_check", "_Electronic check")
           .replace("_Mailed_check", "_Mailed check"): value
        for key, value in input_dict.items()
    }

    final_input = pd.DataFrame(columns=model_columns)
    final_input.loc[0] = 0

    for col, value in input_dict.items():
        if col in final_input.columns:
            final_input.loc[0, col] = value

    probability = model.predict_proba(final_input)[0][1]
    prediction = int(model.predict(final_input)[0])

    return {
        "churn_prediction": prediction,
        "churn_probability": round(probability, 4),
        "risk_level": "High" if probability >= 0.5 else "Low"
    }