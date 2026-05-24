import streamlit as st
import requests


def show_churn_prediction():
    st.header("Live Churn Prediction")

    gender = st.selectbox("Gender", ["Female", "Male"])
    senior = st.selectbox("Senior Citizen", [0, 1])
    partner = st.selectbox("Partner", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["Yes", "No"])
    tenure = st.slider("Tenure Months", 0, 72, 12)

    phone_service = st.selectbox("Phone Service", ["Yes", "No"])
    internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    paperless = st.selectbox("Paperless Billing", ["Yes", "No"])

    payment = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )

    monthly = st.number_input("Monthly Charges", 0.0, 200.0, 70.0)
    total = st.number_input("Total Charges", 0.0, 10000.0, 1000.0)

    if st.button("Predict Churn", key="predict_churn_btn"):
        try:
            response = requests.post(
                "https://nexusiq-api.onrender.com/",
                json={
                    "SeniorCitizen": senior,
                    "tenure": tenure,
                    "MonthlyCharges": monthly,
                    "TotalCharges": total,
                    "gender_Male": 1 if gender == "Male" else 0,
                    "Partner_Yes": 1 if partner == "Yes" else 0,
                    "Dependents_Yes": 1 if dependents == "Yes" else 0,
                    "PhoneService_Yes": 1 if phone_service == "Yes" else 0,
                    "InternetService_Fiber_optic": 1 if internet_service == "Fiber optic" else 0,
                    "InternetService_No": 1 if internet_service == "No" else 0,
                    "Contract_One_year": 1 if contract == "One year" else 0,
                    "Contract_Two_year": 1 if contract == "Two year" else 0,
                    "PaperlessBilling_Yes": 1 if paperless == "Yes" else 0,
                    "PaymentMethod_Electronic_check": 1 if payment == "Electronic check" else 0,
                    "PaymentMethod_Mailed_check": 1 if payment == "Mailed check" else 0
                },
                timeout=5
            )

            result = response.json()

            prediction = result["churn_prediction"]
            probability = result["churn_probability"]

            st.info("Prediction served from FastAPI backend")
            st.subheader("Prediction Result")

            if prediction == 1:
                st.error(f"High Churn Risk: {probability * 100:.2f}%")
                st.write(
                    "Recommended action: Offer discount, assign retention agent, "
                    "and suggest long-term contract."
                )
            else:
                st.success(f"Low Churn Risk: {probability * 100:.2f}%")
                st.write(
                    "Recommended action: Maintain relationship and suggest suitable upgrade."
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "FastAPI backend is not running. Start it using: "
                "python -m uvicorn api.main:app --reload"
            )

        except Exception as e:
            st.error(f"Something went wrong: {e}")
