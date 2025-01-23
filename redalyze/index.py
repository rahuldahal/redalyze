# Run this app with `poetry run python index.py` and
# visit http://127.0.0.1:8050/ in your web browser.


import plotly.express as px
from dash import Dash, html, dcc

import transform_data
# from visualizations.common_domain_per_sub import common_domain_per_sub
from visualizations.sub_by_post import sub_by_post
from visualizations.post_per_hour import post_per_hour
# from visualizations.stats_per_author import stats_per_author

file_path = '../data/top_posts/week.csv'
  
# Call transform to load and transform the data
transformed_df = transform_data.load_and_transform(file_path)



# Plots and visualizations logic
# def common_domains_plot(transformed_df):
#   df = common_domain_per_sub(transformed_df)
#   fig = px.bar(df, x='domain', y='counts', color='subreddit', title='Common Domains per Subreddit')
#   return fig

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

def post_frequencey_overtime(transformed_df):
  fig = px.line(
    post_per_hour(transformed_df),
    x='created_hour',               # X-axis: Hours of the day (created_hour)
    y='total_posts',                # Y-axis: Number of posts
    color='subreddit',              # Different lines for each subreddit
    title='Post Frequency Over Time by Subreddit',
    labels={'created_hour': 'Hour of Day', 'total_posts': 'Number of Posts'},
    line_shape='linear'             # You can choose a line shape, like 'linear' or 'spline'
)
  
  return fig

# def stats_per_author_plot(transformed_df):
#   df = stats_per_author(transformed_df)
#   fig = px.bar(df, x='author', y='Average Score', title='Average Scores per Author')
#   return fig


# Initialize Dash app
app = Dash(__name__)

# Create layout with multiple visualizations
app.layout = html.Div([
  html.H1("Redalyze Dashboard"),
  
  # Common Domains Visualization
  # html.Div([
  #   html.H2("Common Domains per Subreddit"),
  #   dcc.Graph(figure=common_domains_plot(transformed_df))
  # ]),
  
  # Stats per Subreddit Visualization
  html.Div([
    html.H2("Top 10 subreddits by average score, total comments, and total posts"),
    dcc.Graph(figure=sub_by_post_plot(transformed_df))
  ]),
  
  # Scatter plot of Top Subreddits Visualization
  html.Div([
    html.H2("Relationship between average score and total comments"),
    dcc.Graph(figure=scatter_plot_top_subreddits(transformed_df))
  ]),
  
  # Post frequency overtime by subreddit
  html.Div([
    html.H2("Post frequency overtime by subreddit"),
    dcc.Graph(figure=post_frequencey_overtime(transformed_df))
  ]),
  
  # Add more visualizations here
])

if __name__ == '__main__':
  app.run(debug=True)
