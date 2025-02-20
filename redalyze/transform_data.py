import pandas as pd

def load_and_transform(dataframe=None, file_path=None):
  if file_path:
    df = pd.read_csv(file_path)
  elif dataframe is not None:
    df = dataframe
  else:
    raise ValueError("Error: Either a DataFrame or a file path must be provided!")


  # Date Transformations
  df['created_date'] = pd.to_datetime(df['created_utc'], unit='s')
  df['day_of_week'] = df['created_date'].dt.day_name() # Sunday, Monday, etc
  df['created_hour'] = df['created_date'].dt.hour

  # Category Classifications
  df['score_category'] = pd.cut(
    df['score'],
    bins = [200, 1000, 5000, 10000, 25000, 50000, 75000, 100000],
    labels = ['Low', 'Moderate', 'High', 'Very High', 'Huge', 'Massive', 'Extreme'],
    include_lowest=True
  )

  df['comments_category'] = pd.cut(
    df['num_comments'],
    bins=[150, 500, 2000, 5000, 10000, 15000],
    labels=['Few', 'Some', 'Many', 'Trending', 'Top'],
    include_lowest=True
  )

  df['upvote_category'] = pd.cut(
    df['upvote_ratio'],
    bins=[0, 0.1, 0.25, 0.5, 0.6, 0.75, 0.85, 1],
    labels=['Very Low', 'Low', 'Moderate', 'Average', 'High', 'Very High', 'Excellent'],
    include_lowest=True
  )
  
  return df




# * Find out the count of posts with 'many' comments on each league

# filt_condition = (df['comment_category'] == 'many')
# filtered_df = df[filt_condition].groupby('league')

# size_of_everything = filtered_df.size()

# req_data = size_of_everything.items()

# for league, count in req_data:
#     print(f"{league}: {count}")
 