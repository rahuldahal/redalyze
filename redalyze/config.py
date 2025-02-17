import praw
from dotenv import dotenv_values

config = dotenv_values("../.env")

def get_reddit_connection():
  return praw.Reddit(
    client_id=config["REDDIT_CLIENT_ID"],
    client_secret=config["REDDIT_SECRET"],
    user_agent=config["REDDIT_USER_AGENT"]
  )
