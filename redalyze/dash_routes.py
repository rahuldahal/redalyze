from dash import html, dcc

# Function to generate interpretation button
def generate_interpretation_button(data_property):
  return html.Button(
    "Interpret with AI", 
    className="btn btn-primary interepet-trigger mb-3", 
    id=f"interpret_{data_property}",
    **{'data-property': data_property}  # Add the data-property attribute dynamically
  )

# Function to handle saving data to localStorage
def save_data_to_store(data_property, data):
  # If the data is a Plotly figure, convert it to JSON first
  if hasattr(data, 'to_json'):
    data = data.to_json()

  return dcc.Store(id=f"store-{data_property}", data=data)

# The main routing function
def handle_routing(pathname, vs, source):
  if pathname == "/general-info/":
    return html.Div([
      html.H2("Data taken from the following subreddits:"),
      *[html.A(
        id=f"subreddit_link_{index}",
        children=subreddit,
        href=f"https://www.reddit.com/r/{subreddit}/",
        target="_blank",
        className="h3 text-primary d-block mb-2",
      ) for index, subreddit in enumerate(source)],
    ])

  elif pathname == "/subreddit-activity":
    sub_by_post_count = vs.get_sub_by_post_plot()
    post_frequency_overtime = vs.get_post_frequency_plot()

    return html.Div([
      html.H2("Most active subreddits"),
      dcc.Graph(figure=sub_by_post_count),
      save_data_to_store('sub_by_post_count', sub_by_post_count),
      generate_interpretation_button('sub_by_post_count'),
      html.H2("Post frequency overtime on different subreddits"),
      dcc.Graph(figure=post_frequency_overtime),
      save_data_to_store('post_frequency_overtime', post_frequency_overtime),
      generate_interpretation_button('post_frequency_overtime'),
      html.Script(src="/assets/script.js")
    ])

  elif pathname == "/engagement-analysis":
    scatter_plot = vs.get_scatter_plot_plot()
    score_upvote_plot = vs.get_score_upvote_plot()

    return html.Div([
      html.H2("Relationship Between Score and Comments"),
      dcc.Graph(figure=scatter_plot),
      save_data_to_store('scatter_plot', scatter_plot),
      generate_interpretation_button('scatter_plot'),
      html.H2("Correlation Between Score and Upvote Ratio"),
      dcc.Graph(figure=score_upvote_plot),
      save_data_to_store('score_upvote_plot', score_upvote_plot),
      generate_interpretation_button('score_upvote_plot'),
      html.Script(src="/assets/script.js")
    ])

  elif pathname == "/temporal-patterns":
    avg_score_overtime = vs.get_avg_score_overtime_plot()
    hourly_posts_plot = vs.get_hourly_posts_plot()

    return html.Div([
      html.H2("Average score over time"),
      dcc.Graph(figure=avg_score_overtime),
      save_data_to_store('avg_score_overtime', avg_score_overtime),
      generate_interpretation_button('avg_score_overtime'),
      html.H2("Post distribution over time"),
      dcc.Graph(figure=hourly_posts_plot),
      save_data_to_store('hourly_posts_plot', hourly_posts_plot),
      generate_interpretation_button('hourly_posts_plot'),
      html.Script(src="/assets/script.js")
    ])

  elif pathname == "/top-posts":
    top_posts_plot = vs.get_top_posts_plot()
    word_frequencies_plot = vs.get_word_frequencies_plot()

    return html.Div([
      html.H2("Top 10 Posts by Score"),
      dcc.Graph(figure=top_posts_plot),
      save_data_to_store('top_posts_plot', top_posts_plot),
      generate_interpretation_button('top_posts_plot'),
      html.H2("Most used words in titles"),
      dcc.Graph(figure=word_frequencies_plot),
      save_data_to_store('word_frequencies_plot', word_frequencies_plot),
      generate_interpretation_button('word_frequencies_plot'),
      html.Script(src="/assets/script.js")
    ])

  elif pathname == "/author-analysis":
    top_authors_plot = vs.get_top_authors_plot()
    author_contributions_plot = vs.get_author_contributions_plot()

    return html.Div([
      html.H2("Top 10 Authors by Total Posts"),
      dcc.Graph(figure=top_authors_plot),
      save_data_to_store('top_authors_plot', top_authors_plot),
      generate_interpretation_button('top_authors_plot'),
      html.H2("Network of Authors and Subreddits"),
      dcc.Graph(figure=author_contributions_plot),
      save_data_to_store('author_contributions_plot', author_contributions_plot),
      generate_interpretation_button('author_contributions_plot'),
      html.Script(src="/assets/script.js")
    ])

  elif pathname == "/engagement-correlation":
    correlation_heatmap_plot = vs.get_correlation_heatmap_plot()

    return html.Div([
      html.H2("Correlation Heatmap: Score, Comments, Upvote Ratio"),
      dcc.Graph(figure=correlation_heatmap_plot),
      save_data_to_store('correlation_heatmap_plot', correlation_heatmap_plot),
      generate_interpretation_button('correlation_heatmap_plot'),
      html.Script(src="/assets/script.js")
    ])

  return html.Div([
    html.H1("404: Not found", className="text-danger"),
    html.Hr(),
    html.P(f"The pathname {pathname} was not recognised..."),
  ], className="p-3 bg-light rounded-3")
