import dash_bootstrap_components as dbc

def dash_layout(html):
  sidebar = html.Div(
    [
      html.H2("Redalyze", className="display-4 text-center mb-4"),
      html.Hr(),
      dbc.Nav(
        [
          dbc.NavLink("Subreddit Activity", href="/subreddit-activity", active="exact", className="nav-item nav-link"),
          dbc.NavLink("Engagement Analysis", href="/engagement-analysis", active="exact", className="nav-item nav-link"),
          dbc.NavLink("Temporal Patterns", href="/temporal-patterns", active="exact", className="nav-item nav-link"),
          dbc.NavLink("Top Posts", href="/top-posts", active="exact", className="nav-item nav-link"),
          dbc.NavLink("Top Authors", href="/author-analysis", active="exact", className="nav-item nav-link"),
          dbc.NavLink("Correlation Analysis", href="/engagement-correlation", active="exact", className="nav-item nav-link"),
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
