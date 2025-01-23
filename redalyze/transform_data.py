import pandas as pd

def load_and_transform(file_path):
  df = pd.read_csv(file_path)


  # Date Transformations
  df['created_date'] = pd.to_datetime(df['created_utc'], unit='s')
  df['day_of_week'] = df['created_date'].dt.day_name() # Sunday, Monday, etc
  df['created_hour'] = df['created_date'].dt.hour

  # Category Classifications
  df['score_category'] = pd.cut(
    df['score'],
    bins=[70000, 100000, 130000, 160000, 190000],
    labels=['Moderate', 'High', 'Very High', 'Huge'],
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
    bins=[0, 0.25, 0.5, 0.75, 1],
    labels=['Low', 'Moderate', 'High', 'Very High'],
    include_lowest=True
  )


  # Other
  df['domain'] = df['url'].str.extract(r'https?://(?:www\.)?([^/]+)')
  
  return df




# * Find out the count of posts with 'many' comments on each league

# filt_condition = (df['comment_category'] == 'many')
# filtered_df = df[filt_condition].groupby('league')

# size_of_everything = filtered_df.size()

# req_data = size_of_everything.items()

# for league, count in req_data:
#     print(f"{league}: {count}")
 