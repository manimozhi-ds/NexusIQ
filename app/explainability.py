import streamlit as st
import pandas as pd
import joblib
import shap
import plotly.express as px


def show_explainability():
    st.header("Model Explainability")
    st.caption("Interactive explanation of which features influence churn prediction most.")

    model = joblib.load("models/churn_model.pkl")
    columns = joblib.load("models/churn_columns.pkl")

    df = pd.read_csv("data/processed/telco_processed.csv")
    X = df[columns].sample(500, random_state=42)

    with st.spinner("Calculating SHAP values..."):
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X)

    if isinstance(shap_values, list):
        values = shap_values[1]
    elif len(shap_values.shape) == 3:
        values = shap_values[:, :, 1]
    else:
        values = shap_values

    importance = pd.DataFrame({
        "Feature": X.columns,
        "Mean SHAP Value": abs(values).mean(axis=0)
    }).sort_values("Mean SHAP Value", ascending=False)

    top_n = st.slider("Select number of top features", 5, 25, 15)

    top_features = importance.head(top_n)

    fig = px.bar(
        top_features.sort_values("Mean SHAP Value"),
        x="Mean SHAP Value",
        y="Feature",
        orientation="h",
        title="Interactive Global Feature Importance",
        text="Mean SHAP Value",
        hover_data={"Mean SHAP Value": ":.5f", "Feature": True}
    )

    fig.update_traces(texttemplate="%{text:.4f}", textposition="outside")
    fig.update_layout(height=600)

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top Feature Explanation Table")
    st.dataframe(top_features, use_container_width=True)

    st.subheader("Business Interpretation")

    most_important = top_features.iloc[0]["Feature"]

    st.info(
        f"The most influential churn driver in this model is **{most_important}**. "
        "Higher SHAP importance means the feature has a stronger average impact on churn predictions."
    )