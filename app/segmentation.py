import streamlit as st
import pandas as pd
import plotly.express as px

def show_segmentation():

    st.header("Customer Segmentation")

    df = pd.read_csv("data/processed/segmented_customers.csv")

    fig = px.scatter(
        df,
        x="MonthlyCharges",
        y="TotalCharges",
        color=df["Cluster"].astype(str),
        hover_data=["tenure"],
        title="Customer Segments"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Cluster Summary")

    summary = df.groupby("Cluster")[
        ["tenure", "MonthlyCharges", "TotalCharges"]
    ].mean()

    st.dataframe(summary)