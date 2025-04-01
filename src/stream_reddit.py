import praw
import time

reddit = praw.Reddit("Sentiment_dashboard")
subreddit = reddit.subreddit("technology")
try:
    for submission in subreddit.stream.submissions():
        print(f"Time: {time.ctime()}, Title: {submission.title}")
        print(f"Rate limit remaining: {reddit.auth.limits['remaining']}")
        time.sleep(5)  # Wait 5 seconds to stay under 100 QPM (12 posts/minute)
except Exception as e:
    print(f"Error: {e}")
    time.sleep(60)  # Wait before retrying
