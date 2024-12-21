import praw
import pandas as pd
from dotenv import dotenv_values

config = dotenv_values(".env")

def connection():
  return praw.Reddit(
    client_id=config["REDDIT_CLIENT_ID"],
    client_secret=config["REDDIT_SECRET"],
    user_agent=config["REDDIT_USER_AGENT"]
  )


# Create an intermediary list to store relevant data, because the raw data returned by PRAW is not compatible with pandas for analysis
def flatten_raw_data(raw_data):
  flat_data = []
  for datum in raw_data:
    flat_data.append({
        'subreddit': datum.subreddit,
        'id': datum.id,
        'title': datum.title,
        'author': datum.author.name if datum.author else 'N/A',
        'upvotes': datum.ups,
        'downvotes': datum.downs,
        'score': datum.score,
        'num_comments': datum.num_comments,
        'comments': datum.comments, # 'top_level_comment' is inside this => top level of the thread
        'created_utc': datum.created_utc,
        'awards_received': datum.total_awards_received,
        'flair': datum.flair
    })
  return flat_data

# Pandas' logic with the data frame
def analyze_with_pd(df):
  print(df.loc[0:10, "title"])













def main():
  reddit = connection()
  
  # Fetch posts from a subreddit
  # raw_data = reddit.subreddit('premierleague+bundesliga+laliga+seriea+ligue1').hot(limit=100)
  raw_data = reddit.subreddit('premierleague+bundesliga+laliga+seriea+ligue1').hot(limit=10)
  flat_data = flatten_raw_data(raw_data)
  
  # Convert the flat_data into a Pandas DataFrame and handle business logic
  df = pd.DataFrame(flat_data)
  analyze_with_pd(df)

if __name__ == "__main__":
  main()
