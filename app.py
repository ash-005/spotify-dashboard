from flask import Flask, render_template, request
from utils.data_loader import load_data, load_fixed_genres
from visualizations.genre_trends import genre_distribution, genre_evolution_by_year
from visualizations.popularity_analysis import artist_vs_track_popularity, popularity_distribution
from visualizations.duration_analysis import duration_distribution, duration_by_genre
from visualizations.artist_analysis import most_frequent_artists, artist_popularity_genre
from visualizations.additional_analysis import (
    explicit_distribution, release_year_distribution,
    top_albums, followers_vs_popularity
)
from datetime import datetime

app = Flask(__name__)

print("Loading data...")
df = load_data()
fixed_genres_df = load_fixed_genres()

print("Updating genres...")
try:
    missing_genres_mask = df['genres'].apply(lambda x: not x)
    if not fixed_genres_df.empty:
        genres_map = fixed_genres_df.drop_duplicates('id').set_index('id')['genres']
        updates = df.loc[missing_genres_mask, 'id'].map(genres_map)
        df.loc[missing_genres_mask & updates.notna(), 'genres'] = updates[updates.notna()]
except Exception as e:
    print(f"Warning: Error updating genres: {str(e)}")


def compute_stats(data):
    """Compute summary stats for the hero cards."""
    total = len(data)
    artists = data['artist_name'].nunique()
    genres_all = data['genres'].apply(lambda x: x if isinstance(x, list) else []).explode()
    top_genre = genres_all.value_counts().idxmax() if not genres_all.empty else 'N/A'
    avg_pop = round(data['popularity'].mean(), 1)
    avg_dur = round(data['duration_ms'].mean() / 60000, 1)
    top_artist = data['artist_name'].value_counts().idxmax()
    return dict(
        total_tracks=total, unique_artists=artists, top_genre=top_genre,
        avg_popularity=avg_pop, avg_duration=avg_dur, top_artist=top_artist,
    )


@app.route('/')
def index():
    try:
        pop_min = float(request.args.get('popularity_min', 0))
        pop_max = float(request.args.get('popularity_max', 100))
        pop_range = (pop_min, pop_max)

        stats = compute_stats(df)
        viz = {'popularity_range': pop_range, **stats}

        chart_fns = [
            ('genre_chart', lambda: genre_distribution(df, pop_range)),
            ('pop_chart', lambda: artist_vs_track_popularity(df)),
            ('duration_chart', lambda: duration_distribution(df)),
            ('duration_by_genre', lambda: duration_by_genre(df, pop_range)),
            ('genre_evolution', lambda: genre_evolution_by_year(df)),
            ('most_frequent_artists', lambda: most_frequent_artists(df)),
            ('artist_popularity_genre', lambda: artist_popularity_genre(df)),
            ('explicit_chart', lambda: explicit_distribution(df)),
            ('release_year_chart', lambda: release_year_distribution(df)),
            ('top_albums', lambda: top_albums(df)),
            ('followers_vs_pop', lambda: followers_vs_popularity(df)),
        ]
        pop_dist_fn = lambda: popularity_distribution(df)

        for key, fn in chart_fns:
            try:
                viz[key] = fn()
            except Exception as e:
                print(f"Error generating {key}: {e}")
                viz[key] = f"<div class='error-message'>Error loading {key}</div>"

        try:
            viz['artist_pop_dist'], viz['track_pop_dist'] = pop_dist_fn()
        except Exception as e:
            print(f"Error generating popularity distributions: {e}")
            viz['artist_pop_dist'] = viz['track_pop_dist'] = "<div class='error-message'>Error</div>"

        viz['current_date'] = datetime.now().strftime('%B %d, %Y')
        return render_template('index.html', **viz)
    except Exception as e:
        print(f"Error generating dashboard: {e}")
        return render_template('error.html', error=str(e))


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8088)