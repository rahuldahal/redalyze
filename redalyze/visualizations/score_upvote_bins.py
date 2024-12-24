# - Detect patterns in highly upvoted content.

def score_upvote_ratio(transformed_df):
  score_group = transformed_df.groupby('score_category', observed=False)
  score_group_count = score_group.agg(
    total_posts=('score', 'count'),
  ).reset_index()
  
  upvote_group = transformed_df.groupby('upvote_category', observed=False)
  upvote_group_count = upvote_group.agg(
    total_posts=('upvote_ratio', 'count'),
  ).reset_index()
  
  return [score_group_count, upvote_group_count]