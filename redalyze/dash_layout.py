import dash_bootstrap_components as dbc

def dash_layout(html):
  sidebar = html.Div(
    [
      html.H2("Redalyze", className="display-4 text-center mb-4"),
      html.Hr(),
      dbc.Nav(
        [
          dbc.NavLink("Subreddit Activity", href="/page-1", active="exact", className="nav-item nav-link"),
          dbc.NavLink("Engagement Analysis", href="/page-2", active="exact", className="nav-item nav-link"),
          dbc.NavLink("Temporal Patterns", href="/page-3", active="exact", className="nav-item nav-link"),
          dbc.NavLink("Top Posts", href="/page-4", active="exact", className="nav-item nav-link"),
          dbc.NavLink("Word Frequencies", href="/page-5", active="exact", className="nav-item nav-link"),
          dbc.NavLink("Top Authors", href="/page-6", active="exact", className="nav-item nav-link"),
          dbc.NavLink("Author per subreddit", href="/page-7", active="exact", className="nav-item nav-link"),
          dbc.NavLink("Correlation Analysis", href="/page-8", active="exact", className="nav-item nav-link"),
        ],
        vertical=True,
        pills=True,
        className="flex-column",
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
      "box-shadow": "2px 0px 5px rgba(0, 0, 0, 0.1)",
    },
    className="d-flex flex-column align-items-start",
  )

  content = html.Div(id="page-content", style={
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
  })

  # Combining sidebar and content
  return html.Div([sidebar, content])
