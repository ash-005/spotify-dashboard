SPOTIFY_COLORS = {
    'green': '#1DB954',
    'green_light': '#1ed760',
    'black': '#0a0a0a',
    'dark_gray': '#181818',
    'mid_gray': '#282828',
    'light_gray': '#B3B3B3',
    'white': '#FFFFFF',
    'accent_pink': '#E91E63',
    'accent_blue': '#1E90FF',
    'accent_purple': '#9C27B0',
    'accent_orange': '#FFB100',
    'accent_cyan': '#00BCD4',
}

SEQUENTIAL_PALETTE = ['#1DB954', '#1ed760', '#52eb80', '#86efa0', '#baf3c0']
DIVERGING_PALETTE = ['#FF4632', '#FF8A80', '#FFBDAF', '#B3B3B3', '#90F0B3', '#52CD7C', '#1DB954']
QUALITATIVE_PALETTE = [
    '#1DB954', '#FF4632', '#1E90FF', '#FFB100', '#E91E63',
    '#9C27B0', '#00BCD4', '#FF6F00', '#7C4DFF', '#00E676',
    '#FF5252', '#448AFF', '#FFAB40', '#F50057', '#D500F9',
]

MODERN_LAYOUT = dict(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter, system-ui, sans-serif', color='#e0e0e0', size=13),
    title_x=0.5,
    title_font=dict(size=20, color='#ffffff'),
    margin=dict(l=50, r=30, t=50, b=50),
    showlegend=True,
    legend=dict(
        bgcolor='rgba(255,255,255,0.05)',
        bordercolor='rgba(255,255,255,0.1)',
        borderwidth=1,
        font=dict(size=11)
    ),
    hoverlabel=dict(
        bgcolor='rgba(24,24,24,0.95)',
        bordercolor='rgba(29,185,84,0.5)',
        font=dict(family='Inter, sans-serif', size=13, color='#fff')
    ),
)

def apply_dark_theme(fig):
    fig.update_layout(**MODERN_LAYOUT)
    fig.update_xaxes(
        gridcolor='rgba(255,255,255,0.06)',
        gridwidth=1,
        zerolinecolor='rgba(255,255,255,0.1)',
        tickfont=dict(size=11, color='#999')
    )
    fig.update_yaxes(
        gridcolor='rgba(255,255,255,0.06)',
        gridwidth=1,
        zerolinecolor='rgba(255,255,255,0.1)',
        tickfont=dict(size=11, color='#999')
    )
    return fig