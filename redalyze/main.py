import os
import dash
import pandas as pd
from dash import html, dcc
from flask import Flask, session
from flask_session import Session
from dash_layout import dash_layout
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from routes.flask_routes import flask_routes
from routes.dash_routes import handle_routing
from services.plot_service import PlotService

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Flask session requires a secret key

# Use Flask-Session for server-side session storage
app.config['SESSION_TYPE'] = 'filesystem'  # Or 'redis' if you prefer Redis
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
Session(app)  # Initialize Flask-Session

# Initialize Dash app inside Flask
bootstrap_theme = dbc.themes.BOOTSTRAP
dash_app = dash.Dash(__name__, server=app, external_stylesheets=[bootstrap_theme], external_scripts=["/static/script.js"], routes_pathname_prefix="/general-info/")
dash_app.title = "Redalyze Dashboard"

# Initialize routes with the necessary arguments
flask_routes(app)

# Dash Layout
def create_layout():
  """Dynamically creates the Dash layout after data is set."""
  if 'transformed_df' not in session or pd.DataFrame.from_dict(session['transformed_df']).empty:
    return html.Div([html.H2("No data available. Please enter a subreddit on the homepage.")])

  layout = dash_layout(html)
  return layout

# Callback for rendering different pages (This must be defined on `dash_app`)
@dash_app.callback(
  Output("page-content", "children"),
  [Input("url", "pathname")]
)
def render_page_content(pathname):
  vs = PlotService(pd.DataFrame.from_dict(session['transformed_df'])) if session.get('transformed_df') else PlotService(pd.DataFrame())
  session.get('source', [])
  session.get('plot_data', {})

  return handle_routing(pathname, vs)

# Add dcc.Location for URL management
dash_app.layout = html.Div([
  dcc.Location(id="url", refresh=True),  # This listens to URL changes
  dash_layout(html)  # The layout we defined earlier
])

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
