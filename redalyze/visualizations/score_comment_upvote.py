# Correlation between score, num_comments, and upvote_ratio

def score_comment_upvote(transformed_df):
  correlation = transformed_df[['score', 'num_comments', 'upvote_ratio']].corr()
  
  return correlation
