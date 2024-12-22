import praw
import pandas as pd
from dotenv import dotenv_values

import transform_data
import analyze_data

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

def main():
  reddit = connection()
  
  # Fetch posts from a subreddit
  # raw_data = reddit.subreddit('premierleague+bundesliga+laliga+seriea+ligue1').hot(limit=100)
  raw_data = reddit.subreddit('premierleague+bundesliga+laliga+seriea+ligue1').hot(limit=10)
  flat_data = flatten_raw_data(raw_data)
  
  # Convert the flat_data into a Pandas DataFrame
  df = pd.DataFrame(flat_data)

  # Call transform to load and transform the data
  transformed_df = transform_data.load_and_transform(df)
  
  # Call analyze to perform analysis on the transformed data
  analyze_data.analyze(transformed_df)

def offline():
  file_path = './data/index.csv'
    
  # Call transform to load and transform the data
  transformed_df = transform_data.load_and_transform(file_path)
  
  # Call analyze to perform analysis on the transformed data
  analyze_data.analyze(transformed_df)
  
  
if __name__ == "__main__":
  offline()
