# * Most active authors
  
def top_authors(transformed_df):
  author_group = transformed_df.groupby('author')
  author_count = author_group.agg(
    num_posts= ('author', 'count')
  ).reset_index()
  
  return author_count.nlargest(columns='num_posts', n=10)