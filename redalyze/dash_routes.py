def handle_routing(pathname, dcc, html, vs, source):
  if pathname == "/general-info/":
    return html.Div([
      html.H2("Data taken from the following subreddits:"),
      *[html.A(
        id=f"subreddit_link_{i}",
        children=subreddit,
        href=f"https://www.reddit.com/r/{subreddit}/",
        target="_blank",
        className="h3 text-primary d-block mb-2",
      ) for i, subreddit in enumerate(source)]
  ])
  
  elif pathname == "/subreddit-activity":
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

  return html.Div([
    html.H1("404: Not found", className="text-danger"),
    html.Hr(),
    html.P(f"The pathname {pathname} was not recognised..."),
  ], className="p-3 bg-light rounded-3")
