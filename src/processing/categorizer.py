def categorizing(text):

    text = text.lower()

    if "crash" in text or "error" in text:
        return "Bug"

    elif "slow" in text or "lag" in text:
        return "Performance"

    elif "feature" in text or "add" in text:
        return "Feature Request"

    else:
        return "General"