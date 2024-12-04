from dev.spotAPI_base import *

import numpy as np 
import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer

file_path = "./playlist_data_HUGE.csv"
df = pd.read_csv(file_path, encoding='utf-8')

features = df.columns.tolist()

features_to_fit = [ft for ft in audio_headers if ft != "key"] + ["sin_key"]

# print("Missing Values Before Sanitization:")
# print(df.isnull().sum())
# print("\n")
df['Link URL'] = 'https://open.spotify.com/track/' + df['id']

initial_shape = df.shape
df_cleaned = df.dropna()
final_shape = df_cleaned.shape
rows_removed = initial_shape[0] - final_shape[0]
print(f"Removed {rows_removed} rows containing missing values.\n")

df = df_cleaned
df['sin_key'] = np.sin(2 * np.pi * df['key'] / 11)
df['sin_key'] = df['sin_key'].replace({np.inf: np.nan, -np.inf: np.nan})
df['sin_key'] = df['sin_key'].fillna(0)

df['combined_text'] = df['Track Name'].str.lower() + " " + df['Artist'].str.lower()
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_text'])
def get_recs(song_name):
    """
    Fetches recommendations for a given song using Spotify API and cosine similarity.

    Parameters:
    - song_name (str): The name of the song to search for.

    Returns:
    - pd.DataFrame: DataFrame containing the original song followed by recommendations.
    """
    selected_song = df[df["Track Name"].str.lower() == song_name.lower()]
    if selected_song.empty:
        return pd.DataFrame(columns=['Track Name', 'Artist', 'Thumbnail URL', 'Link URL', 'similarity'])
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df[features_to_fit])
    selected_features_scaled = scaler.transform(selected_song[features_to_fit])
    df['cosine_similarity'] = cosine_similarity(selected_features_scaled, scaled_features).flatten()
    
    # find recs
    top_similar = df.sort_values(by='cosine_similarity', ascending=False).head(5)
    top_similar = top_similar.iloc[1:5]
    top_dissimilar = df.sort_values(by='cosine_similarity', ascending=True).head(4)
    
    orig_formatted = selected_song[['Track Name', 'Artist', 'Thumbnail URL', 'Link URL']].copy()
    orig_formatted['cosine_similarity'] = 1.0  # Assign maximum similarity to the original song
    
    # Combine recommendations
    final = pd.concat([
        orig_formatted[['Track Name', 'Artist', 'Thumbnail URL', 'Link URL', 'cosine_similarity']],
        top_dissimilar[['Track Name', 'Artist', 'Thumbnail URL', 'Link URL', 'cosine_similarity']],
        top_similar[['Track Name', 'Artist', 'Thumbnail URL', 'Link URL', 'cosine_similarity']],
    ], ignore_index=True)
    print(final)
    return final


def get_suggestions_DF(query, top_n=5):
    """
    Fetches up to `top_n` song suggestions that match the query based on Track Name and Artist.
    
    Parameters:
    - query (str): The search term for the song and/or artist.
    - top_n (int): The maximum number of suggestions to return.
    
    Returns:
    - pd.DataFrame: DataFrame containing up to `top_n` matching songs.
    """
    if not isinstance(query, str) or not query.strip():
        return pd.DataFrame(columns=['Track Name', 'Artist', 'Thumbnail URL', 'Link URL'])
    query_processed = query.lower()
    query_vector = tfidf.transform([query_processed])
    # NOTE THAT THIS SIM IS QUERY SIM, NOT FEATURE SIM
    cosine_sim = cosine_similarity(query_vector, tfidf_matrix).flatten()
    df['similarity'] = cosine_sim
    sorted_df = df.sort_values(by='similarity', ascending=False)
    sorted_df = sorted_df[sorted_df['similarity'] < 1.0]
    
    suggestions = sorted_df[['Track Name', 'Artist', 'Thumbnail URL', 'Link URL', 'similarity']].head(top_n).copy()
    suggestions = suggestions[suggestions['similarity'] >= 0.1]
    return suggestions