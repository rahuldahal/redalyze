# * Stats per subreddit
  
def init(transformed_df):
  sub_stats = transformed_df.groupby('subreddit').agg({
    'score': [('Average Score', 'mean')],
    'num_comments': [('Total Comments', 'sum')],
    'subreddit': [('Total Posts', 'size')]  # Counting total posts
  })
  
  return sub_stats