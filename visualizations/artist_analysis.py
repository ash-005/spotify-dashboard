import plotly.graph_objects as go
import pandas as pd
from .plot_utils import apply_dark_theme, SPOTIFY_COLORS, QUALITATIVE_PALETTE
from utils.caching import cache_plot
# my top 20 lesgoo
@cache_plot(ttl_seconds=300)
def most_frequent_artists(df: pd.DataFrame, top_n: int = 15) -> str:
    try:
       
        artist_counts = df['artist_name'].value_counts().head(top_n)
        fig = go.Figure()
        
        # Add bars
        fig.add_trace(go.Bar(
            x=artist_counts.values,
            y=artist_counts.index,
            orientation='h',
            marker_color=SPOTIFY_COLORS['green'],
            opacity=0.8,
            marker_line=dict(color=SPOTIFY_COLORS['light_gray'], width=1),
            customdata=artist_counts.index,  # For hover info
            hovertemplate=(
                "<b>%{customdata}</b><br>" +
                "Number of Tracks: %{x}<br>" +
                "<extra></extra>"
            )
        ))
        
        # Update layout
        fig.update_layout(
            title='Most Frequent Artists',
            xaxis_title='Number of Tracks',
            yaxis_title=None,
            height=400,
            bargap=0.2,
            showlegend=False,
            yaxis=dict(autorange="reversed")  # Reverse y-axis to show most frequent at top
        )
        apply_dark_theme(fig)
        
        return fig.to_html(full_html=False)
        
    except Exception as e:
        print(f"Error in most_frequent_artists: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(
            text="Error loading most frequent artists chart",
            showarrow=False,
            font=dict(color=SPOTIFY_COLORS['light_gray'])
        )
        apply_dark_theme(fig)
        return fig.to_html(full_html=False)

@cache_plot(ttl_seconds=300)
def artist_popularity_genre(df: pd.DataFrame) -> str:
    try:
        # Get artists with their track counts and mean popularity
        artist_stats = df.groupby('artist_name').agg({
            'artist_popularity': 'first',
            'id': 'count',
            'genres': 'first',
            'spotify_url': lambda x: list(x)[0]  # Keep first spotify URL for each artist
        }).reset_index()
        
        # Get main genre for each artist (first one listed)
        artist_stats['main_genre'] = artist_stats['genres'].apply(
            lambda x: x[0] if isinstance(x, list) and len(x) > 0 else 'Unknown'
        )
        
        # Get top genres for coloring
        top_genres = artist_stats['main_genre'].value_counts().head(7).index.tolist()
        artist_stats['color_genre'] = artist_stats['main_genre'].apply(
            lambda x: x if x in top_genres else 'Other'
        )
        
        # Create figure
        fig = go.Figure()
        
        # Add traces for each main genre
        for i, genre in enumerate(['Other'] + top_genres):  # Plot Other first
            genre_data = artist_stats[artist_stats['color_genre'] == genre]
            
            fig.add_trace(go.Scatter(
                x=genre_data['artist_popularity'],
                y=genre_data['id'],
                name=genre,
                mode='markers',
                marker=dict(
                    color=QUALITATIVE_PALETTE[i % len(QUALITATIVE_PALETTE)],
                    size=10,
                    opacity=0.7,
                    line=dict(color=SPOTIFY_COLORS['light_gray'], width=1)
                ),
                customdata=list(zip(
                    genre_data['artist_name'],
                    genre_data['main_genre'],
                    genre_data['spotify_url']
                )),
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>" +
                    "Tracks: %{y}<br>" +
                    "Popularity: %{x}<br>" +
                    "Genre: %{customdata[1]}<br>" +
                    "<a href='%{customdata[2]}' target='_blank'>Open in Spotify</a><br>" +
                    "<extra></extra>"
                )
            ))
        
        # Update layout
        fig.update_layout(            title='Artist Popularity vs Track Count by Genre',
            xaxis_title='Artist Popularity Score',
            yaxis_title='Number of Tracks',
            height=600,
            hovermode='closest',
            hoverlabel=dict(bgcolor="rgba(0,0,0,0.8)"),
            hoverdistance=100,
            clickmode='event+select',
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99,
                bgcolor='rgba(0,0,0,0.5)'
            )
        )
        
        # Apply theme
        apply_dark_theme(fig)
        
        return fig.to_html(full_html=False)
        
    except Exception as e:
        print(f"Error in artist_popularity_genre: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(
            text="Error loading artist popularity/genre chart",
            showarrow=False,
            font=dict(color=SPOTIFY_COLORS['light_gray'])
        )
        apply_dark_theme(fig)
        return fig.to_html(full_html=False)