import pandas as pd
import re
from transformers import pipeline


# Load the CSV file containing Reddit posts
df = pd.read_csv("../posts.csv")
df
df.head(5)
df.tail(5)

# 2. Data Cleansing


def preprocess_text(text):
    text = re.sub(r"http\S+", "", text)  # Remove URLs
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # Remove special characters
    return text.lower().strip()


df["Title"]
df["Title_Clean"] = df["Title"].apply(preprocess_text)

df

# 3. Sentiment Analysis

# Load sentiment analysis pipeline (uses MPS on Mac M4 for speed)
sentiment_pipeline = pipeline(
    "sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment", device=0
)

# Get cleaned titles as a list
titles = df["Title_Clean"].tolist()

# Run sentiment analysis in batches for efficiency
sentiments = sentiment_pipeline(titles, batch_size=32)

# Add results to DataFrame
df["Sentiment"] = [res["label"] for res in sentiments]
df["Sentiment_Score"] = [res["score"] for res in sentiments]

df.head(4)

df

# 4. Topic Classification

# Load zero-shot classification pipeline
topic_pipeline = pipeline(
    "zero-shot-classification", model="facebook/bart-large-mnli", device=0
)

# Define candidate topics
labels = ["AI", "gadgets", "software", "hardware", "security"]

# Classify each title
results = [
    topic_pipeline(title, candidate_labels=labels) for title in df["Title_Clean"]
]

# Add top topic and score to DataFrame
df["Topic"] = [res["labels"][0] for res in results]
df["Topic_Score"] = [res["scores"][0] for res in results]
df

# Save the processed DataFrame
# df.to_csv('../processed_posts.csv', index=False)
