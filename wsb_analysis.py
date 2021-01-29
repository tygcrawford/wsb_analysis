import praw
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import pandas as pd

with open('auth', 'r') as f:
	d = f.readlines()
	d = [ l.rstrip('\n') for l in d ]
	client_id, secret, user_agent, username, password = d

reddit = praw.Reddit(client_id=client_id,
                     client_secret=secret,
                     user_agent=user_agent,
                     username=username,
                     password=password)
reddit.read_only = True

subreddit = reddit.subreddit('TheRedPill')
top_subreddit = subreddit.top(limit=10)
titles = [ post.title for post in top_subreddit ]


sia = SIA()
results = []

for line in titles:
    pol_score = sia.polarity_scores(line)
    pol_score['title'] = line
    results.append(pol_score)

df = pd.DataFrame.from_records(results)
print(df['compound'].mean())
print(df.head())
