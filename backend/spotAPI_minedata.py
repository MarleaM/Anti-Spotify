from spotAPI_base import *
from spotAPI_minehelper import get_playlist_id

playlist_urls = [
    # 'https://open.spotify.com/playlist/2YRe7HRKNRvXdJBp9nXFza',
    'https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M',  # Top Hits
    # 'https://open.spotify.com/playlist/1G8IpkZKobrIlXcVPoSIuf'   # 10k
]
OUTPUT_CSV = 'playlist_data_HUGE.csv'

BATCH_WRITE_SIZE = 200


def mine_playlist(playlist_url, batch_size=50):
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
            artist_names = ', '.join([artist['name'] for artist in track['artists']][:3])
            album_name = track['album']['name']
            track_id = track['id']
            thumbnail_url = track['album']['images'][0]['url'] if track['album']['images'] else ""

            # Append track ID for fetching audio features
            if track_id:
                all_track_ids.append(track_id)
            
            # Prepare track data
            track_data = {
                'Track Name': track_name,
                'Artist': artist_names,
                'Album': album_name,
                'Thumbnail URL': thumbnail_url,
                'id': track_id
            }
            data.append(track_data)
        
        offset += batch_size
        print(f"Fetched {min(offset, total_tracks)} / {total_tracks} tracks.")
        
        if offset >= total_tracks:
            break  # All tracks fetched
    
    print("Fetching audio features...")
    
    # Fetch audio features in batches
    for i in range(0, len(all_track_ids), batch_size):
        batch_ids = all_track_ids[i:i+batch_size]
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
        
        print(f"Processed audio features for {min(i+batch_size, len(all_track_ids))} / {len(all_track_ids)} tracks.")
    
    print("Finished processing playlist.")
    return data

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

    if 'id' not in df.columns:
        print("The CSV file does not contain a 'id' column.")
        return

    df = df.dropna(subset=['id'])
    if df.empty:
        print("No valid tracks with 'id' found in the dataset.")
        return

    random_track = df.sample(n=1).iloc[0]
    track_id = random_track['id']
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

    missing_features = [feature for feature in audio_headers if feature not in df.columns]
    if missing_features:
        print(f"The following audio feature columns are missing in the dataset: {missing_features}")
        return

    stored_features = random_track[audio_headers].to_dict()

    discrepancies = {}
    for feature in audio_headers:
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
        'Feature': audio_headers,
        'Stored': [stored_features.get(f) for f in audio_headers],
        'Fetched': [fetched_features.get(f) for f in audio_headers],
        'Match': [
            np.isclose(stored_features.get(f, 0), fetched_features.get(f, 0), atol=1e-5) if isinstance(stored_features.get(f, 0), float) and isinstance(fetched_features.get(f, 0), float) else stored_features.get(f) == fetched_features.get(f)
            for f in audio_headers
        ]
    })

    print("\nDetailed Comparison:")
    print(comparison_df.to_string(index=False))

def dump_buffer(buffer):
    if len(buffer) == 0:
        return
    df_batch = pd.DataFrame(buffer)
    
    # calc sin_key
    if 'key' in df_batch.columns:
        df_batch['sin_key'] = np.sin(np.pi * df_batch['key'] / 11)
    else:
        df_batch['sin_key'] = np.nan

    df_batch = df_batch[csv_headers]
    df_batch.to_csv(OUTPUT_CSV, mode='a', index=False, header=False)
    print(f"Wrote {len(df_batch)} tracks to {OUTPUT_CSV}.")
    buffer.clear()

def main():
    song_buffer = [] 
    total_tracks_processed = 0

    if not os.path.isfile(OUTPUT_CSV):
        with open(OUTPUT_CSV, 'w', encoding='utf-8') as f:
            f.write(','.join(csv_headers) + '\n')

    for playlist_url in playlist_urls:
        print("Processing Spotify Playlist...")
        playlist_data = mine_playlist(playlist_url)
        print(f"Retrieved {len(playlist_data)} tracks from the playlist.\n")

        for track_data in playlist_data:
            song_buffer.append(track_data)
            total_tracks_processed += 1
            
            # dump to CSV in batches
            if len(song_buffer) >= BATCH_WRITE_SIZE:
                dump_buffer(song_buffer)
    dump_buffer(song_buffer) # cleans leftovers

    verify_random_track('playlist_data_HUGE.csv')

if __name__ == "__main__":
    main()
