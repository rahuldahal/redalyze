# * SHred URL domain per subreddit
  
def init(transformed_df):
  domain_counts = transformed_df.groupby(['subreddit', 'domain']).size().reset_index(name='counts')
  
  return domain_counts