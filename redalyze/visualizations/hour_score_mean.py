# * Average score over hours

def hour_score_mean(transformed_df):
  hour_group = transformed_df.groupby('created_hour')
  hour_group_score_mean = hour_group.agg(
    mean_score=('score', 'mean')
  ).reset_index()
  
  return hour_group_score_mean.sort_values('created_hour')
