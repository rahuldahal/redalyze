from flask import session
from dash import html, dcc

def generate_interpretation_button(data_property):
  return html.Button(
    "Interpret with AI", 
    className="btn btn-primary interepet-trigger mb-3", 
    id=f"{data_property}"
  )
  
def generate_markdown_container(data_property):
  return html.Div(
    children=[
      html.Div(id=f"loading_{data_property}", 
               children=html.Div(className="spinner-border text-primary", role="status"),
               style={"display": "none"}), 
      html.Div(id=f"markdown_{data_property}", className="markdown-body", style={"display": "none"})
    ]
  )

def handle_routing(pathname, vs):
  if 'plot_data' not in session:
    session['plot_data'] = {}
    
  session['plot_data'].clear()
  
  if pathname == "/general-info/":
    return html.Div([
      html.H2("Data taken from the following subreddits:"),
      *[html.A(
        id=f"subreddit_link_{index}",
        children=subreddit,
        href=f"https://www.reddit.com/r/{subreddit}/",
        target="_blank",
        className="h3 text-primary d-block mb-2",
      ) for index, subreddit in enumerate(session['source'])],
    ])

  elif pathname == "/subreddit-activity":
    sub_by_post_count = vs.get_sub_by_post_plot()
    post_frequency_overtime = vs.get_post_frequency_plot()
    session['plot_data']['sub_by_post_count'] = sub_by_post_count
    session['plot_data']['post_frequency_overtime'] = post_frequency_overtime

    return html.Div([
      html.H2("Most active subreddits"),
      dcc.Graph(figure=sub_by_post_count),
      generate_interpretation_button('sub_by_post_count'),
      generate_markdown_container('sub_by_post_count'),
      html.H2("Post frequency overtime on different subreddits"),
      dcc.Graph(figure=post_frequency_overtime),
      generate_interpretation_button('post_frequency_overtime'),
      generate_markdown_container('post_frequency_overtime'),
    ])

  elif pathname == "/engagement-analysis":
    scatter_plot = vs.get_scatter_plot_plot()
    score_upvote_plot = vs.get_score_upvote_plot()
    session['plot_data']['scatter_plot'] = scatter_plot
    session['plot_data']['score_upvote_plot'] = score_upvote_plot

    return html.Div([
      html.H2("Relationship Between Score and Comments"),
      dcc.Graph(figure=scatter_plot),
      generate_interpretation_button('scatter_plot'),
      generate_markdown_container('scatter_plot'),
      html.H2("Correlation Between Score and Upvote Ratio"),
      dcc.Graph(figure=score_upvote_plot),
      generate_interpretation_button('score_upvote_plot'),
      generate_markdown_container('score_upvote_plot'),
    ])

  elif pathname == "/temporal-patterns":
    avg_score_overtime = vs.get_avg_score_overtime_plot()
    hourly_posts_plot = vs.get_hourly_posts_plot()
    session['plot_data']['avg_score_overtime'] = avg_score_overtime
    session['plot_data']['hourly_posts_plot'] = hourly_posts_plot

    return html.Div([
      html.H2("Average score over time"),
      dcc.Graph(figure=avg_score_overtime),
      generate_interpretation_button('avg_score_overtime'),
      generate_markdown_container('avg_score_overtime'),
      html.H2("Post distribution over time"),
      dcc.Graph(figure=hourly_posts_plot),
      generate_interpretation_button('hourly_posts_plot'),
      generate_markdown_container('hourly_posts_plot'),
    ])

  elif pathname == "/top-posts":
    top_posts_plot = vs.get_top_posts_plot()
    word_frequencies_plot = vs.get_word_frequencies_plot()
    session['plot_data']['top_posts_plot'] = top_posts_plot
    session['plot_data']['word_frequencies_plot'] = word_frequencies_plot

    return html.Div([
      html.H2("Top 10 Posts by Score"),
      dcc.Graph(figure=top_posts_plot),
      generate_interpretation_button('top_posts_plot'),
      generate_markdown_container('top_posts_plot'),
      html.H2("Most used words in titles"),
      dcc.Graph(figure=word_frequencies_plot),
      generate_interpretation_button('word_frequencies_plot'),
      generate_markdown_container('word_frequencies_plot'),
    ])

  elif pathname == "/author-analysis":
    top_authors_plot = vs.get_top_authors_plot()
    author_contributions_plot = vs.get_author_contributions_plot()
    session['plot_data']['top_authors_plot'] = top_authors_plot
    session['plot_data']['author_contributions_plot'] = author_contributions_plot

    return html.Div([
      html.H2("Top 10 Authors by Total Posts"),
      dcc.Graph(figure=top_authors_plot),
      generate_interpretation_button('top_authors_plot'),
      generate_markdown_container('top_authors_plot'),
      html.H2("Network of Authors and Subreddits"),
      dcc.Graph(figure=author_contributions_plot),
      generate_interpretation_button('author_contributions_plot'),
      generate_markdown_container('author_contributions_plot'),
    ])

  elif pathname == "/engagement-correlation":
    correlation_heatmap_plot = vs.get_correlation_heatmap_plot()
    session['plot_data']['correlation_heatmap_plot'] = correlation_heatmap_plot

    return html.Div([
      html.H2("Correlation Heatmap: Score, Comments, Upvote Ratio"),
      dcc.Graph(figure=correlation_heatmap_plot),
      generate_interpretation_button('correlation_heatmap_plot'),
      generate_markdown_container('correlation_heatmap_plot'),
    ])

  return html.Div([
    html.H1("404: Not found", className="text-danger"),
    html.Hr(),
    html.P(f"The pathname {pathname} was not recognised..."),
  ], className="p-3 bg-light rounded-3")
