import praw
from dotenv import dotenv_values

config = dotenv_values(".env")

def connection():
    return praw.Reddit(
        client_id=config["REDDIT_CLIENT_ID"],
        client_secret=config["REDDIT_SECRET"],
        user_agent=config["REDDIT_USER_AGENT"]
    )

def data_handler(submissions):
    for submission in submissions:
        print(submission.title)

def main():
    reddit = connection()
    submissions = reddit.subreddit('test').hot(limit=10)
    data_handler(submissions)

if __name__ == "__main__":
    main()
