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
  
  comment_score_stats = transformed_df.groupby('league').agg({
    'num_comments': ['mean', 'count'],
    'score': 'mean'
  })
  print(comment_score_stats)
  
  
  # *------- Correlation between columns --------
  # * transformed_df[['column_one', 'column_two']].corr()
  
  # score_to_comment = transformed_df[['score', 'num_comments']].corr()
  # print(f'Correlation: {score_to_comment}')
  