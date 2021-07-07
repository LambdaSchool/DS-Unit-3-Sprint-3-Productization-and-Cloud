import os
import praw
import basilica
from dotenv import load_dotenv

load_dotenv()

user_agent = "LambdaAnalysisClient/0.1 by " + os.getenv("REDDIT_USERNAME")

reddit = praw.Reddit(client_id=os.getenv("REDDIT_CLIENT_ID"),
                     client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
                     password=os.getenv("REDDIT_PASSWORD"),
                     user_agent=user_agent,
                     username=os.getenv("REDDIT_USERNAME"))

lambda_posts = reddit.subreddit('all').search('Lambda School', sort='new')

submissions = []
for submission in lambda_posts:
    submissions.append(submission)

embeddings = []

for submission in submissions:
    if submission.selftext != "":
        
with basilica.Connection(os.getenv("BASILICA_KEY")) as c:
    embeddings = list(c.embed_sentences(sentences))