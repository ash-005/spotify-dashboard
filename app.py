from flask import Flask, render_template, request
from utils.data_loader import load_data, load_fixed_genres
from visualizations.genre_trends import genre_distribution, genre_evolution_by_year
from visualizations.popularity_analysis import (
    artist_vs_track_popularity,
    popularity_distribution
)
from visualizations.duration_analysis import (
    duration_distribution,
    duration_by_genre
)
from visualizations.artist_analysis import (
    most_frequent_artists,
    artist_popularity_genre
)

app = Flask(__name__)

print("Loading data...")
df = load_data()
fixed_genres_df = load_fixed_genres()

print("Updating genres...")
try:
    missing_genres_mask = df['genres'].apply(lambda x: not x)
    
    if not fixed_genres_df.empty:
        # Create a mapping from id to genres, keeping only the first occurrence of each id
        genres_map = fixed_genres_df.drop_duplicates('id').set_index('id')['genres']
        
        # Update only the rows with missing genres using the mapping
        updates = df.loc[missing_genres_mask, 'id'].map(genres_map)
        df.loc[missing_genres_mask & updates.notna(), 'genres'] = updates[updates.notna()]
        
        #print(f"Updated {missing_genres_mask.sum()} tracks with missing genres")
except Exception as e:
    print(f"Warning: Error updating genres: {str(e)}")
    print("Continuing with original genres...")

@app.route('/')
def index():
    """Render the main dashboard page with all visualizations."""
    try:
        # Get popularity filter settings from query parameters
        popularity_min = float(request.args.get('popularity_min', 0))
        popularity_max = float(request.args.get('popularity_max', 100))
        popularity_range = (popularity_min, popularity_max)
        
        visualizations = {}
        visualizations['popularity_range'] = popularity_range
        
        try:
            visualizations['genre_chart'] = genre_distribution(df, popularity_range)
        except Exception as e:
            print(f"Error generating genre distribution: {str(e)}")
            visualizations['genre_chart'] = "<div class='error-message'>Error loading genre distribution</div>"

       
        try:
            visualizations['pop_chart'] = artist_vs_track_popularity(df)
        except Exception as e:
            print(f"Error generating popularity chart: {str(e)}")
            visualizations['pop_chart'] = "<div class='error-message'>Error loading popularity chart</div>"
            
        try:
            visualizations['duration_chart'] = duration_distribution(df)
        except Exception as e:
            print(f"Error generating duration chart: {str(e)}")
            visualizations['duration_chart'] = "<div class='error-message'>Error loading duration chart</div>"
            
        try:
            visualizations['duration_by_genre'] = duration_by_genre(df, popularity_range)
        except Exception as e:
            print(f"Error generating duration by genre: {str(e)}")
            visualizations['duration_by_genre'] = "<div class='error-message'>Error loading duration by genre chart</div>"
            
        try:
            visualizations['genre_evolution'] = genre_evolution_by_year(df)
        except Exception as e:
            print(f"Error generating genre evolution: {str(e)}")
            visualizations['genre_evolution'] = "<div class='error-message'>Error loading genre evolution</div>"
            
        try:
            visualizations['artist_pop_dist'], visualizations['track_pop_dist'] = popularity_distribution(df)
        except Exception as e:
            print(f"Error generating popularity distributions: {str(e)}")
            visualizations['artist_pop_dist'] = "<div class='error-message'>Error loading artist popularity distribution</div>"
            visualizations['track_pop_dist'] = "<div class='error-message'>Error loading track popularity distribution</div>"

        try:
            visualizations['most_frequent_artists'] = most_frequent_artists(df)
        except Exception as e:
            print(f"Error generating most frequent artists: {str(e)}")
            visualizations['most_frequent_artists'] = "<div class='error-message'>Error loading most frequent artists chart</div>"
            
        try:
            visualizations['artist_popularity_genre'] = artist_popularity_genre(df)
        except Exception as e:
            print(f"Error generating artist popularity by genre: {str(e)}")
            visualizations['artist_popularity_genre'] = "<div class='error-message'>Error loading artist popularity by genre chart</div>"
        
        from datetime import datetime
        visualizations['current_date'] = datetime.now().strftime('%B %d, %Y')

        return render_template('index.html', **visualizations)
    except Exception as e:
        print(f"Error generating dashboard: {str(e)}")
        return render_template('error.html', error=str(e))
if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)