from dev.spotAPI_base import *
import time
from tqdm import tqdm
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
import math

def get_playlist_id(playlist_url):
    if 'playlist/' in playlist_url:
        return playlist_url.split('playlist/')[1].split('?')[0]
    else:
        raise ValueError("Invalid Spotify playlist URL.")

def fetch_tracks_batch(playlist_id, offset, limit):
    """
    Fetches a batch of tracks from the Spotify playlist.

    Parameters:
    - playlist_id (str): Spotify playlist ID.
    - offset (int): The index of the first track to return.
    - limit (int): The number of tracks to return (max 50).

    Returns:
    - dict: The response from the Spotify API containing track data.
    """
    while True:
        try:
            response = sp.playlist_tracks(playlist_id, offset=offset, limit=limit)
            return response
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 429:
                retry_after = int(e.headers.get('Retry-After', 5))
                print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                time.sleep(retry_after)
            else:
                print(f"Spotify API error: {e}")
                return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

def fetch_audio_features_batch(track_ids):
    """
    Fetches audio features for a batch of track IDs.

    Parameters:
    - track_ids (list): List of Spotify track IDs.

    Returns:
    - list: List of audio feature dictionaries.
    """
    while True:
        try:
            audio_features = sp.audio_features(tracks=track_ids)
            return audio_features
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 429:
                retry_after = int(e.headers.get('Retry-After', 5))
                print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                time.sleep(retry_after)
            else:
                print(f"Spotify API error: {e}")
                return [None] * len(track_ids)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return [None] * len(track_ids)

def mine_playlist(playlist_url, batch_size=50, max_workers=1):
    """
    Processes the Spotify playlist concurrently and returns a list of track data.
    Handles large playlists by fetching tracks and audio features in parallel using multiple workers.

    Parameters:
    - playlist_url (str): The Spotify playlist URL.
    - batch_size (int): Number of tracks to fetch per request (max 100).
    - max_workers (int): Number of concurrent workers.

    Returns:
    - List[dict]: A list of dictionaries containing track data and audio features.
    """
    try:
        playlist_id = get_playlist_id(playlist_url)
    except ValueError as ve:
        print(ve)
        return []

    # First, fetch the initial batch to get total_tracks
    initial_response = fetch_tracks_batch(playlist_id, offset=0, limit=batch_size)
    if initial_response is None:
        return []

    total_tracks = initial_response.get('total', 0)
    if total_tracks == 0:
        print("Playlist is empty.")
        return []

    num_batches = math.ceil(total_tracks / batch_size)
    offsets = [i * batch_size for i in range(num_batches)]
    data = []
    all_track_ids = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        track_futures = {
            executor.submit(fetch_tracks_batch, playlist_id, offset, batch_size): offset
            for offset in offsets
        }

        with tqdm(total=num_batches, desc="Fetching tracks", unit="batch") as track_pbar:
            for future in as_completed(track_futures):
                response = future.result()
                if response is None:
                    track_pbar.update(1)
                    continue  # skip missing data

                tracks = response.get('items', [])
                for item in tracks:
                    track = item.get('track')

                    if track is None:
                        continue
                    album = track.get('album', {})
                    track_name = track.get('name', '')
                    artist_names = ', '.join([artist.get('name', '') for artist in track.get('artists', [])][:3])
                    album_name = album.get('name', '')
                    track_id = track.get('id')
                    thumbnail_url = album.get('images', [])[0]['url'] if album.get('images', []) else ""

                    if track_id:
                        all_track_ids.append(track_id)

                    track_data = {
                        'Track Name': track_name,
                        'Artist': artist_names,
                        'Album': album_name,
                        'Thumbnail URL': thumbnail_url,
                        'id': track_id
                    }
                    data.append(track_data)

                track_pbar.update(1)

    if not all_track_ids:
        print("No valid track IDs found.")
        return data

    valid_indices = set()
    audio_num_batches = math.ceil(len(all_track_ids) / batch_size)
    audio_offsets = [i * batch_size for i in range(audio_num_batches)]
    audio_batches = [all_track_ids[i:i + batch_size] for i in audio_offsets]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        audio_futures = {
            executor.submit(fetch_audio_features_batch, batch_ids): idx
            for idx, batch_ids in enumerate(audio_batches)
        }

        with tqdm(total=audio_num_batches, desc="Fetching features", unit="batch") as feature_pbar:
            for future in as_completed(audio_futures):
                batch_idx = audio_futures[future]
                audio_features = future.result()
                if audio_features is None:
                    audio_features = [None] * len(audio_batches[batch_idx])

                for j, features in enumerate(audio_features):
                    index = batch_idx * batch_size + j
                    if index >= len(data):
                        continue

                    if features:
                        for key, value in features.items():
                            data[index][key] = value
                        valid_indices.add(index)
                    # else:
                    #     print(f"\nNo audio features found for Track ID: {all_track_ids[index]}")

                feature_pbar.update(1)

    filtered_data = [data[i] for i in sorted(valid_indices)]

    return filtered_data