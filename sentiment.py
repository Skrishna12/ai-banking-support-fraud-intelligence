from transformers import pipeline

sentiment_analyzer = None


def load_model():
    global sentiment_analyzer

    if sentiment_analyzer is None:
        sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest"
        )

    return sentiment_analyzer


def predict_sentiment(text):
    model = load_model()

    result = model(text)[0]

    return {
        "sentiment": result["label"].lower(),
        "confidence": round(result["score"], 4)
    }


if __name__ == "__main__":
    print(
        predict_sentiment(
            "Someone transferred ₹50,000 from my account without permission!"
        )
    )