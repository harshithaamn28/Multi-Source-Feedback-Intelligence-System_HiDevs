import streamlit as st
import pandas as pd
from textblob import TextBlob
import requests
import os
from fpdf import FPDF
from google_play_scraper import reviews, Sort
import matplotlib.pyplot as plt

# -------------------------------
# PAGE CONFIG (important)
# -------------------------------
# -------------------------------
# GOOGLE PLAY STORE REVIEWS
# -------------------------------
def fetch_playstore_reviews():
    try:
        result, _ = reviews(
            "com.instagram.android",
            lang="en",
            country="in",
            sort=Sort.NEWEST,
            count=50
        )

        play_df = pd.DataFrame(result)

        play_df = play_df.rename(columns={
            "content": "message",
            "at": "date"
        })

        play_df = play_df[["message", "date"]]
        play_df["source"] = "google_play"

        return play_df

    except Exception as e:
        st.warning(f"Play Store source failed: {e}")

        fallback_df = pd.DataFrame({
            "message": [
            "App is very good",
            "Slow performance issue",
            "Needs more features"
        ],
        "date": pd.to_datetime(["2026-04-05"] * 3),
        "source": ["google_play"] * 3
    })

    return fallback_df

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
st.title("Feedback Intelligence System")

# -------------------------------
# LOAD CSV
# -------------------------------
try:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "sample_feedback.csv")

    csv_df = pd.read_csv(file_path)
    csv_df["source"] = "csv"

    api_data = requests.get(
    "http://127.0.0.1:8000/reviews",
    timeout=5
    ).json()

    api_df = pd.DataFrame(api_data)
    api_df["source"] = "api"

    play_df = fetch_playstore_reviews()
    st.write("Google Play rows:", len(play_df))
    st.write(play_df.head())

    df = pd.concat(
    [csv_df, api_df, play_df],
    ignore_index=True
    )
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

except Exception as e:
    st.error("Error loading CSV file")
    st.write(e)
    st.stop()

# -------------------------------
# CHECK COLUMN
# -------------------------------
if "message" not in df.columns:
    st.error("CSV must contain 'message' column")
    st.stop()

# -------------------------------
# SENTIMENT FUNCTION
# -------------------------------
def sentiment_analyzer(text):
    polarity = TextBlob(str(text)).sentiment.polarity
    confidence = round(abs(polarity) * 100, 2)

    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return pd.Series([sentiment, confidence])

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
df[["Sentiment", "Confidence"]] = df["message"].apply(sentiment_analyzer)
df["Category"] = df["message"].apply(categorizing)

# -------------------------------
# METRICS (COLORED)
# -------------------------------
st.subheader(" Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Total Feedback", len(df))
col2.metric("😊 Positive", int((df["Sentiment"] == "Positive").sum()))
col3.metric("😡 Negative", int((df["Sentiment"] == "Negative").sum()))

# -------------------------------
# FILTER
# -------------------------------
# -------------------------------
# FILTER
# -------------------------------
st.subheader("🔍 Filter Feedback")

option = st.selectbox(
    "Select Sentiment",
    ["All", "Positive", "Negative", "Neutral"]
)

source_option = st.selectbox(
    "Select Source",
    ["All", "csv", "api", "google_play"]
)

date_range = st.date_input(
    "Select Date Range",
    value=(df["date"].min(), df["date"].max())
)

# Start with full dataframe
filtered_df = df.copy()

# Apply date filter
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df["date"] >= pd.to_datetime(start_date)) &
        (filtered_df["date"] <= pd.to_datetime(end_date))
    ]

# Apply source filter
if source_option != "All":
    filtered_df = filtered_df[
        filtered_df["source"].str.lower() == source_option.lower()
    ]

# Apply sentiment filter
if source_option != "All":
    filtered_df = filtered_df[
        filtered_df["source"].astype(str).str.strip().str.lower()
        == source_option.strip().lower()
    ]

# Debug (optional - remove later)
st.write("Filtered Rows:", len(filtered_df))

# -------------------------------
# CHARTS (SIDE BY SIDE)
# -------------------------------
st.subheader(" Analysis")
st.write("All sources in df:", df["source"].value_counts())
st.write("Filtered rows:", len(filtered_df))

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
st.line_chart(filtered_df["Category"].value_counts())

st.subheader("Sentiment Trend Over Time")

df["date"] = pd.to_datetime(df["date"])

trend_df = df.groupby(["date", "Sentiment"]).size().unstack(fill_value=0)

st.line_chart(trend_df)

def create_pdf():
    # -------------------------------
    # CHART 1: SENTIMENT DISTRIBUTION
    # -------------------------------
    sentiment_counts = df["Sentiment"].value_counts()

    plt.figure(figsize=(5, 3))
    sentiment_counts.plot(kind="bar")
    plt.title("Sentiment Distribution")
    plt.tight_layout()
    plt.savefig("sentiment_chart.png")
    plt.close()

    # -------------------------------
    # CHART 2: ISSUE CATEGORY
    # -------------------------------
    category_counts = df["Category"].value_counts()

    plt.figure(figsize=(5, 3))
    category_counts.plot(kind="bar")
    plt.title("Issue Categories")
    plt.tight_layout()
    plt.savefig("category_chart.png")
    plt.close()

    # -------------------------------
    # PDF CREATION
    # -------------------------------
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Weekly Feedback Report", ln=True)

    total = len(df)
    positive = (df["Sentiment"] == "Positive").sum()
    negative = (df["Sentiment"] == "Negative").sum()
    neutral = (df["Sentiment"] == "Neutral").sum()

    pdf.cell(200, 10, txt=f"Total Feedback: {total}", ln=True)
    pdf.cell(200, 10, txt=f"Positive Reviews: {positive}", ln=True)
    pdf.cell(200, 10, txt=f"Negative Reviews: {negative}", ln=True)
    pdf.cell(200, 10, txt=f"Neutral Reviews: {neutral}", ln=True)

    top_issue = df["Category"].value_counts().idxmax()
    pdf.cell(200, 10, txt=f"Top Reported Issue: {top_issue}", ln=True)

    # ADD CHART IMAGES
    pdf.ln(5)
    pdf.image("sentiment_chart.png", x=10, w=180)

    pdf.ln(70)
    pdf.image("category_chart.png", x=10, w=180)

    pdf.output("weekly_report.pdf")


if st.button("Generate PDF Report"):
    create_pdf()
    st.success("PDF report generated successfully")

# ISSUE PRIORITIZATION
# -------------------------------
st.subheader("🚨 Priority Issues")

priority_issues = df[df["Sentiment"] == "Negative"]["Category"].value_counts()

st.bar_chart(priority_issues)
# TABLE
st.subheader("Feedback Data")
st.dataframe(
    df[["message", "Sentiment", "Confidence", "Category", "source", "date"]]
)