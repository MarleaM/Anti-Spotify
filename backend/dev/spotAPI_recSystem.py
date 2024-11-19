from dev.spotAPI_base import *

import numpy as np 
import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler


file_path = "./playlist_data.csv"
df = pd.read_csv(file_path, encoding='utf-8')

features = df.columns.tolist()

features_to_fit = [ft for ft in audio_headers if ft != "key"] + ["sin_key"]

# print("Missing Values Before Sanitization:")
# print(df.isnull().sum())
# print("\n")

initial_shape = df.shape
df_cleaned = df.dropna()
final_shape = df_cleaned.shape
rows_removed = initial_shape[0] - final_shape[0]
print(f"Removed {rows_removed} rows containing missing values.\n")

df = df_cleaned

def search_spotify_PD(song_name):
    search_results = sp.search(q=song_name, type='track', limit=1)
    if not search_results['tracks']['items']:
        print(f"No results found for '{song_name}'.")
        return pd.DataFrame()
    
    track = search_results['tracks']['items'][0]
    track_id = track['id']
    print("Selected Song:")
    print(f"Track Name: {track['name']}, Artist: {', '.join([artist['name'] for artist in track['artists']])}")
    
    audio_features = sp.audio_features([track_id])[0]
    if audio_features is None:
        print("No audio features found for the selected song.")
        return pd.DataFrame()
    
    song_out = pd.DataFrame([audio_features])
    song_out['Track Name'] = track['name']
    song_out['Artist'] = ', '.join([artist['name'] for artist in track['artists']])
    song_out['uri'] = track['uri']
    song_out['Thumbnail URL'] = track['album']['images'][0]['url']
    song_out['Preview URL'] = track.get('preview_url', None)
    song_out['Link URL'] = track['external_urls']['spotify']
    song_out['sin_key'] = np.sin(2 * np.pi * song_out['key'] / 11)
    return song_out

def process_recommendations(recs, scaler, original_song_features):
    if not recs:
        return pd.DataFrame()
    
    rec_df = pd.DataFrame({
        'Track Name': [track['name'] for track in recs],
        'Artist': [', '.join([artist['name'] for artist in track['artists']]) for track in recs],
        'URI': [track['uri'] for track in recs],
        'Thumbnail URL': [track['album']['images'][0]['url'] for track in recs],
        'Preview URL': [track.get('preview_url', None) for track in recs],
        'Link URL': [track['external_urls']['spotify'] for track in recs]
    })
    
    uris = rec_df['URI'].tolist()
    audio_features = []
    for i in range(0, len(uris), 50):
        batch = uris[i:i+50]
        features = sp.audio_features(batch)
        audio_features.extend(features)
    
    audio_features = [feat for feat in audio_features if feat is not None]
    
    if not audio_features:
        print("No audio features found for recommendations.")
        return pd.DataFrame()
    
    features_df = pd.DataFrame(audio_features)
    features_df['sin_key'] = np.sin(2 * np.pi * features_df['key'] / 11)
    features_df[features_to_fit] = features_df[features_to_fit].fillna(0)
    
    scaled_rec_features = scaler.transform(features_df[features_to_fit])
    similarities = cosine_similarity(original_song_features, scaled_rec_features).flatten()
    rec_df['similarity'] = similarities
    
    return rec_df

def fetch_recommendations(seed_uris, rec_type='similar', limit=100):
    if not seed_uris:
        print(f"No seed URIs provided for {rec_type} recommendations.")
        return []
    
    seed_uris = seed_uris[:5]
    
    try:
        recommendations = sp.recommendations(seed_tracks=seed_uris, limit=limit)
        return recommendations.get('tracks', [])
    except spotipy.SpotifyException as e:
        print(f"Spotify API error while fetching {rec_type} recommendations: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error while fetching {rec_type} recommendations: {e}")
        return []

def get_recs(song_name):
    """
    Fetches recommendations for a given song using Spotify API and cosine similarity.

    Parameters:
    - song_name (str): The name of the song to search for.

    Returns:
    - pd.DataFrame: DataFrame containing the original song followed by recommendations.
    """
    selected_song = search_spotify_PD(song_name)
    selected_song[features_to_fit] = selected_song[features_to_fit].fillna(0)
    df['sin_key'] = np.sin(2 * np.pi * df['key'] / 11)
    df['sin_key'] = df['sin_key'].replace({np.inf: np.nan, -np.inf: np.nan})
    df['sin_key'] = df['sin_key'].fillna(0)
    
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df[features_to_fit])
    selected_features_scaled = scaler.transform(selected_song[features_to_fit])
    df['cosine_similarity'] = cosine_similarity(selected_features_scaled, scaled_features).flatten()
    
    # find recs
    top_5_similar = df.sort_values(by='cosine_similarity', ascending=False).head(5)
    top_5_dissimilar = df.sort_values(by='cosine_similarity', ascending=True).head(5)
    
    # print("\nTop 5 Similar Songs:")
    # print(top_5_similar[['Track Name', 'Artist', 'cosine_similarity']])
    
    # print("\nTop 5 Dissimilar Songs:")
    # print(top_5_dissimilar[['Track Name', 'Artist', 'cosine_similarity']])
    
    similar_uris = top_5_similar['uri'].tolist()
    dissimilar_uris = top_5_dissimilar['uri'].tolist()
    
    similar_recommendations = fetch_recommendations(similar_uris, rec_type='similar', limit=100)
    dissimilar_recommendations = fetch_recommendations(dissimilar_uris, rec_type='dissimilar', limit=100)
    
    similar_rec_df = process_recommendations(similar_recommendations, scaler, selected_features_scaled)
    dissimilar_rec_df = process_recommendations(dissimilar_recommendations, scaler, selected_features_scaled)
    
    # top 4 from each, ensure uniqueness
    if not similar_rec_df.empty:
        top_similar_final = similar_rec_df.sort_values(by='similarity', ascending=False).drop_duplicates(subset=['URI']).head(4)
        print("\nTop 4 Similar Recommendations from Spotify API:")
        print(top_similar_final[['Track Name', 'Artist', 'similarity']])
    else:
        top_similar_final = pd.DataFrame()
        print("\nNo similar recommendations available.")
    
    if not dissimilar_rec_df.empty:
        top_dissimilar_final = dissimilar_rec_df.sort_values(by='similarity').drop_duplicates(subset=['URI']).head(4)
        print("\nTop 4 Dissimilar Recommendations from Spotify API:")
        print(top_dissimilar_final[['Track Name', 'Artist', 'similarity']])
    else:
        top_dissimilar_final = pd.DataFrame()
        print("\nNo dissimilar recommendations available.")
    
    orig_formatted = selected_song[['Track Name', 'Artist', 'uri', 'Thumbnail URL', 'Preview URL', 'Link URL']].copy()
    orig_formatted.rename(columns={'uri': 'URI'}, inplace=True)
    orig_formatted['similarity'] = 1.0  # Assign maximum similarity to the original song
    
    # Combine recommendations
    final = pd.concat([
        orig_formatted,
        top_dissimilar_final[['Track Name', 'Artist', 'URI', 'Thumbnail URL', 'Preview URL', 'Link URL', 'similarity']],
        top_similar_final[['Track Name', 'Artist', 'URI', 'Thumbnail URL', 'Preview URL', 'Link URL', 'similarity']],
    ], ignore_index=True)
    
    return final

# get_recs(song_name)
