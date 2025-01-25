from visualizations.score_upvote_bins import score_upvote_ratio

def analyze(transformed_df):  
  # *------ Mean, Median, Quartiles, Standard Deviation, and stuff -------
  # * For specific column: transformed_df[column].describe()
  # * Group wise for all columns: transformed_df.groupby('league').describe()
  # * Group wise for specific columns: transformed_df.groupby('league')['upvotes'].describe()
  # * Specific stat of a specific column: transformed_df['new_column'].mean()
  # * Aggregated stats with single specific column: transformed_df.groupby('league')['upvotes'].agg('mean', 'sum', 'count')
  # * Aggregated stats with specific multiple columns: .agg({
  # *  'upvotes': ['mean', 'sum'],
  # * 'num_comments': 'count'
  # * })

  # upvote_stats = transformed_df.groupby('league')['upvotes'].describe()
  # print(upvote_stats)
  
  # comment_score_stats = transformed_df.groupby('league').agg({
  #   'num_comments': ['mean', 'count'],
  #   'score': 'mean'
  # })
  # print(comment_score_stats)

  
  
  # *------- Correlation between columns --------
  # * transformed_df[['column_one', 'column_two']].corr()
  
  # score_to_comment = transformed_df[['score', 'num_comments']].corr()
  # print(f'Correlation: {score_to_comment}')
  
  
  # *----------Sorting and arranging-----------
  # authors_group = transformed_df.groupby('author')
  # entries_per_author = authors_group.size() # No.of entries per author group
  
  # regular_creators = entries_per_author.sort_values(ascending=False)
  # top_five_creators = regular_creators.head(5)

  
  # print(top_five_creators)
  
  
  # * Score vs Upvote ration correlation

  # upvote_stats = transformed_df.groupby('upvote_category').agg({
  #     'score': 'mean',
  #     'num_comments': 'mean'
  # })
  
  
  # sub_stats = transformed_df.groupby('subreddit').count().reset_index()
  # per_subreddit = transformed_df.groupby(['subreddit', 'hour']).count()
  
  print(score_upvote_ratio(transformed_df))
  
  # Post distribution per hour
  # TODO: 5. Author analysis more: https://chatgpt.com/share/676addf5-56f8-8005-a730-474ac5d96f9f