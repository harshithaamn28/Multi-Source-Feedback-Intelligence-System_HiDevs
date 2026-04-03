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
@app.get("/reviews")
def get_reviews():
    return [
        {"source": "api", "message": "App crashes during login", "date": "2026-04-01"},
        {"source": "api", "message": "Great user experience", "date": "2026-04-02"},
        {"source": "api", "message": "Slow performance issue", "date": "2026-04-03"}
    ]