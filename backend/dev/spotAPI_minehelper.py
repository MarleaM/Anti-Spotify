from spotAPI_base import sp

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
            if len(track['artists']) >=3:
                artist_names = ', '.join([artist['name'] for artist in track['artists']][:3])
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