import pandas as pd

def load_data(path='data/top_500songs_with_fixed_genres.csv'):

    encodings = ['utf-8-sig', 'latin1', 'iso-8859-1', 'cp1252']
    
    for encoding in encodings:
        try:
            df = pd.read_csv(path, encoding=encoding)
            
            # Rename columns to match expected names, distinguishing between artist and track data
            column_mapping = {
                'track_track_id': 'id',
                'track_track_name': 'name',
                'popularity': 'artist_popularity',  # Artist popularity
                'track_popularity': 'popularity',   # Track popularity
                'track_duration_ms': 'duration_ms',
                'track_explicit': 'explicit',
                'track_release_date': 'release_date',
                'track_album_name': 'album_name',
                'artist_name': 'artist_name',
                'followers': 'artist_followers',
                'track_spotify_url': 'spotify_url'
            }
            
            df = df.rename(columns=column_mapping)
              # Try different date formats
            for date_format in ['%d-%m-%Y', '%Y-%m-%d']:
                try:
                    df['release_date'] = pd.to_datetime(df['release_date'], format=date_format, dayfirst=True)
                    break
                except:
                    continue
            
            # If date parsing failed, try without format
            if not pd.api.types.is_datetime64_any_dtype(df['release_date']):
                df['release_date'] = pd.to_datetime(df['release_date'], dayfirst=True, errors='coerce')
            
            df['release_year'] = df['release_date'].dt.year
            
            # Convert string representations of lists to actual lists for genres
            df['genres'] = df['genres'].apply(lambda x: eval(x) if isinstance(x, str) and x.startswith('[') else ([x] if x and not pd.isna(x) else []))
            
            return df
            
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error reading file with {encoding} encoding: {str(e)}")
            continue
    
    raise ValueError(f"Could not read the CSV file with any of the attempted encodings: {encodings}")

def load_fixed_genres(path='data/top_500songs_with_fixed_genres.csv'):

    try:
        df = load_data(path)
        return df[['id', 'genres']]
    except Exception as e:
        print(f"Error loading fixed genres: {str(e)}")
        return pd.DataFrame(columns=['id', 'genres'])