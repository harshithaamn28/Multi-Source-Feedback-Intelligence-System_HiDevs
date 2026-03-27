from processing.analyzer import sentiment_analyzer
from processing.cleaner import cleaning_text
from processing.categorizer import categorizing

text = "App crashes when login"

cleaned = cleaning_text(text)

sentiment = sentiment_analyzer(cleaned)

category = categorizing(cleaned)

print("Original:", text)
print("Cleaned:", cleaned)
print("Sentiment:", sentiment)
print("Category:", category)