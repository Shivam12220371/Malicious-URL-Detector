from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from scipy.sparse import hstack
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

from feature_engineering import extract_struct_features


def load_dataset(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df = df[["url", "label"]].dropna()
    df["label"] = df["label"].str.lower().map({"good": 0, "bad": 1})
    df = df.dropna(subset=["label"]).reset_index(drop=True)
    return df


def build_features(urls: pd.Series, vectorizer: TfidfVectorizer):
    text_features = vectorizer.fit_transform(urls)
    struct_features = np.array([extract_struct_features(url) for url in urls])
    return hstack([text_features, struct_features])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, default="../dataset/urls.csv")
    parser.add_argument("--model-out", type=str, default="model.pkl")
    parser.add_argument("--vectorizer-out", type=str, default="vectorizer.pkl")
    args = parser.parse_args()

    df = load_dataset(Path(args.dataset))

    vectorizer = TfidfVectorizer(
        analyzer="char",
        ngram_range=(3, 5),
        min_df=2,
        max_features=12000,
    )

    X = build_features(df["url"], vectorizer)
    y = df["label"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    lr = LogisticRegression(max_iter=500, class_weight="balanced")
    rf = RandomForestClassifier(
        n_estimators=260,
        random_state=42,
        class_weight="balanced_subsample",
        n_jobs=-1,
    )
    nb = MultinomialNB(alpha=0.3)

    ensemble = VotingClassifier(
        estimators=[("lr", lr), ("rf", rf), ("nb", nb)],
        voting="soft",
        n_jobs=-1,
    )

    ensemble.fit(X_train, y_train)

    y_pred = ensemble.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print(f"Accuracy: {accuracy:.4f}")
    print(report)

    joblib.dump(ensemble, args.model_out)
    joblib.dump(vectorizer, args.vectorizer_out)


if __name__ == "__main__":
    main()
