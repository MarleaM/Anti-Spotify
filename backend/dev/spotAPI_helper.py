import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import pandas as pd
import numpy as np 
import time

load_dotenv()
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

metadata_ft = [
    "Track Name",
    "Artist",
    "Album",
    "Thumbnail URL",
    "Track ID",
    "id",
    "uri",
    "track_href",
    "analysis_url"
]


def get_thumbnail_url(track_name, artist_name):
    query = f"{track_name} {artist_name}"
    results = sp.search(q=query, type='track', limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        if track['album']['images']:
            return track['album']['images'][0]['url'], track['album']['name']
    return "", ""

def get_playlist_id(playlist_url):
    if 'playlist/' in playlist_url:
        return playlist_url.split('playlist/')[1].split('?')[0]
    else:
        raise ValueError("Invalid Spotify playlist URL.")

def fetch_playlist_tracks(playlist_id, limit=10):
    results = sp.playlist_tracks(playlist_id, limit=limit)
    return results['items']
    
def process_playlist(playlist_url, batch_size=50):
    """
    Processes the Spotify playlist and returns a list of track data.
    Handles large playlists by fetching tracks in batches using offsets.
    
    Parameters:
    - playlist_url (str): The Spotify playlist URL.
    - batch_size (int): Number of tracks to fetch per request (max 50).
    
    Returns:
    - List[dict]: A list of dictionaries containing track data and audio features.
    """
    try:
        playlist_id = get_playlist_id(playlist_url)
    except ValueError as ve:
        print(ve)
        return []
    
    # Initialize variables
    offset = 0
    total_tracks = None
    data = []
    all_track_ids = []
    
    print("Fetching playlist tracks...")
    
    while True:
        try:
            # Fetch a batch of tracks
            response = sp.playlist_tracks(playlist_id, offset=offset, limit=batch_size)
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 429:
                # Rate limit exceeded
                retry_after = int(e.headers.get('Retry-After', 5))
                print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                time.sleep(retry_after)
                continue
            else:
                print(f"Spotify API error: {e}")
                break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
        
        if total_tracks is None:
            total_tracks = response['total']
            print(f"Total tracks in playlist: {total_tracks}")
        
        tracks = response['items']
        if not tracks:
            break  # No more tracks to fetch
        
        for item in tracks:
            track = item['track']
            if track is None:
                continue  # Skip if track information is not available
            
            track_name = track['name']
            artist_names = ', '.join([artist['name'] for artist in track['artists']])
            album_name = track['album']['name']
            track_id = track['id']
            
            # Get thumbnail URL
            thumbnail_url, _ = get_thumbnail_url(track_name, artist_names)
            
            # Append track ID for fetching audio features
            if track_id:
                all_track_ids.append(track_id)
            
            # Prepare track data
            track_data = {
                'Track Name': track_name,
                'Artist': artist_names,
                'Album': album_name,
                'Thumbnail URL': thumbnail_url,
                'Track ID': track_id
            }
            data.append(track_data)
        
        offset += batch_size
        print(f"Fetched {min(offset, total_tracks)} / {total_tracks} tracks.")
        
        if offset >= total_tracks:
            break  # All tracks fetched
    
    print("Fetching audio features...")
    
    # Fetch audio features in batches
    for i in range(0, len(all_track_ids), 50):
        batch_ids = all_track_ids[i:i+50]
        try:
            audio_features = sp.audio_features(tracks=batch_ids)
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 429:
                retry_after = int(e.headers.get('Retry-After', 5))
                print(f"Rate limit exceeded while fetching audio features. Retrying after {retry_after} seconds.")
                time.sleep(retry_after)
                audio_features = sp.audio_features(tracks=batch_ids)
            else:
                print(f"Spotify API error while fetching audio features: {e}")
                audio_features = [None] * len(batch_ids)
        
        for j, features in enumerate(audio_features):
            index = i + j
            if features:
                for key, value in features.items():
                    data[index][key] = value
            else:
                print(f"No audio features found for Track ID: {batch_ids[j]}")
        
        print(f"Processed audio features for {min(i+50, len(all_track_ids))} / {len(all_track_ids)} tracks.")
    
    print("Finished processing playlist.")
    return data

def main():
    playlist_urls = [
        'https://open.spotify.com/playlist/2YRe7HRKNRvXdJBp9nXFza',
        'https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M',  # Top Hits
        'https://open.spotify.com/playlist/1G8IpkZKobrIlXcVPoSIuf'   # 10k
    ]
    output_csv = 'playlist_data_HUGE.csv'
    song_buffer = [] 
    batch_write_size = 200
    total_tracks_processed = 0

    def dump_buffer(buffer):
        if len(buffer) == 0:
            return
        df_batch = pd.DataFrame(buffer)
        
        # calc sin_key
        if 'key' in df_batch.columns:
            df_batch['sin_key'] = np.sin(np.pi * df_batch['key'] / 11)
        else:
            df_batch['sin_key'] = np.nan

        if 'danceability' in df_batch.columns:
            audio_feature_columns = [col for col in df_batch.columns if col not in metadata_ft]
            columns_order = metadata_ft + audio_feature_columns
            df_batch = df_batch[columns_order]
        
        df_batch.to_csv(output_csv, mode='a', index=False, header=False)
        print(f"Wrote {len(df_batch)} tracks to {output_csv}.")

    if not os.path.isfile(output_csv):
        with open(output_csv, 'w', encoding='utf-8') as f:
            headers = ["Track Name",
                        "Artist",
                        "Album",
                        "Thumbnail URL",
                        "Track ID",
                        "id",
                        "uri",
                        "track_href",
                        "analysis_url",

                        "danceability",
                        "energy",
                        "key",
                        "loudness",
                        "mode",
                        "speechiness",
                        "acousticness",
                        "instrumentalness",
                        "liveness",
                        "valence",
                        "tempo",
                        "type",
                        "duration_ms",
                        "time_signature",
                        "sin_key"]
            headers.append('sin_key')
            f.write(','.join(headers) + '\n')

    for playlist_url in playlist_urls:
        print("Processing Spotify Playlist...")
        playlist_data = process_playlist(playlist_url)
        print(f"Retrieved {len(playlist_data)} tracks from the playlist.\n")

        for track_data in playlist_data:
            song_buffer.append(track_data)
            total_tracks_processed += 1
            
            # dump to CSV in batches
            if len(song_buffer) >= batch_write_size:
                dump_buffer(song_buffer)
                song_buffer = []
    dump_buffer(song_buffer) # cleans leftovers
    song_buffer = []

def verify_random_track(csv_file_path):
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print(f"CSV file not found at path: {csv_file_path}")
        return
    except pd.errors.EmptyDataError:
        print(f"CSV file at path {csv_file_path} is empty.")
        return
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    if 'Track ID' not in df.columns:
        print("The CSV file does not contain a 'Track ID' column.")
        return

    df = df.dropna(subset=['Track ID'])
    if df.empty:
        print("No valid tracks with 'Track ID' found in the dataset.")
        return

    random_track = df.sample(n=1).iloc[0]
    track_id = random_track['Track ID']
    track_name = random_track.get('Track Name', 'Unknown')
    artist_names = random_track.get('Artist', 'Unknown')
    print(f"\nSelected Track:\n- Name: {track_name}\n- Artist(s): {artist_names}\n- Track ID: {track_id}\n")

    try:
        fetched_features = sp.audio_features([track_id])[0]
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API error while fetching audio features: {e}")
        return
    except Exception as e:
        print(f"Unexpected error while fetching audio features: {e}")
        return

    if not fetched_features:
        print(f"No audio features found for Track ID: {track_id}")
        return

    spotify_audio_features_keys = [
        "danceability",
        "energy",
        "key",
        "loudness",
        "mode",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
        "type",
        "duration_ms",
        "time_signature"
    ]

    missing_features = [feature for feature in spotify_audio_features_keys if feature not in df.columns]
    if missing_features:
        print(f"The following audio feature columns are missing in the dataset: {missing_features}")
        return

    stored_features = random_track[spotify_audio_features_keys].to_dict()

    discrepancies = {}
    for feature in spotify_audio_features_keys:
        stored_value = stored_features.get(feature)
        fetched_value = fetched_features.get(feature)

        if pd.isna(stored_value) and fetched_value is None:
            continue  # Both are missing; consider as matching
        elif pd.isna(stored_value) or fetched_value is None:
            discrepancies[feature] = {'stored': stored_value, 'fetched': fetched_value}
            continue

        if isinstance(stored_value, float) and isinstance(fetched_value, float):
            if not np.isclose(stored_value, fetched_value, atol=1e-5):
                discrepancies[feature] = {'stored': stored_value, 'fetched': fetched_value}
        else:
            if stored_value != fetched_value:
                discrepancies[feature] = {'stored': stored_value, 'fetched': fetched_value}

    if not discrepancies:
        print("all audio features match.")
    else:
        print("!!! ERR: discrepancies found !!!")
        for feature, values in discrepancies.items():
            print(f" - {feature}: Stored = {values['stored']}, Fetched = {values['fetched']}")

    comparison_df = pd.DataFrame({
        'Feature': spotify_audio_features_keys,
        'Stored': [stored_features.get(f) for f in spotify_audio_features_keys],
        'Fetched': [fetched_features.get(f) for f in spotify_audio_features_keys],
        'Match': [
            np.isclose(stored_features.get(f, 0), fetched_features.get(f, 0), atol=1e-5) if isinstance(stored_features.get(f, 0), float) and isinstance(fetched_features.get(f, 0), float) else stored_features.get(f) == fetched_features.get(f)
            for f in spotify_audio_features_keys
        ]
    })

    print("\nDetailed Comparison:")
    print(comparison_df.to_string(index=False))

if __name__ == "__main__":
    main()
    verify_random_track('playlist_data_HUGE.csv')
