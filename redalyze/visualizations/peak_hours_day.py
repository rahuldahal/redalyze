# * Peak hours per day
  
def init(transformed_df):
  day_hour = transformed_df.groupby(['day_of_week', 'hour']).size()
  
  return day_hour