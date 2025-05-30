
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI', 'http://localhost:8000/callback')

# Scope for accessing user's top tracks and artist info
SCOPE = 'user-top-read'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))


def get_top_tracks(limit=100, time_range='medium_term'):
    # Spotify API returns max 50 tracks per request, so we need to paginate
    tracks = []
    for offset in range(0, limit, 50):
        response = sp.current_user_top_tracks(limit=min(50, limit - offset), offset=offset, time_range=time_range)
        items = response['items'] if response and 'items' in response and response['items'] is not None else []
        tracks.extend(items)
        if len(items) < 50:
            break
    return tracks


# Helper to get artist details (genres, popularity, followers)
def get_artist_details(artist_id):
    try:
        artist = sp.artist(artist_id)
        if artist is not None:
            return {
                'artist_id': artist['id'],
                'artist_name': artist['name'],
                'genres': artist.get('genres', []),
                'popularity': artist.get('popularity', None),
                'followers': artist.get('followers', {}).get('total', None)
            }
        else:
            return None
    except Exception:
        return None


# Helper to get song details in the requested format
def get_track_details(track):
    # Get artist details for all artists
    artists = []
    for artist in track.get('artists', []):
        details = get_artist_details(artist['id'])
        if details:
            artists.append(details)
        else:
            artists.append({
                'artist_id': artist['id'],
                'artist_name': artist['name'],
                'genres': [],
                'popularity': None,
                'followers': None
            })
    return {
        'track_id': track['id'],
        'track_name': track['name'],
        'popularity': track.get('popularity'),
        'duration_ms': track.get('duration_ms'),
        'explicit': track.get('explicit'),
        'release_date': track.get('album', {}).get('release_date', ''),
        'album_name': track.get('album', {}).get('name', ''),
        'artists': artists,
        'spotify_url': track.get('external_urls', {}).get('spotify', '')
    }


if __name__ == '__main__':
    top_tracks = get_top_tracks(limit=500)
    print("Fetching artist details for all tracks. This may take a while...")
    all_details = []
    for track in top_tracks:
        details = get_track_details(track)
        all_details.append(details)
    # Save as JSON
    with open('top_500songs_detailed.json', 'w', encoding='utf-8') as f:
        json.dump(all_details, f, ensure_ascii=False, indent=2)
    print("Saved detailed track data to top_500songs_detailed.json")