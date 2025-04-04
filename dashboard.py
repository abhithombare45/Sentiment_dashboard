import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
# import re
# import nltk
# from nltk.corpus import stopwords

# st.write("Hello, Streamlit is working!")
st.balloons()
# Dashboard title
st.title("Social Media Sentiment Dashboard")

# Load processed data
df = pd.read_csv("processed_posts.csv")

# Sentiment filter
sentiment_filter = st.selectbox(
    "Select Sentiment", ["All", "POSITIVE", "NEGATIVE", "NEUTRAL"]
)
if sentiment_filter != "All":
    df = df[df["Sentiment"] == sentiment_filter]

# Display data table
st.write(df[["Time", "Title", "Sentiment", "Topic"]])

# Sentiment pie chart
fig, ax = plt.subplots()
df["Sentiment"].value_counts().plot.pie(autopct="%1.1f%%", ax=ax)
st.pyplot(fig)

# Topic bar chart
fig, ax = plt.subplots()
df["Topic"].value_counts().plot.bar(ax=ax)
st.pyplot(fig)

# Word cloud
wordcloud = WordCloud().generate(" ".join(df["Title"]))
fig, ax = plt.subplots()
ax.imshow(wordcloud)
ax.axis("off")
st.pyplot(fig)
