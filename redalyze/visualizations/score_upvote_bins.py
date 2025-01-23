# - Detect patterns in highly upvoted content.

def score_upvote_grid(transformed_df):
  score_upvote_group = transformed_df.groupby(['score_category', 'upvote_category'], observed=False)
  score_upvote_group_count = score_upvote_group.size().reset_index(name='post_count')
  
  pivot_table = score_upvote_group_count.pivot(index='score_category', columns='upvote_category', values='post_count').fillna(0)
  
  return pivot_table