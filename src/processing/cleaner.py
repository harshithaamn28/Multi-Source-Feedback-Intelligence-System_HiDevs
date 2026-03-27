import re

def cleaning_text(text):

    text = text.lower()

    text = re.sub(r"[^a-zA-Z ]", "", text)

    return text