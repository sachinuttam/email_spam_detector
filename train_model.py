"""
train_model.py
----------------
Trains a spam-detection model (TF-IDF + Multinomial Naive Bayes) on
data/spam_dataset.csv and saves the trained model + vectorizer to the
model/ folder so the Streamlit app can load them instantly.

Run this once before launching the app:
    python train_model.py
"""

import csv
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report


def load_data(path="data/spam_dataset.csv"):
    texts, labels = [], []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            texts.append(row["text"])
            labels.append(row["label"])
    return texts, labels


def main():
    print("Loading dataset...")
    texts, labels = load_data()
    print(f"Loaded {len(texts)} emails.")

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    print("Vectorizing text (TF-IDF)...")
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        max_features=5000,
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    print("Training Multinomial Naive Bayes classifier...")
    model = MultinomialNB()
    model.fit(X_train_vec, y_train)

    y_pred = model.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nTest accuracy: {acc * 100:.2f}%\n")
    print(classification_report(y_test, y_pred))

    joblib.dump(model, "model/spam_classifier.pkl")
    joblib.dump(vectorizer, "model/vectorizer.pkl")
    print("Saved model to model/spam_classifier.pkl")
    print("Saved vectorizer to model/vectorizer.pkl")


if __name__ == "__main__":
    main()
