# cd /local/;
# mkdir data-oss;
# curl -L -O https://www.kaggle.com/api/v1/datasets/download/yamaerenay/spotify-dataset-19212020-600k-tracks;
# unzip spotify-dataset-19212020-600k-tracks;


# cleaned_file_path = "/local/data-oss/tracks_cleaned.csv"
# df.to_csv(cleaned_file_path, index=False)
# print(f"Cleaned data saved to {cleaned_file_path}")

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

file_path = "./spotify-2023.csv"
df = pd.read_csv(file_path, encoding='iso-8859-2')

features = df.columns.tolist()
print(features)
cols_to_convert = ['streams', 'in_deezer_playlists' , 'in_spotify_playlists', 'in_shazam_charts', 'key', 'mode']

for col in cols_to_convert:
    df[col] = pd.to_numeric(df[col], errors='coerce')

features_excluded = [
    'id',
    'name',
    'popularity',
    'duration_ms',
    'explicit',
    'artists',
    'id_artists',
    'release_date',
    ]

# features_to_fit = [
#     'danceability',
#     'energy',
#     'key',
#     'loudness',
#     'mode',
#     'speechiness',
#     'acousticness',
#     'instrumentalness',
#     'liveness',
#     'valence',
#     'tempo',
#     'time_signature',
#     ]
features_to_fit= [
    'danceability_%',
    'valence_%',
    'energy_%',
    'acousticness_%',
    'instrumentalness_%',
    'liveness_%',
    'speechiness_%'
]

# print("DataFrame Information:")
# print(df.info())
# print("\n")

# print("First 5 Rows:")
# print(df.head())
# print("\n")

# print("Summary Statistics:")
# print(df.describe(include='all'))
# print("\n")

# print("Missing Values Before Sanitization:")
# print(df.isnull().sum())
# print("\n")

# Data Sanitization
# initial_shape = df.shape
# df_cleaned = df.dropna()
# final_shape = df_cleaned.shape
# rows_removed = initial_shape[0] - final_shape[0]
# print(f"Removed {rows_removed} rows containing missing values.\n")

# df = df_cleaned

# numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
# for col in numerical_cols:
#     plt.figure(figsize=(8, 4))
#     sns.histplot(df[col], kde=True)
#     plt.title(f'Distribution of {col}')
#     plt.xlabel(col)
#     plt.ylabel('Frequency')
#     plt.tight_layout()
#     plt.show()

# b. Correlation Heatmap
# if len(numerical_cols) > 1:  # Ensure there are at least two numerical columns
#     plt.figure(figsize=(12, 10))
#     corr_matrix = df[numerical_cols].corr()
#     sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True)
#     plt.title('Correlation Heatmap')
#     plt.tight_layout()
#     plt.show()
# else:
#     print("Not enough numerical columns to display a correlation heatmap.\n")


# Step 1: Normalize the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df[features_to_fit])

# Step 2: Select a song weighted by popularity
selected_song = df.sample(n=1, weights='streams')
selected_index = selected_song.index[0]

print("Selected Song:")
print(selected_song[['track_name', 'artist(s)_name', 'streams']])

# Step 3: Compute cosine similarity between the selected song and all others
selected_features_scaled = scaled_features[selected_index].reshape(1, -1)
cosine_similarities = cosine_similarity(selected_features_scaled, scaled_features).flatten()

# Step 4: Add cosine similarities to the dataframe
df['cosine_similarity'] = cosine_similarities

# Step 5: Exclude the selected song from the dataframe
df_others = df.drop(selected_index)

# # Step 6: Find top 5 songs with best cosine similarity
top_5_similar = df_others.sort_values(by='cosine_similarity', ascending=False).head(5)

# # Step 7: Find top 5 songs with worst cosine similarity
top_5_dissimilar = df_others.sort_values(by='cosine_similarity', ascending=True).head(5)

# # Step 8: Display the results
print("\nTop 5 Similar Songs:")
print(top_5_similar[['track_name', 'artist(s)_name', 'cosine_similarity']])

print("\nTop 5 Dissimilar Songs:")
print(top_5_dissimilar[['track_name', 'artist(s)_name', 'cosine_similarity']])