# * Active subreddit by frequency of post 
  
def sub_by_post(transformed_df):
  sub_group = transformed_df.groupby('subreddit')
  sub_count = sub_group.agg(
    total_posts= ('subreddit', 'count')
  ).reset_index()
  
  return sub_count.sort_values(by='total_posts', ascending=False).head(10)