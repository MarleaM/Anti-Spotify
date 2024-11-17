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

def get_recs(song_name):
    df['sin_key'] = np.sin(2 * np.pi * df['key'] / 11)
    df['sin_key'] = df['sin_key'].replace({np.inf: np.nan, -np.inf: np.nan})
    df['sin_key'] = df['sin_key'].fillna(0)

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df[features_to_fit])
    
    # random song
    # selected_song = df.sample(n=1).reset_index(drop=True)
    selected_song = df[df['Track Name'].str.contains(song_name, case=False, na=False)]
    selected_index = selected_song.index[0]
    print("Selected Song:")
    print(selected_song[['Track Name', 'Artist']])
    
    # Compute cosine similarities
    selected_features_scaled = scaled_features[selected_index].reshape(1, -1)
    cosine_similarities = cosine_similarity(selected_features_scaled, scaled_features).flatten()
    df['cosine_similarity'] = cosine_similarities
    
    df_others = df.drop(selected_index)
    top_5_similar = df_others.sort_values(by='cosine_similarity', ascending=False).head(5)
    top_5_dissimilar = df_others.sort_values(by='cosine_similarity', ascending=True).head(5)
    
    print("\nTop 5 Similar Songs:")
    print(top_5_similar[['Track Name', 'Artist', 'cosine_similarity']])
    
    print("\nTop 5 Dissimilar Songs:")
    print(top_5_dissimilar[['Track Name', 'Artist', 'cosine_similarity']])
    
    similar_uris = top_5_similar['uri'].tolist()
    dissimilar_uris = top_5_dissimilar['uri'].tolist()
    
    # up to 5 seed tracks, genres, or artists combined
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
    
    similar_recommendations = fetch_recommendations(similar_uris, rec_type='similar', limit=100)
    dissimilar_recommendations = fetch_recommendations(dissimilar_uris, rec_type='dissimilar', limit=100)
    
    def process_recommendations(recs, scaler, original_song_features):
        if not recs:
            return pd.DataFrame()
        
        rec_df = pd.DataFrame({
            'Track Name': [track['name'] for track in recs],
            'Artist': [', '.join([artist['name'] for artist in track['artists']]) for track in recs],
            'URI': [track['uri'] for track in recs],
            'Thumbnail URL': [track['album']['images'][0]['url'] for track in recs],
            'Preview URL': [track.get('preview_url', None) for track in recs]
            
        })
        
        # Fetch audio features for recommendations
        uris = rec_df['URI'].tolist()
        audio_features = []
        for i in range(0, len(uris), 50):  # Spotify API allows up to 100 audio features per request
            batch = uris[i:i+50]
            features = sp.audio_features(batch)
            audio_features.extend(features)
        
        # Remove None entries
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
    
    final = pd.DataFrame()
    print()
    print("user input: ", song_name)

    similar_rec_df = process_recommendations(similar_recommendations, scaler, selected_features_scaled)
    dissimilar_rec_df = process_recommendations(dissimilar_recommendations, scaler, selected_features_scaled)
    
    if not similar_rec_df.empty:
        top_similar_final = similar_rec_df.sort_values(by='similarity', ascending=False).drop_duplicates(subset=['URI']).head(5)
        print("\nTop 5 Similar Recommendations from Spotify API:")
        print(top_similar_final[['Track Name', 'Artist', 'similarity']])
    else:
        top_similar_final = pd.DataFrame()
        print("\nNo similar recommendations available.")
    
    if not dissimilar_rec_df.empty:
        top_dissimilar_final = dissimilar_rec_df.sort_values(by='similarity').drop_duplicates(subset=['URI']).head(5)
        print("\nTop 5 Dissimilar Recommendations from Spotify API:")
        print(top_dissimilar_final[['Track Name', 'Artist', 'similarity']])
    else:
        top_dissimilar_final = pd.DataFrame()
        print("\nNo dissimilar recommendations available.")
    
    final = pd.concat([top_similar_final, top_dissimilar_final], ignore_index=True)
    return final

# get_recs(song_name)
