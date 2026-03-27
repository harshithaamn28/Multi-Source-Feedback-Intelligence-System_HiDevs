import streamlit as st
import pandas as pd
from textblob import TextBlob
import os

# -------------------------------
# PAGE CONFIG (important)
# -------------------------------
st.set_page_config(page_title="Feedback System", layout="wide")

# -------------------------------
# CUSTOM STYLING (COLORS)
# -------------------------------
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
        color: white;
    }
    h1 {
        color: #00ADB5;
        text-align: center;
    }
    .stMetric {
        background-color: #1f2937;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# TITLE
# -------------------------------
st.title("📊 Feedback Intelligence System")

# -------------------------------
# LOAD CSV
# -------------------------------
try:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "sample_feedback.csv")

    df = pd.read_csv(file_path)

except Exception as e:
    st.error("❌ Error loading CSV file")
    st.write(e)
    st.stop()

# -------------------------------
# CHECK COLUMN
# -------------------------------
if "message" not in df.columns:
    st.error("❌ CSV must contain 'message' column")
    st.stop()

# -------------------------------
# SENTIMENT FUNCTION
# -------------------------------
def sentiment_analyzer(text):
    polarity = TextBlob(str(text)).sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# -------------------------------
# CATEGORY FUNCTION
# -------------------------------
def categorizing(text):
    text = str(text).lower()
    if "crash" in text or "error" in text:
        return "Bug"
    elif "slow" in text or "lag" in text:
        return "Performance"
    elif "add" in text:
        return "Feature Request"
    else:
        return "General"

# -------------------------------
# APPLY ANALYSIS
# -------------------------------
df["Sentiment"] = df["message"].apply(sentiment_analyzer)
df["Category"] = df["message"].apply(categorizing)

# -------------------------------
# METRICS (COLORED)
# -------------------------------
st.subheader("📌 Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Total Feedback", len(df))
col2.metric("😊 Positive", int((df["Sentiment"] == "Positive").sum()))
col3.metric("😡 Negative", int((df["Sentiment"] == "Negative").sum()))

# -------------------------------
# FILTER
# -------------------------------
st.subheader("🔍 Filter Feedback")

option = st.selectbox(
    "Select Sentiment", ["All", "Positive", "Negative", "Neutral"]
)

filtered_df = df.copy()

if option != "All":
    filtered_df = df[df["Sentiment"] == option]

# -------------------------------
# CHARTS (SIDE BY SIDE)
# -------------------------------
st.subheader("📊 Analysis")

col1, col2 = st.columns(2)

with col1:
    st.write("### Sentiment Distribution")
    st.bar_chart(filtered_df["Sentiment"].value_counts())

with col2:
    st.write("### Issue Categories")
    st.bar_chart(filtered_df["Category"].value_counts())

# -------------------------------
# TABLE
# -------------------------------
st.subheader("📄 Feedback Data")
st.dataframe(filtered_df, use_container_width=True)