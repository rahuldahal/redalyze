from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
from config import get_reddit_connection
import transform_data
import dash
from dash import html, dcc
from services.plot_service import PlotService

# Initialize Flask app
app = Flask(__name__)

# Initialize Dash app inside Flask
dash_app = dash.Dash(__name__, server=app, routes_pathname_prefix="/dashboard/")
dash_app.title = "Redalyze Dashboard"

# Global variable to store processed data
transformed_df = pd.DataFrame()

@app.route("/", methods=["GET", "POST"])
def index():
  global transformed_df
  if request.method == "POST":
    subreddits = request.form.get("subreddits")
    if subreddits:
      # Normalize input (replace spaces & commas with '+')
      subreddits = subreddits.replace(",", " ").replace("+", " ").split()
      subreddits = "+".join(subreddits)  # Convert list back to Reddit's format

      reddit = get_reddit_connection()
      raw_data = reddit.subreddit(subreddits).top(time_filter="week", limit=50)

      flat_data = [
        {
          'subreddit': str(post.subreddit),
          'id': post.id,
          'title': post.title,
          'author': post.author.name if post.author else 'N/A',
          'upvote_ratio': post.upvote_ratio,
          'score': post.score,
          'num_comments': post.num_comments,
          # 'comments': post.comments, # 'top_level_comment' is inside this => top level of the thread
          'created_utc': post.created_utc,
          'url': post.url,
          'awards_received': post.total_awards_received,
          'flair': post.flair
        }
        for post in raw_data
      ]

      transformed_df = transform_data.load_and_transform(pd.DataFrame(flat_data))

    return redirect(url_for("/dashboard/"))

  return render_template("index.html")

# Dash Layout
def create_layout():
  """Dynamically creates the Dash layout after data is set."""
  if transformed_df.empty:
    return html.Div([html.H2("No data available. Please enter a subreddit on the homepage.")])

  vs = PlotService(transformed_df)

  return html.Div([
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

dash_app.layout = create_layout

if __name__ == "__main__":
  app.run(debug=True, port=5000)  # Only one server
