import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.caching import cache_plot
from .plot_utils import apply_dark_theme, SPOTIFY_COLORS, QUALITATIVE_PALETTE

@cache_plot(ttl_seconds=300)
def duration_distribution(df):
    try:
        df = df.copy()
        df['duration_min'] = df['duration_ms'] / (1000 * 60) # to minutes
        fig = go.Figure()
        bins = np.histogram_bin_edges(df['duration_min'], bins=40)
        counts, _ = np.histogram(df['duration_min'], bins=bins)
        bin_centers = (bins[:-1] + bins[1:]) / 2
        
        # Get sample songs for each bin for hover info
        hover_data = []
        for i in range(len(bins)-1):
            mask = (df['duration_min'] >= bins[i]) & (df['duration_min'] < bins[i+1])
            bin_songs = df[mask].sort_values('popularity', ascending=False).head(3)
            hover_data.append([
                f"<b>{name}</b> by {artist}<br>"
                f"<a href='{url}' target='_blank'>Open in Spotify</a>"
                for name, artist, url in 
                zip(bin_songs['name'], bin_songs['artist_name'], bin_songs['spotify_url'])
            ])
        
        fig.add_trace(go.Bar(
            x=bin_centers,
            y=counts,
            name='Duration Distribution',
            marker_color=SPOTIFY_COLORS['green'],
            opacity=0.8,
            width=(bins[1] - bins[0]) * 0.9,
            marker_line=dict(color=SPOTIFY_COLORS['light_gray'], width=1),
            customdata=hover_data,
            hovertemplate=(
                "Duration: %{x:.1f} min<br>" +
                "Count: %{y}<br>" +
                "Sample tracks:<br>%{customdata[0]}" +
                "---<br>%{customdata[1]}" +
                "---<br>%{customdata[2]}" +
                "<extra></extra>"
            )
        ))
        mean_duration = df['duration_min'].mean() # mean song duration 
        fig.add_vline(
            x=mean_duration,
            line_dash="dash",
            line_color=SPOTIFY_COLORS['light_gray'],
            annotation_text=f"Mean: {mean_duration:.1f} min",
            annotation_position="top"
        )
        
        # Update layout
        fig.update_layout(
            title='Distribution of Track Durations',
            xaxis_title='Duration (minutes)',
            yaxis_title='Number of Tracks',
            height=500,
            bargap=0,
            showlegend=False,
            hoverlabel=dict(
                bgcolor=SPOTIFY_COLORS['dark_gray'],
                font_size=14,
                font_family="Segoe UI"
            ),
            hovermode='closest',
            hoverdistance=100,
            clickmode='event+select'
        )
        
        # Apply dark theme
        apply_dark_theme(fig)
        
        return fig.to_html(full_html=False)
    except Exception as e:
        print(f"Error in duration_distribution: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(
            text="Error loading duration distribution",
            showarrow=False,
            font=dict(color=SPOTIFY_COLORS['light_gray'])
        )
        apply_dark_theme(fig)
        return fig.to_html(full_html=False)

@cache_plot(ttl_seconds=300)
def duration_by_genre(df, popularity_range: tuple[float, float] | None = None):
    try:
     
        if popularity_range:
            df = df[(df['popularity'] >= popularity_range[0]) & 
                   (df['popularity'] <= popularity_range[1])]
        df = df.copy()
        df['duration_min'] = df['duration_ms'] / (1000 * 60)
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
        genre_counts = df.explode('genres')['genres'].value_counts()
        top_genres = genre_counts.head(15).index.tolist()
        
        plot_data = df.explode('genres')
        plot_data = plot_data[plot_data['genres'].isin(top_genres)]
        
        fig = go.Figure()
        
        for i, genre in enumerate(top_genres):
            genre_data = plot_data[plot_data['genres'] == genre]
            stats = {
                'median': genre_data['duration_min'].median(),
                'q1': genre_data['duration_min'].quantile(0.25),
                'q3': genre_data['duration_min'].quantile(0.75),
                'count': len(genre_data)
            }
            sample_tracks = genre_data.sort_values('popularity', ascending=False).head(3)
            sample_text = "<br>".join([
                f"<b>{name}</b> by {artist} ({dur:.1f} min)<br>"
                f"<a href='{url}' target='_blank'>Open in Spotify</a>"
                for name, artist, dur, url in 
                zip(sample_tracks['name'], sample_tracks['artist_name'], 
                    sample_tracks['duration_min'], sample_tracks['spotify_url'])
            ])
            
            fig.add_trace(go.Violin(
                x=genre_data['duration_min'],
                name=genre,
                orientation='h',
                side='positive',
                width=2,
                points='outliers',
                meanline=dict(visible=True, color=SPOTIFY_COLORS['white']),
                fillcolor=QUALITATIVE_PALETTE[i % len(QUALITATIVE_PALETTE)],
                line=dict(color=SPOTIFY_COLORS['light_gray']),
                opacity=0.7,
                customdata=[[
                    genre,
                    stats['median'],
                    stats['q1'],
                    stats['q3'],
                    stats['count'],
                    sample_text
                ]],
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>" +
                    "Median: %{customdata[1]:.1f} min<br>" +
                    "Q1-Q3: %{customdata[2]:.1f}-%{customdata[3]:.1f} min<br>" +
                    "Track count: %{customdata[4]}<br><br>" +
                    "Popular tracks in this genre:<br>%{customdata[5]}" +
                    "<extra></extra>"
                )
            ))
        
        # Update layout
        fig.update_layout(
            title='Track Duration Distribution by Genre',
            xaxis_title='Duration (minutes)',
            yaxis_title='Genre',
            height=600,
            showlegend=False,
            violingap=0.1,
            violingroupgap=0,
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
        
        return fig.to_html(full_html=False)
    except Exception as e:
        print(f"Error in duration_by_genre: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(
            text="Error loading duration by genre distribution",
            showarrow=False,
            font=dict(color=SPOTIFY_COLORS['light_gray'])
        )
        apply_dark_theme(fig)
        return fig.to_html(full_html=False)