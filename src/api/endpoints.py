from fastapi import FastAPI
from src.processing.cleaner import cleaning_text
from src.processing.analyzer import sentiment_analyzer
from src.processing.categorizer import categorizing

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Feedback Intelligence System Running"}

@app.post("/feedback")
def process_feedback(data: dict):

    text = data.get("message")

    cleaned = cleaning_text(text)

    sentiment = sentiment_analyzer(cleaned)

    category = categorizing(cleaned)

    return {
        "original": text,
        "cleaned": cleaned,
        "sentiment": sentiment,
        "category": category
    }