import dash
from dash_layout import dash_layout
import pandas as pd
import transform_data
from dash import html, dcc
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from config import get_reddit_connection
from services.plot_service import PlotService
from flask import Flask, request, render_template, redirect, url_for

# Initialize Flask app
app = Flask(__name__)

# Initialize Dash app inside Flask
bootstrap_theme = dbc.themes.BOOTSTRAP
dash_app = dash.Dash(__name__, server=app, external_stylesheets=[bootstrap_theme], routes_pathname_prefix="/subreddit-activity/")
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
          'post_id': post.id,
          'title': post.title,
          'author': post.author.name if post.author else 'N/A',
          'upvote_ratio': post.upvote_ratio,
          'score': post.score,
          'num_comments': post.num_comments,
          'created_utc': post.created_utc,
          'url': post.url,
          'awards_received': post.total_awards_received,
          'flair': post.flair
        }
        for post in raw_data
      ]

      transformed_df = transform_data.load_and_transform(pd.DataFrame(flat_data))

    return redirect(url_for("/subreddit-activity/"))

  return render_template("index.html")

# Dash Layout
def create_layout():
  """Dynamically creates the Dash layout after data is set."""
  if transformed_df.empty:
    return html.Div([html.H2("No data available. Please enter a subreddit on the homepage.")])

  vs = PlotService(transformed_df)

  layout = dash_layout(html)
  return layout


# Callback for rendering different pages (This must be defined on `dash_app`)
@dash_app.callback(
  Output("page-content", "children"),
  [Input("url", "pathname")]
)
def render_page_content(pathname):
  vs = PlotService(transformed_df)
  
  if pathname == "/subreddit-activity":
    return html.Div([
      html.H2("Most active subreddits"),
      dcc.Graph(figure=vs.get_sub_by_post_plot()),
      html.H2("Post frequency overtime on different subreddits"),
      dcc.Graph(figure=vs.get_post_frequency_plot())
    ])
  
  elif pathname == "/engagement-analysis":
    return html.Div([
      html.H2("Relationship Between Score and Comments"),
      dcc.Graph(figure=vs.get_scatter_plot_plot()),
      html.H2("Correlation Between Score and Upvote Ratio"),
      dcc.Graph(figure=vs.get_score_upvote_plot())
    ])
    
  elif pathname == "/temporal-patterns":
    return html.Div([
      html.H2("Average score over time"),
      dcc.Graph(figure=vs.get_avg_score_overtime_plot()),
      html.H2("Post distribution over time"),
      dcc.Graph(figure=vs.get_hourly_posts_plot())
    ])
  
  elif pathname == "/top-posts":
    return html.Div([
      html.H2("Top 10 Posts by Score"),
      vs.get_top_posts_plot(),
      html.H2("Most used words in titles"),
      dcc.Graph(figure=vs.get_word_frequencies_plot())
    ])
  
  elif pathname == "/author-analysis":
    return html.Div([
      html.H2("Top 10 Authors by Total Posts"),
      dcc.Graph(figure=vs.get_top_authors_plot()),
      html.H2("Network of Authors and Subreddits"),
      dcc.Graph(figure=vs.get_author_contributions_plot())
    ])
  
  elif pathname == "/engagement-correlation":
    return html.Div([
      html.H2("Correlation Heatmap: Score, Comments, Upvote Ratio"),
      dcc.Graph(figure=vs.get_correlation_heatmap_plot())
    ])
  
  # If the user tries to reach a different page, return a 404 message
  return html.Div([
    html.H1("404: Not found", className="text-danger"),
    html.Hr(),
    html.P(f"The pathname {pathname} was not recognised..."),
  ], className="p-3 bg-light rounded-3")

# Add dcc.Location for URL management
dash_app.layout = html.Div([
  dcc.Location(id="url", refresh=True),  # This listens to URL changes
  dash_layout(html)  # The layout we defined earlier
])

if __name__ == "__main__":
  app.run(debug=True, port=5000)
