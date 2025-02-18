import dash
from dash_layout import dash_layout
import pandas as pd
import transform_data
from dash import html, dcc
from config import get_reddit_connection
from services.plot_service import PlotService
from flask import Flask, request, render_template, redirect, url_for

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

  layout =  dash_layout(html, dcc, vs)
  return layout


dash_app.layout = create_layout

if __name__ == "__main__":
  app.run(debug=True, port=5000)
