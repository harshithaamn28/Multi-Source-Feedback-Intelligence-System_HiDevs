from textblob import TextBlob

def sentiment_analyzer(text):

    sentiment_score = TextBlob(text).sentiment.polarity

    if sentiment_score > 0:
        return "Positive"

    elif sentiment_score < 0:
        return "Negative"

    else:
        return "Neutral"