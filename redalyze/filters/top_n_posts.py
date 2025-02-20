# Top posts by score

def top_n_posts(transformed_df, n):
  top_posts = transformed_df[['title', 'author', 'score', 'num_comments', 'subreddit', 'post_id']]
  
  return top_posts.nlargest(columns='score', n=n)
