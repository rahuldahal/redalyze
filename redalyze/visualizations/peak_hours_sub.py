# * Peak hours per subreddit
  
def peak_hours_sub(transformed_df):
  sub_per_hour = transformed_df.groupby(['subreddit', 'created_hour'])  
  sub_per_hour_count = sub_per_hour.agg(
    total_posts= ('created_hour', 'count')
  ).reset_index()
  
  return sub_per_hour_count