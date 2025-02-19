import dash_bootstrap_components as dbc
from dash import html, dcc

def dash_layout(html, dcc, vs):
  sidebar = html.Div(
    [
      html.H2("Redalyze", className="display-4"),
      html.Hr(),
      dbc.Nav(
        [
          dbc.NavLink("Subreddit Activity", href="/page-1", active="exact"),
          dbc.NavLink("Engagement Analysis", href="/page-2", active="exact"),
          dbc.NavLink("Temporal Patterns", href="/page-3", active="exact"),
          dbc.NavLink("Top Posts", href="/page-4", active="exact"),
          dbc.NavLink("Author Analysis", href="/page-5", active="exact"),
          dbc.NavLink("Correlation Analysis", href="/page-6", active="exact"),
        ],
        vertical=True,
        pills=True,
      ),
    ],
    style={
      "position": "fixed",
      "top": 0,
      "left": 0,
      "bottom": 0,
      "width": "16rem",
      "padding": "2rem 1rem",
      "background-color": "#f8f9fa",
    },
  )

  content = html.Div(id="page-content", style={
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
  })

  # Combining sidebar and content
  return html.Div([sidebar, content])
