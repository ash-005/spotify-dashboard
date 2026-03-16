import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.caching import cache_plot
from .plot_utils import apply_dark_theme, SPOTIFY_COLORS, QUALITATIVE_PALETTE, SEQUENTIAL_PALETTE

@cache_plot(ttl_seconds=300)
def explicit_distribution(df: pd.DataFrame) -> str:
    try:
        explicit_counts = df['explicit'].map({True: 'Explicit', False: 'Clean'}).value_counts()
        
        fig = go.Figure(data=[go.Pie(
            labels=explicit_counts.index,
            values=explicit_counts.values,
            hole=0.6,
            marker=dict(
                colors=[SPOTIFY_COLORS['accent_pink'], SPOTIFY_COLORS['green_light']],
                line=dict(color='rgba(0,0,0,0)', width=2)
            ),
            textinfo='label+percent',
            textfont=dict(size=14, color='#fff'),
            hoverinfo='label+value',
            hovertemplate='<b>%{label}</b><br>Tracks: %{value} (%{percent})<extra></extra>'
        )])
        
        fig.update_layout(
            title='Explicit vs Clean Content',
            height=400,
            showlegend=False,
            margin=dict(t=50, b=20, l=20, r=20),
            annotations=[dict(text='Content<br>Rating', x=0.5, y=0.5, font_size=18, showarrow=False)]
        )
        apply_dark_theme(fig)
        return fig.to_html(full_html=False)
    except Exception as e:
        print(f"Error in explicit_distribution: {e}")
        return f"<div class='error-message'>Error loading chart</div>"

@cache_plot(ttl_seconds=300)
def release_year_distribution(df: pd.DataFrame) -> str:
    try:
        df_valid = df.dropna(subset=['release_year'])
        year_counts = df_valid['release_year'].value_counts().sort_index().reset_index()
        year_counts.columns = ['release_year', 'count']
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=year_counts['release_year'],
            y=year_counts['count'],
            mode='lines+markers',
            fill='tozeroy',
            fillcolor='rgba(29, 185, 84, 0.2)',
            line=dict(color=SPOTIFY_COLORS['green'], width=3),
            marker=dict(size=8, color=SPOTIFY_COLORS['white'], line=dict(width=2, color=SPOTIFY_COLORS['green'])),
            hovertemplate='<b>Year: %{x}</b><br>Tracks: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Tracks by Release Year',
            xaxis_title='Release Year',
            yaxis_title='Number of Tracks',
            height=450,
            hovermode='x unified'
        )
        apply_dark_theme(fig)
        return fig.to_html(full_html=False)
    except Exception as e:
        print(f"Error in release_year_distribution: {e}")
        return f"<div class='error-message'>Error loading chart</div>"

@cache_plot(ttl_seconds=300)
def top_albums(df: pd.DataFrame, top_n: int = 10) -> str:
    try:
        album_counts = df.groupby(['album_name', 'artist_name']).size().reset_index(name='count')
        album_counts = album_counts.sort_values('count', ascending=True).tail(top_n)
        
        fig = go.Figure(go.Bar(
            x=album_counts['count'],
            y=album_counts['album_name'] + ' <span style="color:#aaa; font-size:10px;">(' + album_counts['artist_name'] + ')</span>',
            orientation='h',
            marker=dict(
                color=album_counts['count'],
                colorscale=SEQUENTIAL_PALETTE,
                line=dict(color='rgba(0,0,0,0)', width=0)
            ),
            hovertemplate='<b>%{y}</b><br>Tracks in Top 500: %{x}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Albums with Most Top Tracks',
            xaxis_title='Number of Tracks',
            yaxis_title=None,
            height=500,
            margin=dict(l=20)
        )
        apply_dark_theme(fig)
        return fig.to_html(full_html=False)
    except Exception as e:
        print(f"Error in top_albums: {e}")
        return f"<div class='error-message'>Error loading chart</div>"

@cache_plot(ttl_seconds=300)
def followers_vs_popularity(df: pd.DataFrame) -> str:
    try:
        # Aggregate by artist to avoid duplicates
        artist_df = df.groupby('artist_name').agg({
            'artist_followers': 'first',
            'artist_popularity': 'first',
            'id': 'count'
        }).reset_index().rename(columns={'id': 'track_count'})
        
        artist_df = artist_df.dropna(subset=['artist_followers', 'artist_popularity'])
        
        fig = go.Figure(go.Scatter(
            x=artist_df['artist_followers'],
            y=artist_df['artist_popularity'],
            mode='markers',
            marker=dict(
                size=artist_df['track_count'] * 3 + 5,
                color=artist_df['track_count'],
                colorscale=SEQUENTIAL_PALETTE,
                showscale=True,
                colorbar=dict(title="Top Tracks", tickfont=dict(color='#fff')),
                opacity=0.8,
                line=dict(color=SPOTIFY_COLORS['white'], width=0.5)
            ),
            text=artist_df['artist_name'],
            customdata=artist_df['track_count'],
            hovertemplate='<b>%{text}</b><br>Followers: %{x:,.0f}<br>Popularity: %{y}<br>Top Tracks: %{customdata}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Artist Followers vs Popularity',
            xaxis_title='Total Followers',
            yaxis_title='Artist Popularity',
            xaxis_type='log',
            height=500
        )
        apply_dark_theme(fig)
        return fig.to_html(full_html=False)
    except Exception as e:
        print(f"Error in followers_vs_popularity: {e}")
        return f"<div class='error-message'>Error loading chart</div>"
