# How the Backend Works

If you would like to contribute to backend components, this document might be of help to you! The files listed below are components that you will most likely have to interact with. We assme that the file path will be repo_name/backend/ etc.

The backend is built using Flask and interacts with the Spotify API and a static .csv with data on audio features fetched from the API to provide song recommendations to the frontend.

**General notes for contributors when working with the backend:**
- Rate limits: the Spotify API has a built-in rate limits on your interaction frequency - make sure to handle it gracefully  handled gracefully and reduce redundant API calls
- Error handling: when creating a new functionality, always include robust error handling to account for API failures, unexpected data formats
- The .csv dataset contains audio features fetched from the Spotify API. Unfortunately, audio features are no longer an API endpoint we can access, so expanding this dataset could be difficult

### minedata.py
This script mines multiple Spotify playlists and outputs the cleaned, processed track data to a .csv file.

### playlist_data_HUGE.csv
This .csv file is a pre-processed dataset containing track metadata and audio features for songs mined from Spotify playlists using the API. Our system currently only allows the users to search songs available in this dataset.

## dev/

### spotapi_base.py
This is the main script that defines the backend application. It initalizes the Flask app, defines API endpoints, and fetches recommendations using data from the .csv dataset. If you would like to add a new API endpoint (e.g., if you want to add a song's Album name), you should update this file accordingly. 

### spotapi_minehelper.py
This file provides helper functions to mine Spotify playlists from the API, such as fetching track metadata (e.g., playlist URL, track_IDs, etc.). 

- get_playlist_id(playlist_url): Extracts the playlist ID from a Spotify playlist URL
- fetch_tracks_batch(playlist_id, offset, limit): Fetches a batch of tracks from a Spotify playlist using pagination
- fetch_audio_features_batch(track_ids): Retrieves audio features for a list of Spotify track IDs
- mine_playlist(playlist_url, batch_size=50, max_workers=1): Mines a Spotify playlist by fetching tracks and their audio features concurrently using threading

### spotAPI_recSystem.py
This file is where the majority of our recommendation system is coded. It uses pre-processed playlist data from a static .csv file (playlist_data_HUGE.csv), runs a cosine similarity model of audio features and text-based metadata, and ouutputs song recommendations. 

- get_recs(song_name): Fetches recommendations for a given song based on audio feature similarities; eturns the original song, top 4 most similar songs, and top 4 most dissimilar songs
- get_suggestions_DF(query, top_n=5): Provides up to top_n song suggestions that match a search query based on TF-IDF text similarity of the track name and artist

To see outputs of the recommendation algorithm, run:  
```python
recommendations = get_recs("<song name>") # make sure to check that <song name> is in the .csv database
print(recommendations)
```

### ‎spotAPI_recSystem-DEPRECATED.py
Due to limited access to Spotify API's audio-features call (endpoint revoked since November 2024), this script is no longer in use. This is an archived version of our recommendation system, where we fetches data from Spotify API, analyze the fetched data (specifically the audio features of the user's searched song), and use cosine similarity on those data to output our song recommedantions. 
