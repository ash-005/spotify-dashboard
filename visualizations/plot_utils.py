SPOTIFY_COLORS = {
    'green': '#1DB954',
    'black': '#191414',
    'dark_gray': '#282828',
    'light_gray': '#B3B3B3',
    'white': '#FFFFFF'
}

# Color palettes for different types of plots
SEQUENTIAL_PALETTE = ['#1DB954', '#1ed760', '#52eb80', '#86efa0', '#baf3c0']
DIVERGING_PALETTE = ['#FF4632', '#FF8A80', '#FFBDAF', '#B3B3B3', '#90F0B3', '#52CD7C', '#1DB954']
QUALITATIVE_PALETTE = ['#1DB954', '#FF4632', '#1E90FF', '#FFB100', '#E91E63', '#9C27B0', '#00BCD4']

def apply_dark_theme(fig):
    fig.update_layout(
        plot_bgcolor=SPOTIFY_COLORS['dark_gray'],
        paper_bgcolor=SPOTIFY_COLORS['black'],
        font=dict(color=SPOTIFY_COLORS['white']),
        title_x=0.5,
        title_font=dict(size=24),
        showlegend=True,
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)'
        )
    )
    
    # Update axes
    fig.update_xaxes(
        gridcolor=SPOTIFY_COLORS['light_gray'],
        gridwidth=0.2,
        zerolinecolor=SPOTIFY_COLORS['light_gray']
    )
    fig.update_yaxes(
        gridcolor=SPOTIFY_COLORS['light_gray'],
        gridwidth=0.2,
        zerolinecolor=SPOTIFY_COLORS['light_gray']
    )
    
    return fig