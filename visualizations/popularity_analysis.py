import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.caching import cache_plot
from .plot_utils import apply_dark_theme, SPOTIFY_COLORS, SEQUENTIAL_PALETTE, DIVERGING_PALETTE

@cache_plot(ttl_seconds=300)
def artist_vs_track_popularity(df):
    try:
        # Create hover text         
        hover_text = []
        for name, artist, album, art_pop, track_pop, url in zip(
            df['name'], df['artist_name'], df['album_name'],
            df['artist_popularity'], df['popularity'], df['spotify_url']
        ):
            hover_text.append(
                f"Track: {name}<br>"
                f"Artist: {artist}<br>"
                f"Album: {album}<br>"
                f"Artist Popularity: {art_pop}<br>"
                f"Track Popularity: {track_pop}<br>"
                f"<a href='{url}' target='_blank'>Open in Spotify</a>"
            )

        fig = go.Figure()
        
        # Add scatter points
        fig.add_trace(go.Scatter(
            x=df['artist_popularity'],
            y=df['popularity'],
            name='Artists',
            mode='markers',
            marker=dict(
                size=8,
                color=df['popularity'],
                colorscale=SEQUENTIAL_PALETTE,
                showscale=True,
                colorbar=dict(
                    title=dict(
                        text='Track<br>Popularity',
                        side='right'
                    ),
                    thickness=15,
                    len=0.7,
                    bgcolor='rgba(0,0,0,0)'
                ),
                line=dict(
                    color=SPOTIFY_COLORS['dark_gray'],
                    width=1
                ),
                opacity=0.8
            ),
            text=hover_text,
            hovertemplate="%{text}<extra></extra>",
            
        ))
        
        # Add trend line
        z = np.polyfit(df['artist_popularity'], df['popularity'], 1)
        p = np.poly1d(z)
        x_range = np.array([df['artist_popularity'].min(), df['artist_popularity'].max()])
        
        fig.add_trace(go.Scatter(
            x=x_range,
            y=p(x_range),
            mode='lines',
            line=dict(
                color=SPOTIFY_COLORS['green'],
                dash='dash',
                width=2
            ),
            name='Trend Line',
            hovertemplate="Correlation Line<br>y = %.2fx + %.2f<extra></extra>" % (z[0], z[1])
        ))
          # Update layout
        fig.update_layout(
            title='Artist vs Track Popularity',
            xaxis_title='Artist Popularity Score',
            yaxis_title='Track Popularity Score',
            height=600,
            hovermode='closest',
            hoverlabel=dict(bgcolor="rgba(0,0,0,0.8)"),
            hoverdistance=100,
            clickmode='event+select',
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor='rgba(0,0,0,0.5)'
            )
        )
        
        # Apply dark theme
        apply_dark_theme(fig)
        
        return fig.to_html(full_html=False)
        
    except Exception as e:
        print(f"Error in artist_vs_track_popularity: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(
            text="Error loading popularity comparison",
            showarrow=False,
            font=dict(color=SPOTIFY_COLORS['light_gray'])
        )
        apply_dark_theme(fig)
        return fig.to_html(full_html=False)

@cache_plot(ttl_seconds=300)
def popularity_distribution(df):
    try:
        artist_fig = go.Figure()
        artist_fig.add_trace(go.Histogram(
            x=df['artist_popularity'],
            nbinsx=30,
            marker_color=SPOTIFY_COLORS['green'],
            opacity=0.8,
            marker_line=dict(color=SPOTIFY_COLORS['light_gray'], width=1),
            hovertemplate=(
                "Popularity Score: %{x}<br>" +
                "Number of Artists: %{y}<extra></extra>"
            )
        ))
        
        # Add mean line
        mean_artist_pop = df['artist_popularity'].mean()
        artist_fig.add_vline(
            x=mean_artist_pop,
            line_dash="dash",
            line_color=SPOTIFY_COLORS['light_gray'],
            annotation=dict(
                text=f"Mean: {mean_artist_pop:.1f}",
                font=dict(color=SPOTIFY_COLORS['light_gray'])
            )
        )
        
        artist_fig.update_layout(
            title='Distribution of Artist Popularity',
            xaxis_title='Artist Popularity Score',
            yaxis_title='Number of Artists',
            height=500,
            bargap=0.1
        )
        
        apply_dark_theme(artist_fig)
        
        # Track popularity histogram
        track_fig = go.Figure()
        
        track_fig.add_trace(go.Histogram(
            x=df['popularity'],
            nbinsx=30,
            marker_color=SPOTIFY_COLORS['green'],
            opacity=0.8,
            marker_line=dict(color=SPOTIFY_COLORS['light_gray'], width=1),
            hovertemplate=(
                "Popularity Score: %{x}<br>" +
                "Number of Tracks: %{y}<extra></extra>"
            )
        ))
        
        # Add mean line
        mean_track_pop = df['popularity'].mean()
        track_fig.add_vline(
            x=mean_track_pop,
            line_dash="dash",
            line_color=SPOTIFY_COLORS['light_gray'],
            annotation=dict(
                text=f"Mean: {mean_track_pop:.1f}",
                font=dict(color=SPOTIFY_COLORS['light_gray'])
            )
        )
        track_fig.update_layout(
            title='Distribution of Track Popularity',
            xaxis_title='Track Popularity Score',
            yaxis_title='Number of Tracks',
            height=500,
            bargap=0.1,
            hovermode='closest',
            hoverlabel=dict(bgcolor="rgba(0,0,0,0.8)"),
            hoverdistance=100,
            clickmode='event+select'
        )
        
        apply_dark_theme(track_fig)
        
        return artist_fig.to_html(full_html=False), track_fig.to_html(full_html=False)
        
    except Exception as e:
        print(f"Error in popularity_distribution: {str(e)}")
        error_fig = go.Figure()
        error_fig.add_annotation(
            text="Error loading popularity distribution",
            showarrow=False,
            font=dict(color=SPOTIFY_COLORS['light_gray'])
        )
        apply_dark_theme(error_fig)
        error_html = error_fig.to_html(full_html=False)
        return error_html, error_html