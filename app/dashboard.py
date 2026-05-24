import streamlit as st
import pandas as pd
import plotly.express as px

from churn import show_churn_prediction
from segmentation import show_segmentation
from sentiment import show_sentiment
from explainability import show_explainability
from ticket_classifier import show_ticket_classifier

st.set_page_config(
    page_title="NexusIQ",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("NexusIQ Suite")
st.sidebar.markdown("Customer analytics, churn prediction, NLP insights, and explainable AI.")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Choose Module",
    [
        "Overview",
        "Churn Analytics",
        "Customer Segments",
        "Review Intelligence",
        "Model Insights",
        "Support Intelligence"
    ],
    key="main_navigation"
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Enterprise AI platform built using Streamlit, FastAPI, Transformers, SHAP, Plotly, and Docker."
)

if page == "Churn Analytics":
    show_churn_prediction()
    st.stop()

elif page == "Customer Segments":
    show_segmentation()
    st.stop()

elif page == "Review Intelligence":
    show_sentiment()
    st.stop()

elif page == "Model Insights":
    show_explainability()
    st.stop()

elif page == "Support Intelligence":
    show_ticket_classifier()
    st.stop()

st.title("NexusIQ")
st.caption("AI-driven customer intelligence for retention, support analytics, and business insights")

df = pd.read_csv("data/raw/telco.csv")

total_customers = len(df)
churned = df[df["Churn"] == "Yes"].shape[0]
active_customers = df[df["Churn"] == "No"].shape[0]
churn_rate = round((churned / total_customers) * 100, 2)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", total_customers)
col2.metric("Active Customers", active_customers)
col3.metric("Churned Customers", churned)
col4.metric("Churn Rate", f"{churn_rate}%")

st.divider()

st.subheader("Customer Retention Analytics")

fig = px.histogram(
    df,
    x="Churn",
    color="Churn",
    text_auto=True,
    title="Customer Churn Distribution"
)
st.plotly_chart(fig, use_container_width=True)

col_left, col_right = st.columns(2)

with col_left:
    fig2 = px.histogram(
        df,
        x="Contract",
        color="Churn",
        barmode="group",
        title="Contract Type vs Churn"
    )
    st.plotly_chart(fig2, use_container_width=True)

with col_right:
    fig3 = px.box(
        df,
        x="Churn",
        y="MonthlyCharges",
        color="Churn",
        title="Monthly Charges Distribution"
    )
    st.plotly_chart(fig3, use_container_width=True)

st.subheader(" Key Business Insight")
st.info(
    "Customers with month-to-month contracts and higher monthly charges show stronger churn behavior. "
    "This insight supports targeted retention campaigns and personalized offers."
)