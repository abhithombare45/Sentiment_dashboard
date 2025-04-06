import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from datetime import datetime

st.set_page_config(layout="wide")
st.title("Social Media Sentiment Dashboard")

# Load processed data
df = pd.read_csv("processed_posts.csv")
df["Time"] = pd.to_datetime(df["Time"])

sentiment_filter = st.selectbox(
    "Select Sentiment", ["All", "POSITIVE", "NEGATIVE", "NEUTRAL"]
)
topic_filter = st.multiselect(
    "Select Topics", df["Topic"].unique(), default=df["Topic"].unique()
)

filtered_df = df.copy()
if sentiment_filter != "All":
    filtered_df = filtered_df[filtered_df["Sentiment"] == sentiment_filter]
if topic_filter:
    filtered_df = filtered_df[filtered_df["Topic"].isin(topic_filter)]

# Display data table
st.write(filtered_df[["Time", "Title", "Sentiment", "Topic"]])

# Time-based sentiment distribution
fig, ax = plt.subplots(figsize=(10, 6))
filtered_df.groupby(
    [pd.Grouper(key="Time", freq="H"), "Sentiment"]
).size().unstack().plot(ax=ax)
ax.set_title("Sentiment Distribution by Hour")
st.pyplot(fig)

# Sentiment pie chart
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()
    filtered_df["Sentiment"].value_counts().plot.pie(autopct="%1.1f%%", ax=ax)
    ax.set_ylabel("")  # Hide y-label for aesthetics
    st.pyplot(fig)
st.write("Total Posts:", filtered_df.shape[0])
st.write(
    "Positive Posts:", filtered_df[filtered_df["Sentiment"] == "POSITIVE"].shape[0]
)
st.write(
    "Negative Posts:", filtered_df[filtered_df["Sentiment"] == "NEGATIVE"].shape[0]
)
st.write("Neutral Posts:", filtered_df[filtered_df["Sentiment"] == "NEUTRAL"].shape[0])

with col2:
    st.markdown(
        "<br><br><br><span style='font-size:19px; font-style:italic;'>This pie chart shows the distribution of sentiment categories in the dataset (Positive, Neutral, and Negative). The percentages indicate the relative frequency of each sentiment.</span>",
        unsafe_allow_html=True,
    )
# Topic word cloud
if topic_filter:
    topic = topic_filter[0]
    words = df[df["Topic"] == topic]["Text"].str.split().explode().value_counts
    fig, ax = plt.subplots(figsize=(10, 6))
    words.nlargest(10).plot(kind="bar", ax=ax)
    ax.set_title(f"Top 10 Words in Topic: {topic}")
    st.pyplot(fig)
else:
    st.write("Select a topic to view its word cloud")

# Topic bar chart
fig, ax = plt.subplots()
topic_counts = filtered_df["Topic"].value_counts()
st.write("Topic Counts:")
st.write(topic_counts)

if not topic_counts.empty:
    topic_counts.plot.bar(ax=ax)
    st.pyplot(fig)
else:
    st.write("No data available for the selected sentiment.")

# Word cloud
wordcloud = WordCloud().generate(" ".join(filtered_df["Title"]))
fig, ax = plt.subplots()
ax.imshow(wordcloud)
ax.axis("off")
st.pyplot(fig)
