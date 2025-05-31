import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.caching import cache_plot
from .plot_utils import apply_dark_theme, SPOTIFY_COLORS, QUALITATIVE_PALETTE

@cache_plot(ttl_seconds=300)
def genre_cooccurrence_network(df: pd.DataFrame, top_n: int = 15) -> str:
    """
    Plot a network graph of genre co-occurrences per artist.
    Nodes: genres. Edges: number of artists sharing both genres.
    Only top_n genres by frequency are shown for clarity.
    """
    import itertools
    import networkx as nx
    try:
        def parse_genres(x):
            if isinstance(x, str):
                try:
                    return eval(x) if x.startswith('[') else [x]
                except:
                    return [x]
            elif isinstance(x, list):
                return x
            else:
                return [str(x)]

        # Get top N genres
        genres_series = df['genres'].apply(parse_genres)
        all_genres = genres_series.explode().value_counts().head(top_n).index.tolist()

        # Build co-occurrence matrix (per artist)
        artist_genres = df.groupby('artist_name')['genres'].apply(lambda x: list(itertools.chain.from_iterable([parse_genres(g) for g in x]))).reset_index()
        # Only keep top genres
        artist_genres['genres'] = artist_genres['genres'].apply(lambda gs: [g for g in gs if g in all_genres])

        # Count co-occurrences
        cooccurrence = {}
        for genres in artist_genres['genres']:
            for g1, g2 in itertools.combinations(sorted(set(genres)), 2):
                key = tuple(sorted([g1, g2]))
                cooccurrence[key] = cooccurrence.get(key, 0) + 1

        # Build networkx graph
        G = nx.Graph()
        for genre in all_genres:
            G.add_node(genre)
        for (g1, g2), weight in cooccurrence.items():
            if weight > 0:
                G.add_edge(g1, g2, weight=weight)

        # Node positions (circular for clarity)
        pos = nx.circular_layout(G)

        # Plotly edge traces
        edge_x = []
        edge_y = []
        edge_weights = []
        for edge in G.edges(data=True):
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]
            edge_weights.append(edge[2]['weight'])

        # Normalize edge width
        max_weight = max(edge_weights) if edge_weights else 1
        edge_widths = [2 + 6 * (w / max_weight) for w in edge_weights]

        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=1, color=SPOTIFY_COLORS['light_gray']),
            hoverinfo='none',
            mode='lines',
            opacity=0.5
        )

        # Plotly node traces
        node_x = []
        node_y = []
        node_text = []
        for i, genre in enumerate(G.nodes()):
            x, y = pos[genre]
            node_x.append(x)
            node_y.append(y)
            node_text.append(f"<b>{genre}</b><br>Appears with: " + ", ".join([g for g in G.neighbors(genre)]))

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers+text',
            text=[g for g in G.nodes()],
            textposition='bottom center',
            hoverinfo='text',
            marker=dict(
                color=[QUALITATIVE_PALETTE[i % len(QUALITATIVE_PALETTE)] for i in range(len(G.nodes()))],
                size=30,
                line=dict(width=2, color=SPOTIFY_COLORS['black'])
            ),
            hovertext=node_text
        )

        fig = go.Figure(data=[edge_trace, node_trace])
        fig.update_layout(
            title='Genre Combo Generator: Genre Co-occurrence Network',
            showlegend=False,
            height=700,
            margin=dict(l=40, r=40, t=60, b=40),
            plot_bgcolor=SPOTIFY_COLORS['dark_gray'],
            paper_bgcolor=SPOTIFY_COLORS['black'],
            font=dict(color=SPOTIFY_COLORS['white']),
            hoverlabel=dict(
                bgcolor=SPOTIFY_COLORS['dark_gray'],
                font_size=14,
                font_family="Segoe UI"
            ),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
        return fig.to_html(full_html=False)
    except Exception as e:
        print(f"Error in genre_cooccurrence_network: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(
            text="Error loading genre co-occurrence network",
            showarrow=False,
            font=dict(color=SPOTIFY_COLORS['light_gray'])
        )
        apply_dark_theme(fig)
        return fig.to_html(full_html=False)
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.caching import cache_plot
from .plot_utils import apply_dark_theme, SPOTIFY_COLORS, QUALITATIVE_PALETTE

@cache_plot(ttl_seconds=300)
def genre_distribution(df: pd.DataFrame, popularity_range: tuple[float, float] | None = None) -> str:
    try:
        if popularity_range:
            df = df[(df['popularity'] >= popularity_range[0]) & 
                   (df['popularity'] <= popularity_range[1])]
        def parse_genres(x):
            if isinstance(x, str):
                try:
                    return eval(x) if x.startswith('[') else [x]
                except:
                    return [x]
            elif isinstance(x, list):
                return x
            else:
                return [str(x)]
        genres_series = df['genres'].apply(parse_genres).explode()
        genre_counts = genres_series.value_counts().nlargest(20)
        fig = go.Figure()
        genre_popularity = df.explode('genres').groupby('genres')['popularity'].mean()
        
        fig.add_trace(go.Bar(
            x=genre_counts.index,
            y=genre_counts.values,
            marker_color=SPOTIFY_COLORS['green'],
            marker_line_color=SPOTIFY_COLORS['light_gray'],
            marker_line_width=1,
            opacity=0.8,
            customdata=[[
                genre,
                genre_counts[genre],
                genre_popularity.get(genre, 0)
            ] for genre in genre_counts.index],
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>" +
                "Tracks: %{customdata[1]}<br>" +
                "Avg Popularity: %{customdata[2]:.1f}<br>" +
                "<extra></extra>"
            )
        ))
          # Update layout
        fig.update_layout(
            title='Top 20 Genres in Your Music',
            xaxis_title='Genre',
            yaxis_title='Number of Tracks',
            xaxis_tickangle=45,
            height=600,
            bargap=0.3,
            hoverlabel=dict(
                bgcolor=SPOTIFY_COLORS['dark_gray'],
                font_size=14,
                font_family="Segoe UI"
            ),
            hovermode='closest',
            hoverdistance=100,
            clickmode='event+select'
        )
        
        apply_dark_theme(fig)
        
    except Exception as e:
        print(f"Error in genre_distribution: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(
            text="Error loading genre distribution",
            showarrow=False,
            font=dict(color=SPOTIFY_COLORS['light_gray'])
        )
        apply_dark_theme(fig)
    
    return fig.to_html(full_html=False)

@cache_plot(ttl_seconds=300)
def genre_evolution_by_year(df: pd.DataFrame, top_n: int = 8) -> str:
    try:
        # Handle string representation of lists if they haven't been converted
        def parse_genres(x):
            if isinstance(x, str):
                try:
                    return eval(x) if x.startswith('[') else [x]
                except:
                    return [x]
            elif isinstance(x, list):
                return x
            else:
                return [str(x)]
        
        df = df.assign(genres=df['genres'].apply(parse_genres))
      
        top_genres = df['genres'].explode().value_counts().nlargest(top_n).index.tolist()
        
        plot_df = df.explode('genres')
        plot_df = plot_df[plot_df['genres'].isin(top_genres)]
        genre_years = plot_df.groupby(['release_year', 'genres']).agg({
            'id': 'count',
            'popularity': 'mean',
            'name': lambda x: '<br>'.join(
                f"• {name} (<a href='{url}' target='_blank'>Spotify</a>)"
                for name, url in zip(x.head(3), plot_df.loc[x.index].head(3)['spotify_url'])
            )
        }).reset_index()
        
        # Create figure
        fig = go.Figure()
        
        # Add lines for each genre
        for i, genre in enumerate(top_genres):
            genre_data = genre_years[genre_years['genres'] == genre]
            
            fig.add_trace(go.Scatter(
                x=genre_data['release_year'],
                y=genre_data['id'],
                name=genre,
                mode='lines+markers',
                marker=dict(
                    color=QUALITATIVE_PALETTE[i % len(QUALITATIVE_PALETTE)],
                    size=8
                ),
                line=dict(
                    color=QUALITATIVE_PALETTE[i % len(QUALITATIVE_PALETTE)],
                    width=2
                ),
                customdata=list(zip(
                    genre_data['genres'],
                    genre_data['popularity'],
                    genre_data['name']
                )),
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>" +
                    "Year: %{x}<br>" +
                    "Tracks: %{y}<br>" +
                    "Avg Popularity: %{customdata[1]:.1f}<br><br>" +
                    "Sample tracks:<br>%{customdata[2]}" +
                    "<extra></extra>"
                )
            ))
        
        # Update layout
        fig.update_layout(
            title='Genre Evolution Over Time',
            xaxis_title='Year',
            yaxis_title='Number of Tracks',
            height=600,
            hovermode='closest',
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99,
                bgcolor='rgba(0,0,0,0.5)'
            ),
            hoverlabel=dict(
                bgcolor=SPOTIFY_COLORS['dark_gray'],
                font_size=14,
                font_family="Segoe UI"
            )
        )
        
        apply_dark_theme(fig)
        
        return fig.to_html(full_html=False)
        
    except Exception as e:
        print(f"Error in genre_evolution_by_year: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(
            text="Error loading genre evolution",
            showarrow=False,
            font=dict(color=SPOTIFY_COLORS['light_gray'])
        )
        apply_dark_theme(fig)
        return fig.to_html(full_html=False)