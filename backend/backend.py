from flask import Flask, jsonify, request 
from flask_cors import CORS
from flask_caching import Cache
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# import dev.spotAPI_base
# import dev.spotAPI_minehelper
# import dev.spotAPI_recSystem
from dev.spotAPI_recSystem import get_recs

app = Flask(__name__, static_folder='static')
cors = CORS(app, origins='*')
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Spotify API setup (assuming credentials are in environment variables)
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#this is an example to see how a python script would send data to the frontend
#if you are trying to run this, make sure to use a virtual environment! :) 
#note: the following commands are for windows
# python3 -m venv virtual_environment
#activate with this command: virtual_environment/Scripts/activate
#to run the script do: python mockup_script.py
#you can see the returned JSON on http://localhost:8080/api/users

@app.route("/api/users", methods = {'GET'})
def get_songs():
    song_name = request.args.get('song_name')

    if not song_name:
        return jsonify({"error": "Please provide a song name"}), 400

    result = get_recs(song_name)
    
    return jsonify(
        {
            "songs": [
                {
                    "song_name": row["Track Name"],
                    "artist": row["Artist"],
                    "album_cover": row["Thumbnail URL"],
                    "preview_url": row["Preview URL"],
                    "link_url": row["Link URL"]
                }
                for _, row in result.iterrows()
            ]
        }
    )

@app.route("/api/suggestions", methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def get_suggestions():
    """Endpoint to return search suggestions for a song"""
    query = request.args.get('query')

    if not query:
        return jsonify({"error": "Please provide a search query"}), 400

    try:
        results = sp.search(q=query, type='track', limit=10) 
        suggestions = [
            {
                "song_name": track["name"],
                "artist": ", ".join([artist["name"] for artist in track["artists"]]),
                "album_cover": track["album"]["images"][0]["url"] if track["album"]["images"] else None,
                "preview_url": track["preview_url"],
                "link_url": track["external_urls"]["spotify"]
            }
            for track in results["tracks"]["items"]
        ]

        return jsonify({"suggestions": suggestions})

    except Exception as e:
        print(f"Error fetching suggestions: {e}")
        return jsonify({"error": "Failed to fetch suggestions"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)

