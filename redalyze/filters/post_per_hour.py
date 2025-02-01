# Post distribution per hour
  
def post_per_hour(transformed_df):
  hour_group = transformed_df.groupby('created_hour')
  hour_group_count = hour_group.agg(
    total_posts=('created_hour', 'count')
  ).reset_index()
  
  return hour_group_count.sort_values('created_hour')