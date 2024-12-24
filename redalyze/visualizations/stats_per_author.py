# * Stats per author
  
def init(transformed_df):
  author_stats = transformed_df.groupby('author').agg({
    'score': [('Total Score', 'sum')],
    'num_comments': [('Total Comments', 'sum')],
    'author': [('Total Contributons', 'size')]
  })
  
  return author_stats