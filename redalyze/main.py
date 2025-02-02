import sys
import praw
import pandas as pd
from dotenv import dotenv_values

import transform_data
import visualization

config = dotenv_values(".env")

def connection():
  return praw.Reddit(
    # client_id=config["REDDIT_CLIENT_ID"],
    # client_secret=config["REDDIT_SECRET"],
    # user_agent=config["REDDIT_USER_AGENT"]
    client_id="iFIkxi9ipIVjsQW5sQ9CRg",
    client_secret="9G2TjS26m_Rw5ACtocIW3Clr0g6f9A",
    user_agent="redalyze by r/Own-Roadride-"
  )

def get_subreddits():
  subreddits = []
  while True:
    sub = input("Enter the subreddit to analyze (or 'N' to finish): ").strip()
    if sub.lower() == 'n':
      break
    if sub:
      subreddits.append(sub)

  if subreddits:
    return "+".join(subreddits)
  else:
    print("No subreddits provided.")
    sys.exit(1)  # Terminate program

# Create an intermediary list to store relevant data, because the raw data returned by PRAW is not compatible with pandas for analysis
def flatten_raw_data(raw_data):
  flat_data = []
  for datum in raw_data:
    flat_data.append({
        'subreddit': str(datum.subreddit),
        'id': datum.id,
        'title': datum.title,
        'author': datum.author.name if datum.author else 'N/A',
        'upvote_ratio': datum.upvote_ratio,
        'score': datum.score,
        'num_comments': datum.num_comments,
        # 'comments': datum.comments, # 'top_level_comment' is inside this => top level of the thread
        'created_utc': datum.created_utc,
        'url': datum.url,
        'awards_received': datum.total_awards_received,
        'flair': datum.flair
    })
  return flat_data

def main():
  reddit = connection()
  
  # Fetch posts from a subreddit
  # raw_data = reddit.subreddit('premierleague+bundesliga+laliga+seriea+ligue1').hot(limit=100)
  
  try:
    subreddit_query = get_subreddits()
    raw_data = reddit.subreddit(subreddit_query).top(time_filter="week", limit=50)
    print(f"Fetching top posts from: {subreddit_query}")
    
    print("Flatening the data...")
    flat_data = flatten_raw_data(raw_data)

    # Convert the flat_data into a Pandas DataFrame
    print("Converting the data into pandas dataframe...")
    df = pd.DataFrame(flat_data)

    # Call transform to load and transform the data
    print("Transforming and cleaning the data...")
    transformed_df = transform_data.load_and_transform(dataframe=df)
    
    # Call analyze to perform analysis on the transformed data
    # analyze_data.analyze(transformed_df)
    
    # Call visualize to perform visualization on the transformed data
    print("Visualizing the transformed data...")
    
    # Set the data in visualization file
    visualization.set_data(transformed_df)
  except Exception as e:
    print(f"Error: {e}")
  sys.exit(1) 


def offline():
  file_path = '../data/top_posts/week.csv'
    
  # Call transform to load and transform the data
  transformed_df = transform_data.load_and_transform(file_path=file_path)
  
  # Call analyze to perform analysis on the transformed data
  # analyze_data.analyze(transformed_df)
  
  # Set the data in visualization file
  visualization.set_data(transformed_df)

  # Start Dash app (since it's already defined in visualization.py)
  visualization.app.run_server(debug=True)
  
if __name__ == "__main__":
  main()
