from flask import Flask, jsonify, request 
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
cors = CORS(app, origins='*')
#this is an example to see how a python script would send data to the frontend
#if you are trying to run this, make sure to use a virtual environment! :) 
#note: the following commands are for windows

#activate with this command: virtual_environment/Scripts/activate
#to run the script do: python mockup_script.py
#you can see the returned JSON on http://localhost:8080/api/users
@app.route("/api/users", methods = {'GET'})

def get_songs():
    song_name = request.args.get('song_name')

    return jsonify(
        {
            "songs": [
                {
                    "song_name": "Evil Lisa's Song",
                    "artist": "Lisa",
                    "album_cover": "url/to/album_cover1.jpg"
                },
                {
                    "song_name": "Evil Tony's Song",
                    "artist": "Tony",
                    "album_cover": "url/to/album_cover2.jpg"
                },
                {
                    "song_name": "Evil Emily's Song",
                    "artist": "Emily",
                    "album_cover": "url/to/album_cover3.jpg"
                },
                {
                    "song_name": "Evil Marlea's Song",
                    "artist": "Marlea",
                    "album_cover": "url/to/album_cover4.jpg"
                },
                                {
                    "song_name": "Lisa's Song",
                    "artist": "Lisa",
                    "album_cover": "url/to/album_cover1.jpg"
                },
                {
                    "song_name": "Tony's Song",
                    "artist": "Tony",
                    "album_cover": "url/to/album_cover2.jpg"
                },
                {
                    "song_name": "Emily's Song",
                    "artist": "Emily",
                    "album_cover": "url/to/album_cover3.jpg"
                },
                {
                "song_name": "Evil Marlea's Song",
                "artist": "Marlea",
                "album_cover": "/static/assets/sample_background.png"
                }

            ]
        }
    )

if __name__ == "__main__":
    app.run(debug=True, port=8080)