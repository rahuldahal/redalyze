# Run this app with `poetry run python index.py` and
# visit http://127.0.0.1:8050/ in your web browser.


import plotly.express as px
from dash import Dash, html, dcc, dash_table
import networkx as nx
import plotly.graph_objects as go

import transform_data

from visualizations.sub_by_post import sub_by_post
from visualizations.top_n_posts import top_n_posts
from visualizations.top_authors import top_authors
from visualizations.post_per_hour import post_per_hour
from visualizations.hour_score_mean import hour_score_mean
from visualizations.word_frequencies import word_frequencies
from visualizations.score_upvote_bins import score_upvote_grid
from visualizations.post_per_hour_per_sub import post_per_hour_per_sub
from visualizations.score_comment_upvote import score_comment_upvote
from visualizations.author_sub_network import author_sub_network

file_path = '../data/top_posts/week.csv'
  
# Call transform to load and transform the data
transformed_df = transform_data.load_and_transform(file_path)


# SUBREDDIT ACTIVITTY
def sub_by_post_plot(transformed_df):
  df = sub_by_post(transformed_df)

  fig = px.bar(
      df,
      x='subreddit',
      y='total_posts',
      title='Top 10 Subreddits by no. of Posts'
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

def word_frequency_in_title(transformed_df):
  fig = px.treemap(
    word_frequencies(transformed_df),
    path=["word"],
    values="frequency",
    title="Treemap of the most used words in the title"
  )
  
  return fig

# AUTHOR ANALYSIS
def most_active_creators(transformed_df):
  authors = top_authors(transformed_df)

  fig = px.bar(
      authors,
      x='author',
      y='num_posts',
      title='Top 10 Authors by no. of Posts'
  )
  fig.update_layout(xaxis_title="Author", yaxis_title="Number of Posts")
  return fig

def author_contributions(transformed_df):
  G = nx.Graph()
  contributions_df = author_sub_network(transformed_df)

  for _, row in contributions_df.iterrows():
      G.add_edge(row["author"], row["subreddit"], weight=row["contributions"])

  pos = nx.spring_layout(G)

  node_x = []
  node_y = []
  node_labels = []
  node_colors = []

  for node, coords in pos.items():
      node_x.append(coords[0])
      node_y.append(coords[1])
      node_labels.append(node)
      if node in set(contributions_df["author"]):
        node_colors.append("blue")
      else:
        node_colors.append("orange")

  edge_x = []
  edge_y = []

  for edge in G.edges(data=True):
      x0, y0 = pos[edge[0]]
      x1, y1 = pos[edge[1]]
      edge_x.extend([x0, x1, None])
      edge_y.extend([y0, y1, None])

  edge_trace = go.Scatter(
      x=edge_x,
      y=edge_y,
      line=dict(width=1.5, color="#888"),
      hoverinfo="none",
      mode="lines",
  )

  node_trace = go.Scatter(
      x=node_x,
      y=node_y,
      mode="markers+text",
      text=node_labels,
      textposition="top center",
      marker=dict(
          size=20,
          color=node_colors,  # Blue for authors, orange for subreddits
          line_width=2,
      ),
      hoverinfo="text",
  )

  fig = go.Figure(data=[edge_trace, node_trace])
  fig.update_layout(
      showlegend=False,
      margin=dict(t=0, l=0, b=0, r=0),
      xaxis=dict(showgrid=False, zeroline=False),
      yaxis=dict(showgrid=False, zeroline=False),
  )

  return fig


# VARIABLE CORRELATIONS
def variables_correlation(transformed_df):
  fig = px.imshow(
      score_comment_upvote(transformed_df),
      text_auto=True,
      color_continuous_scale='Viridis',
      labels=dict(x="Metrics", y="Metrics", color="Correlation"),
      title="Correlation Heatmap between score, comments, and upvote ratio."
  )
  fig.update_layout(autosize=True)
  return fig

# Initialize Dash app
app = Dash(__name__)

# Create layout with multiple visualizations
app.layout = html.Div([
  html.H1("Redalyze Dashboard"),
  
  # Stats per Subreddit Visualization
  html.Div([
    html.H2("Top 10 subreddits by total posts"),
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
  
  # Most used words
  html.Div([
    html.H2("Most used words"),
    dcc.Graph(figure=word_frequency_in_title(transformed_df))
  ]),
  
  # Top authors
  html.Div([
    html.H2("Top 10 authors by total posts posted"),
    dcc.Graph(figure=most_active_creators(transformed_df))
  ]),
  
  # Author contributions on subreddit
  html.Div([
    html.H2("Author's relationship with subreddits based on volume of contributions"),
    dcc.Graph(figure=author_contributions(transformed_df))
  ]),
  
  # Correlation Heatmap between score, comments, and upvote ratio.
  html.Div([
    html.H2("Correlation Heatmap between score, comments, and upvote ratio."),
    dcc.Graph(figure=variables_correlation(transformed_df))
  ]),
  
  # Add more visualizations here
])

if __name__ == '__main__':
  app.run(debug=True)
