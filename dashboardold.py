import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Dashboard title
st.title("Social Media Sentiment Dashboard")

# troubleshooting
st.write("App Loaded")

# Load processed data
df = pd.read_csv("../processed_posts.csv")
#
st.write("CSV Loaded Successfully", df.shape)
if not os.path.exists("../processed_posts.csv"):
    st.error("CSV file not found!")
    st.stop()
df = pd.read_csv("../processed_posts.csv")
#

df

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
