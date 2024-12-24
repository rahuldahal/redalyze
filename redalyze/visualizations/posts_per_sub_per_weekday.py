# * Posts per sub per weekday

def init(transformed_df):
  per_subreddit = transformed_df.groupby(['subreddit', 'day_of_week']).size()
  
  return per_subreddit
