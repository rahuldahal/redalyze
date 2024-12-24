import pandas as pd

def load_and_transform(file_path):
  df = pd.read_csv(file_path)


  # Date Transformations
  df['created_date'] = pd.to_datetime(df['created_utc'], unit='s')
  df['day_of_week'] = df['created_date'].dt.day_name() # Sunday, Monday, etc
  df['hour'] = df['created_date'].dt.hour

  # Category Classifications
  df['score_category'] = pd.cut(df['score'], bins=[0, 50, 100, 200, 500, 1000], labels=['Low', 'Average', 'High', 'Very High', 'Top Scores'])
  df['comment_category'] = pd.cut(df['num_comments'], bins=[0, 10, 50, 100, 200, 300], labels=['Few', 'Moderate', 'Many', 'Popular', 'Most Comments'])
  df['upvote_category'] = pd.cut(df['upvote_ratio'], bins=[0, 0.7, 0.9, 1], labels=['Low', 'Medium', 'High'])

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
 