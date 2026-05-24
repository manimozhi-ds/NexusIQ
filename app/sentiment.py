import streamlit as st
import pandas as pd
import plotly.express as px
#from textblob import TextBlob
from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def analyze_sentiment(text):

    result = classifier(text)[0]

    label = result["label"]
    score = result["score"]

    if label == "POSITIVE":
        return "Positive", score

    else:
        return "Negative", score


def detect_complaint_type(text):

    text = str(text).lower()

    if any(word in text for word in [
        "refund", "money", "price", "charged", "expensive"
    ]):
        return "Billing / Refund Issue"

    elif any(word in text for word in [
        "broken", "damage", "poor quality", "defective", "stopped"
    ]):
        return "Product Quality Issue"

    elif any(word in text for word in [
        "delivery", "shipping", "arrived", "late", "package"
    ]):
        return "Delivery Issue"

    elif any(word in text for word in [
        "support", "service", "response", "help"
    ]):
        return "Customer Support Issue"

    else:
        return "General Feedback"


def show_sentiment():

    st.header("Customer Review Analytics")

    df = pd.read_csv(
        "data/processed/amazon_reviews_processed.csv"
    )


    st.subheader("Live Customer Review Analysis")

    review = st.text_area(
        "Enter customer review",
        "The product stopped working after two days and support never responded."
    )

    if st.button("Analyze Review", key="analyze_review_btn"):

        sentiment, score = analyze_sentiment(review)

        complaint = detect_complaint_type(review)

        st.subheader("AI Review Intelligence Result")

        if sentiment == "Positive":
            st.success(f"Sentiment: {sentiment}")

        elif sentiment == "Negative":
            st.error(f"Sentiment: {sentiment}")

        else:
            st.warning(f"Sentiment: {sentiment}")

        st.write(f"**Sentiment Score:** {score:.3f}")

        st.write(f"**Complaint Type:** {complaint}")

        if sentiment == "Negative":
            st.error(
                "Business Action: Escalate customer issue and prioritize retention support."
            )

        elif sentiment == "Neutral":
            st.warning(
                "Business Action: Monitor customer experience and request more feedback."
            )

        else:
            st.success(
                "Business Action: Customer sentiment is positive. Recommend loyalty or upsell strategy."
            )

    st.divider()


    st.subheader("Amazon Customer Review Overview")

    col1, col2, col3 = st.columns(3)

    total = len(df)

    positive = df[df["sentiment"] == "Positive"].shape[0]

    negative = df[df["sentiment"] == "Negative"].shape[0]

    col1.metric("Total Reviews", total)

    col2.metric("Positive Reviews", positive)

    col3.metric("Negative Reviews", negative)


    fig = px.histogram(
        df,
        x="sentiment",
        color="sentiment",
        text_auto=True,
        title="Customer Review Sentiment Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)


    sample_df = df.sample(1000, random_state=42)

    sample_df["review_length"] = (
        sample_df["review"]
        .astype(str)
        .apply(len)
    )

    fig2 = px.box(
        sample_df,
        x="sentiment",
        y="review_length",
        color="sentiment",
        title="Review Length vs Sentiment"
    )

    st.plotly_chart(fig2, use_container_width=True)


    st.subheader("Sample Customer Reviews")

    st.dataframe(
        df.sample(10, random_state=42)
    )