import pandas as pd

# Reload from file
df = pd.read_csv('data.csv')


# ---- TRANSFORMATIONS ----
 
# Date Transformations
df['created_date'] = pd.to_datetime(df['created_utc'], unit='s')
df['day_of_week'] = df['created_date'].dt.day_name() # Sunday, Monday, etc
df['hour'] = df['created_date'].dt.hour

# Category Classifications
df['score_category'] = pd.cut(df['score'], bins=[0, 50, 100, 200, 500, 1000], labels=['low', 'medium', 'high', 'very high', 'top'])
df['comment_category'] = pd.cut(df['num_comments'], bins=[0, 10, 50, 100, 200, 300], labels=['few', 'some', 'many', 'trending', 'top'])

df['league'] = df['subreddit'].map({
    'PremierLeague': 'Premier League',
    'LaLiga': 'La Liga',
    'Bundesliga': 'Bundesliga',
    'seriea': 'Serie A',
    'Ligue1': 'Ligue 1'
})
