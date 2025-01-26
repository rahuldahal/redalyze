# Analyze author and their contributions and involvement in subreddit

import pandas as pd

def author_sub_network(transformed_df):
  authors = transformed_df['author'].dropna()
  subreddits = transformed_df['subreddit'].dropna()
  
  author_sub = pd.DataFrame({
    'author': authors,
    'subreddit': subreddits
  }).drop_duplicates()
  
  
  # Network author->subreddit where source = author and target = subreddit
  network = author_sub.groupby('author')['subreddit'].value_counts().reset_index(name='contributions')
  
  return network.nlargest(columns='contributions', n=20)
