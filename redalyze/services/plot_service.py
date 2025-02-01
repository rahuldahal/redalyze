import networkx as nx
import plotly.express as px
from dash import dash_table
import plotly.graph_objects as go

from filters.sub_by_post import sub_by_post
from filters.top_n_posts import top_n_posts
from filters.top_authors import top_authors
from filters.post_per_hour import post_per_hour
from filters.hour_score_mean import hour_score_mean
from filters.word_frequencies import word_frequencies
from filters.score_upvote_bins import score_upvote_grid
from filters.post_per_hour_per_sub import post_per_hour_per_sub
from filters.score_comment_upvote import score_comment_upvote
from filters.author_sub_network import author_sub_network

class PlotService:
    def __init__(self, transformed_df):
        self.df = transformed_df
    
    def get_sub_by_post_plot(self):
        df = sub_by_post(self.df)
        fig = px.bar(df, x='subreddit', y='total_posts', title='Top 10 Subreddits by no. of Posts')
        fig.update_layout(xaxis_title="Subreddit", yaxis_title="Metric Value")
        return fig

    def get_post_frequency_plot(self):
        fig = px.line(
            post_per_hour_per_sub(self.df),
            x='created_hour',
            y='total_posts',
            color='subreddit',
            title='Post Frequency Over Time by Subreddit',
            labels={'created_hour': 'Hour of Day', 'total_posts': 'Number of Posts'}
        )
        return fig

    def get_scatter_plot_plot(self):
        fig = px.scatter(
            self.df,
            x='score',
            y='num_comments',
            size='score',
            color='subreddit',
            title='Relationship Between Score and Total Comments',
            labels={'score': 'Score', 'num_comments': 'Total Comments'}
        )
        return fig

    def get_score_upvote_plot(self):
        heatmap_grid = score_upvote_grid(self.df)
        fig = px.imshow(
            heatmap_grid,
            labels=dict(x="Upvote Ratio Category", y="Score Category", color="Post Count")
        )
        fig.update_layout(title="Heatmap: Score vs Upvote Ratio")
        return fig

    def get_avg_score_overtime_plot(self):
        fig = px.line(
            hour_score_mean(self.df),
            x='created_hour',
            y='mean_score',
            title='Average Score Over Time',
            labels={'created_hour': 'Hour of Day', 'mean_score': 'Average Score'}
        )
        return fig

    def get_hourly_posts_plot(self):
        fig = px.histogram(post_per_hour(self.df), x='created_hour', y='total_posts')
        return fig

    def get_top_posts_plot(self):
        top_posts = top_n_posts(self.df, 10) # n = 10 -> Top 10
        return dash_table.DataTable(
            data=top_posts.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in top_posts.columns]
        )

    def get_word_frequencies_plot(self):
        fig = px.treemap(
            word_frequencies(self.df),
            path=["word"],
            values="frequency",
            title="Most Used Words in Titles"
        )
        return fig

    def get_top_authors_plot(self):
        authors = top_authors(self.df)
        fig = px.bar(authors, x='author', y='num_posts', title='Top 10 Authors by Posts')
        return fig

    def get_author_contributions_plot(self):
        G = nx.Graph()
        contributions_df = author_sub_network(self.df)

        for _, row in contributions_df.iterrows():
            G.add_edge(row["author"], row["subreddit"], weight=row["contributions"])

        pos = nx.spring_layout(G)
        node_x, node_y, node_labels, node_colors = [], [], [], []

        for node, coords in pos.items():
            node_x.append(coords[0])
            node_y.append(coords[1])
            node_labels.append(node)
            node_colors.append("blue" if node in set(contributions_df["author"]) else "orange")

        edge_x, edge_y = [], []
        for edge in G.edges(data=True):
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1.5, color="#888"), mode="lines")
        node_trace = go.Scatter(
            x=node_x, y=node_y, mode="markers+text", text=node_labels, textposition="top center",
            marker=dict(size=20, color=node_colors, line_width=2)
        )

        fig = go.Figure(data=[edge_trace, node_trace])
        fig.update_layout(showlegend=False, margin=dict(t=0, l=0, b=0, r=0))
        return fig

    def get_correlation_heatmap_plot(self):
        fig = px.imshow(
            score_comment_upvote(self.df),
            text_auto=True,
            color_continuous_scale='Viridis',
            labels=dict(x="Metrics", y="Metrics", color="Correlation"),
            title="Correlation Heatmap"
        )
        return fig
