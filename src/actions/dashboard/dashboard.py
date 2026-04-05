import streamlit as st
import pandas as pd
from textblob import TextBlob

# Title
st.title("📊 Feedback Intelligence System")

# Load data
df = pd.read_csv("data/sample_feedback.csv")

# Sentiment function
def sentiment_analyzer(text):
    polarity = TextBlob(str(text)).sentiment.polarity
    confidence = round(abs(polarity) * 100, 2)

    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return pd.Series([sentiment, confidence])"

# Category function
def categorizing(text):
    text = text.lower()
    if "crash" in text or "error" in text:
        return "Bug"
    elif "slow" in text or "lag" in text:
        return "Performance"
    elif "add" in text:
        return "Feature Request"
    else:
        return "General"

# Apply analysis
df[["Sentiment", "Confidence"]] = df["message"].apply(sentiment_analyzer)
df["Category"] = df["message"].apply(categorizing)

# Metrics
st.subheader("📌 Summary")
col1, col2, col3 = st.columns(3)

col1.metric("Total Feedback", len(df))
col2.metric("Positive", (df["Sentiment"] == "Positive").sum())
col3.metric("Negative", (df["Sentiment"] == "Negative").sum())

# Filter
st.subheader("🔍 Filter Feedback")
sentiment_filter = st.selectbox("Select Sentiment", ["All", "Positive", "Negative", "Neutral"])

if sentiment_filter != "All":
    df = df[df["Sentiment"] == sentiment_filter]

# Charts
st.subheader("📊 Sentiment Distribution")
st.bar_chart(df["Sentiment"].value_counts())

st.subheader("📊 Issue Categories")
st.bar_chart(df["Category"].value_counts())

# Data table
st.subheader("📄 Feedback Data")
st.dataframe(df)