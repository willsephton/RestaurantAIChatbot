import glob
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import streamlit as st


@st.cache_resource
def load_model():
    # ! Load and train the intent classification model.
    def load_csv_files(folder_path):
        file_paths = glob.glob(f"{folder_path}/*.csv")
        data_frames = [pd.read_csv(file_path) for file_path in file_paths]
        return pd.concat(data_frames, ignore_index=True)

    folder_path = "intent_data"
    df = load_csv_files(folder_path)
    texts = df["text"].tolist()
    labels = df["label"].tolist()

    model = make_pipeline(
        TfidfVectorizer(stop_words=None, max_df=0.95, ngram_range=(1, 2)),
        MultinomialNB(alpha=0.5, fit_prior=False),
    )
    model.fit(texts, labels)
    return model
