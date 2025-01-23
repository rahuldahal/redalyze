# Post distribution per hour per subreddit
  
def post_per_hour(transformed_df):
  hour_group = transformed_df.groupby(['subreddit', 'created_hour'])
  hour_group_count = hour_group.agg(
    total_posts=('created_hour', 'count')
  ).reset_index()
  
  return hour_group_count