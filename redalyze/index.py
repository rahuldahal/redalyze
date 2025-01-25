# Run this app with `poetry run python index.py` and
# visit http://127.0.0.1:8050/ in your web browser.


import plotly.express as px
from dash import Dash, html, dcc, dash_table

import transform_data

from visualizations.sub_by_post import sub_by_post
from visualizations.post_per_hour_per_sub import post_per_hour_per_sub
from visualizations.score_upvote_bins import score_upvote_grid
from visualizations.hour_score_mean import hour_score_mean
from visualizations.post_per_hour import post_per_hour
from visualizations.top_n_posts import top_n_posts

file_path = '../data/top_posts/week.csv'
  
# Call transform to load and transform the data
transformed_df = transform_data.load_and_transform(file_path)


# SUBREDDIT ACTIVITTY
def sub_by_post_plot(transformed_df):
  df = sub_by_post(transformed_df).melt(id_vars='subreddit', value_vars=['total_posts'],
                        var_name='metric', value_name='value')

  fig = px.bar(
      df,
      x='subreddit',
      y='value',
      color='metric',
      title='Top 10 Subreddits by no. of Posts',
      labels={'value': 'Metric Value', 'subreddit': 'Subreddit'}
  )
  fig.update_layout(xaxis_title="Subreddit", yaxis_title="Metric Value")
  return fig

def post_frequencey_overtime(transformed_df):
  fig = px.line(
    post_per_hour_per_sub(transformed_df),
    x='created_hour',
    y='total_posts',
    color='subreddit',
    title='Post Frequency Over Time by Subreddit',
    labels={'created_hour': 'Hour of Day', 'total_posts': 'Number of Posts'},
    line_shape='linear'
)
  
  return fig

# ENGAGEMENT ANALYSIS
def scatter_plot_top_subreddits(transformed_df):
  fig = px.scatter(
      transformed_df,
      x='score',           # X-axis as score
      y='num_comments',          # Y-axis as num_comments
      size='score',          # I have no idea what this is... just WORKED!
      color='subreddit',           # Color points by subreddit
      title='Relationship Between Average Score and Total Comments for Top 10 Subreddits',
      labels={'score': 'Average Score', 'num_comments': 'Total Comments', 'subreddit': 'Total Posts'},
      hover_data=['subreddit']     # Hover data showing subreddit name
  )
  
  # Update the layout to make the chart clearer
  fig.update_layout(
      xaxis_title='Average Score',
      yaxis_title='Total Comments',
      title_x=0.5
  )
  
  return fig

def score_upvote_patterns(transformed_df):
  heatmap_grid = score_upvote_grid(transformed_df)
  
  fig = px.imshow(
      heatmap_grid,
      labels=dict(x="Upvote Ratio Category", y="Score Category", color="Post Count"),
      x=heatmap_grid.columns,
      y=heatmap_grid.index,
      # color_continuous_scale="Viridis",
  )
  fig.update_layout(title="Heatmap: Score vs Upvote Ratio")
  return fig

# TEMPRAL PATTERNS  
def average_score_overtime(transformed_df):
  fig = px.line(
    hour_score_mean(transformed_df),
    x='created_hour',
    y='mean_score',
    title='Average Score Over Time across subreddits',
    labels={'created_hour': 'Hour of Day', 'mean_score': 'Average Score'},
    line_shape='linear'
)
  
  return fig

def hourly_posts(transformed_df):
  fig = px.histogram(post_per_hour(transformed_df), x='created_hour', y='total_posts')
  
  return fig

# TOP POSTS
def top_10_posts(transformed_df):
  top_posts = top_n_posts(transformed_df, 10)
  
  fig = dash_table.DataTable(
    data=top_posts.to_dict('records'),
    columns=[{'name': i, 'id': i} for i in top_posts.columns]
  )
  
  return fig

# Initialize Dash app
app = Dash(__name__)

# Create layout with multiple visualizations
app.layout = html.Div([
  html.H1("Redalyze Dashboard"),
  
  # Stats per Subreddit Visualization
  html.Div([
    html.H2("Top 10 subreddits by average score, total comments, and total posts"),
    dcc.Graph(figure=sub_by_post_plot(transformed_df))
  ]),
  
  # Post frequency overtime by subreddit
  html.Div([
    html.H2("Post frequency overtime by subreddit"),
    dcc.Graph(figure=post_frequencey_overtime(transformed_df))
  ]),
  
  # Scatter plot of Top Subreddits Visualization
  html.Div([
    html.H2("Relationship between average score and total comments"),
    dcc.Graph(figure=scatter_plot_top_subreddits(transformed_df))
  ]),
  
  # Upvote patterns with post score
  html.Div([
    html.H2("Upvote patterns with post score"),
    dcc.Graph(figure=score_upvote_patterns(transformed_df))
  ]),
  
  # Average score overtime
  html.Div([
    html.H2("Average score overtime"),
    dcc.Graph(figure=average_score_overtime(transformed_df))
  ]),
  
  # Posts per hour
  html.Div([
    html.H2("Posts per hour"),
    dcc.Graph(figure=hourly_posts(transformed_df))
  ]),
  
  # Top 10 posts by socre
  html.Div([
    html.H2("Top 10 posts by socre"),
    top_10_posts(transformed_df)
  ]),
  
  # Add more visualizations here
])

if __name__ == '__main__':
  app.run(debug=True)
