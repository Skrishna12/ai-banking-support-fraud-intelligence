import pandas as pd
import joblib

from Database import engine
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

# Load data
tickets_df = pd.read_sql(
    "SELECT query_text, category FROM support_tickets",
    engine
)

# Features and labels
X = tickets_df["query_text"]
y = tickets_df["category"]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Pipeline
intent_model = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english")),
    ("classifier", LogisticRegression(max_iter=1000))
])

# Train
intent_model.fit(X_train, y_train)

# Predict
predictions = intent_model.predict(X_test)

# Evaluation
accuracy = accuracy_score(y_test, predictions)

print(f"Accuracy: {accuracy:.2f}")
print("\nClassification Report:\n")
print(classification_report(y_test, predictions))

# Save model
joblib.dump(intent_model, "models/intent_classifier.pkl")

print("\nIntent classifier saved successfully.")