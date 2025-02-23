import pandas as pd
from config import get_gemini_key
from config import get_reddit_connection
from transform_data import load_and_transform
from services.genai_service import GenaiService
from flask import request, render_template, redirect, url_for, jsonify, send_from_directory, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

limiter = Limiter(get_remote_address)
cache = Cache(config={'CACHE_TYPE': 'simple'})

def flask_routes(app):
  limiter.init_app(app)
  cache.init_app(app)

  @app.route("/", methods=["GET", "POST"])
  def index():
    if request.method == "POST":
      subreddits = request.form.get("subreddits")
      if subreddits:
        subreddits = subreddits.replace(",", " ").replace("+", " ").split()
        subreddits = "+".join(subreddits)
        session['source'] = subreddits.split("+")
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
        transformed_df = load_and_transform(pd.DataFrame(flat_data))
        session['transformed_df'] = transformed_df.to_dict()

      return redirect(url_for('general_info'))
    return render_template("index.html")

  @app.route("/general-info/")
  def general_info():
    return redirect('/general-info/')

  @app.route('/api/interpret', methods=['POST'])
  @limiter.limit("5 per minute")
  def interpret():
    plot_type = request.json.get('plot_type')

    cached_response = cache.get(plot_type)
    if cached_response:
      return jsonify({"message": cached_response, "cached": True})

    if plot_type in session['plot_data']:
      plot_type_meaning = {
        'sub_by_post_count': 'Barchart of subreddits by no. of posts',
        'post_frequency_overtime': 'Linechart of post frequency overtime on subreddits',
        'scatter_plot': 'Scatter plot of score vs comments',
        'score_upvote_plot': 'Correlation of score vs upvote ratio',
        'avg_score_overtime': 'Linechart of average score overtime',
        'hourly_posts_plot': 'Linechart of post distribution per hour',
        'top_posts_plot': 'DataTable of top posts',
        'word_frequencies_plot': 'Word cloud of word frequencies',
        'top_authors_plot': 'Barchart of top authors by no. of posts',
        'author_contribution_plot': 'Network graph of authors on subreddits',
        'correlation_heatmap_plot': 'Correlation: Score, Comments, Upvote Ratio',
      }
      gs = GenaiService(api_key=get_gemini_key())
      genai_response = gs.interpret_data(session['plot_data'][plot_type], plot_type_meaning[plot_type])

      cache.set(plot_type, genai_response, timeout=30)
      return jsonify({"message": genai_response, "cached": False})

    return jsonify({"message": "No data available for interpretation."})

  @app.route('/static/<path:path>')
  def serve_static(path):
    return send_from_directory('static', path)
