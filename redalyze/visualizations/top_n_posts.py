# Top posts by score

# * Trim(limit characters) the title
# * wrap URL inside the anchor tag

def top_n_posts(transformed_df, n):
  top_posts = transformed_df[['title', 'author', 'score', 'num_comments', 'url']]
  
  return top_posts.nlargest(columns='score', n=n)
