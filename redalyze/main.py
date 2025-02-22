import os
import dash
import pandas as pd
import transform_data
from dash import html, dcc
from dash_layout import dash_layout
from dash_routes import handle_routing
import dash_bootstrap_components as dbc
from config import get_reddit_connection
from dash.dependencies import Output, Input
from services.plot_service import PlotService
from flask import Flask, request, render_template, redirect, url_for, jsonify, send_from_directory

# Initialize Flask app
app = Flask(__name__)

# Initialize Dash app inside Flask
bootstrap_theme = dbc.themes.BOOTSTRAP
dash_app = dash.Dash(__name__, server=app, external_stylesheets=[bootstrap_theme], external_scripts=["/static/script.js"], routes_pathname_prefix="/general-info/")
dash_app.title = "Redalyze Dashboard"

# Global variable to store processed data
transformed_df = pd.DataFrame()
source = None

@app.route("/", methods=["GET", "POST"])
def index():
  global transformed_df
  global source
  if request.method == "POST":
    subreddits = request.form.get("subreddits")
    if subreddits:
      # Normalize input (replace spaces & commas with '+')
      subreddits = subreddits.replace(",", " ").replace("+", " ").split()
      subreddits = "+".join(subreddits)
      source = subreddits.split("+")

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
        }
        for post in raw_data
      ]

      transformed_df = transform_data.load_and_transform(pd.DataFrame(flat_data))

    return redirect(url_for('general_info'))

  return render_template("index.html")

@app.route("/general-info/")
def general_info():
  return dash_app.index()

@app.route('/api/interpret', methods=['POST'])
def interpret():
    data = request.json
    print("Received data for AI interpretation:", data)
    # Call Google Gemini API here and process the data
    return jsonify({"message": "Data received", "input": data})

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)
  
# Dash Layout
def create_layout():
  """Dynamically creates the Dash layout after data is set."""
  if transformed_df.empty:
    return html.Div([html.H2("No data available. Please enter a subreddit on the homepage.")])

  layout = dash_layout(html)
  return layout


# Callback for rendering different pages (This must be defined on `dash_app`)
@dash_app.callback(
  Output("page-content", "children"),
  [Input("url", "pathname")]
)
def render_page_content(pathname):
  vs = PlotService(transformed_df)
  global source
  
  return handle_routing(pathname, vs, source)
  

# Add dcc.Location for URL management
dash_app.layout = html.Div([
  dcc.Location(id="url", refresh=True),  # This listens to URL changes
  dash_layout(html)  # The layout we defined earlier
])

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

