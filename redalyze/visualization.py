# Run this app with `poetry run python index.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc

from services.plot_service import PlotService

# Initialize Dash app
app = Dash(__name__)
transformed_df = None

def set_data(df):
  """Set the transformed DataFrame before running the app."""
  global transformed_df
  transformed_df = df
  create_layout()
  
  # Start Dash app after layout is been created.
  app.run_server(debug=True)

def create_layout():
  if transformed_df is None:
    raise ValueError("transformed_df is None. Ensure data is loaded before visualization.")

  vs = PlotService(transformed_df)
  
  app.layout = html.Div([
    html.H1("Redalyze Dashboard"),
    
    # Subreddit Activity
    html.Div([
      html.H2("Top 10 Subreddits by Total Posts"),
      dcc.Graph(figure=vs.get_sub_by_post_plot())
    ]),
    html.Div([
      html.H2("Post Frequency Overtime by Subreddit"),
      dcc.Graph(figure=vs.get_post_frequency_plot())
    ]),
    
    # Engagement Analysis
    html.Div([
      html.H2("Relationship Between Score and Comments"),
      dcc.Graph(figure=vs.get_scatter_plot_plot())
    ]),
    html.Div([
      html.H2("Upvote Patterns with Post Score"),
      dcc.Graph(figure=vs.get_score_upvote_plot())
    ]),
    
    # Temporal Patterns
    html.Div([
      html.H2("Average Score Over Time"),
      dcc.Graph(figure=vs.get_avg_score_overtime_plot())
    ]),
    html.Div([
      html.H2("Posts Per Hour"),
      dcc.Graph(figure=vs.get_hourly_posts_plot())
    ]),
    
    # Top Posts
    html.Div([
      html.H2("Top 10 Posts by Score"),
      vs.get_top_posts_plot()
    ]),
    html.Div([
      html.H2("Most Used Words in Titles"),
      dcc.Graph(figure=vs.get_word_frequencies_plot())
    ]),
    
    # Author Analysis
    html.Div([
      html.H2("Top 10 Authors by Total Posts"),
      dcc.Graph(figure=vs.get_top_authors_plot())
    ]),
    html.Div([
      html.H2("Author Contributions Across Subreddits"),
      dcc.Graph(figure=vs.get_author_contributions_plot())
    ]),
    
    # Correlation Analysis
    html.Div([
      html.H2("Correlation Heatmap: Score, Comments, Upvote Ratio"),
      dcc.Graph(figure=vs.get_correlation_heatmap_plot())
    ])
  ])
