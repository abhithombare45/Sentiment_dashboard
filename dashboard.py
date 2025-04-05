import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
# import re
# import nltk
# from nltk.corpus import stopwords

# st.write("Hello, Streamlit is working!")
# st.balloons()
st.snow()
# Dashboard title
st.title("Social Media Sentiment Dashboard")

# Load processed data
df = pd.read_csv("./processed_posts.csv")

# df["Sentiment"]

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

# Topic bar chart (Debugging added)
fig, ax = plt.subplots()
topic_counts = df["Topic"].value_counts()

# Debugging: Print topic data before plotting
# st.write("Filtered DataFrame (first 5 rows):")
# st.write(df.head())

st.write("Topic Counts:")
st.write(topic_counts)

if not topic_counts.empty:
    topic_counts.plot.bar(ax=ax)
    st.pyplot(fig)
else:
    st.write("No data available for the selected sentiment.")

# Clear Matplotlib cache
plt.close(fig)

# Word cloud
wordcloud = WordCloud().generate(" ".join(df["Title"]))
fig, ax = plt.subplots()
ax.imshow(wordcloud)
ax.axis("off")
st.pyplot(fig)
