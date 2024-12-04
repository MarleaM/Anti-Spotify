from dev.spotAPI_base import *
from dev.spotAPI_minehelper import mine_playlist
import numpy as np 
import pandas as pd
import time

playlist_urls = [
    'https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M',     # Current 50 Top Hits
    'https://open.spotify.com/playlist/2YRe7HRKNRvXdJBp9nXFza',     # All time most played, 900
    'https://open.spotify.com/playlist/1G8IpkZKobrIlXcVPoSIuf'      # 10k
]
OUTPUT_CSV = 'playlist_data_REPAIR.csv'
BATCH_WRITE_SIZE = 200

# def verify_random_track(csv_file_path):
#     try:
#         df = pd.read_csv(csv_file_path)
#     except FileNotFoundError:
#         print(f"CSV file not found at path: {csv_file_path}")
#         return
#     except pd.errors.EmptyDataError:
#         print(f"CSV file at path {csv_file_path} is empty.")
#         return
#     except Exception as e:
#         print(f"Error reading CSV file: {e}")
#         return

#     if 'id' not in df.columns:
#         print("The CSV file does not contain a 'id' column.")
#         return

#     df = df.dropna(subset=['id'])
#     if df.empty:
#         print("No valid tracks with 'id' found in the dataset.")
#         return

#     random_track = df.sample(n=1).iloc[0]
#     track_id = random_track['id']
#     track_name = random_track.get('Track Name', 'Unknown')
#     artist_names = random_track.get('Artist', 'Unknown')
#     try:
#         fetched_features = sp.audio_features([track_id])[0]
#         if not fetched_features:
#             print(f"No audio features found for Track ID: {track_id}")
#             return
#     except spotipy.exceptions.SpotifyException as e:
#         print(f"Spotify API error while fetching audio features: {e}")
#         return
#     except Exception as e:
#         print(f"Unexpected error while fetching audio features: {e}")
#         return


#     missing_features = [feature for feature in audio_headers if feature not in df.columns]
#     if missing_features:
#         print(f"Missing feature columns in the dataset: {missing_features}")
#         return

#     stored_features = random_track[audio_headers].to_dict()

#     discrepancies = {}
#     for feature in audio_headers:
#         stored_value, fetched_value = stored_features.get(feature), fetched_features.get(feature)

#         if pd.isna(stored_value) and fetched_value is None:
#             continue  # Both are missing; consider as matching
#         elif pd.isna(stored_value) or fetched_value is None:
#             discrepancies[feature] = {'stored': stored_value, 'fetched': fetched_value}
#             continue

#         if isinstance(stored_value, float) and isinstance(fetched_value, float):
#             if not np.isclose(stored_value, fetched_value, atol=1e-5):
#                 discrepancies[feature] = {'stored': stored_value, 'fetched': fetched_value}
#         else:
#             if stored_value != fetched_value:
#                 discrepancies[feature] = {'stored': stored_value, 'fetched': fetched_value}

#     if discrepancies:
#         print("!!! ERR: discrepancies found !!!")
#         for feature, values in discrepancies.items():
#             print(f" - {feature}: Stored = {values['stored']}, Fetched = {values['fetched']}")

#     comparison_df = pd.DataFrame({
#         'Feature': audio_headers,
#         'In CSV': [stored_features.get(f) for f in audio_headers],
#         'Live API': [fetched_features.get(f) for f in audio_headers],
#         'Match': [
#             np.isclose(stored_features.get(f, 0), fetched_features.get(f, 0), atol=1e-5) if isinstance(stored_features.get(f, 0), float) and isinstance(fetched_features.get(f, 0), float) else stored_features.get(f) == fetched_features.get(f)
#             for f in audio_headers
#         ]
#     })

#     print(f"Sampled Track:\n- Name: {track_name}\n- Artist(s): {artist_names}\n- Track ID: {track_id}\n" +
#           "\nDetailed Comparison:\n" +
#           comparison_df.to_string(index=False),
#           flush=True)

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
    buffer.clear()

def main():
    start_time = time.time()
    total_tracks_processed = 0
    if not os.path.isfile(OUTPUT_CSV):
        with open(OUTPUT_CSV, 'w', encoding='utf-8') as f:
            f.write(','.join(csv_headers) + '\n')

    song_buffer = [] 
    for playlist_url in playlist_urls:
        playlist_data = mine_playlist(playlist_url)

        for track_data in playlist_data:
            if any(value is None or (isinstance(value, str) and not value.strip()) for value in track_data.values()):
                continue
            song_buffer.append(track_data)
            total_tracks_processed +=1
            # dump to CSV in batches
            if len(song_buffer) >= BATCH_WRITE_SIZE:
                dump_buffer(song_buffer)

    end_time = time.time()  # End timing
    elapsed_time = end_time - start_time
    dump_buffer(song_buffer) # cleans leftovers
    # verify_random_track(OUTPUT_CSV)
    print(f"\nMined {total_tracks_processed} tracks in {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    main()
