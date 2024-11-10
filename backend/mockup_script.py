from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, origins='*')
#this is an example to see how a python script would send data to the frontend
#if you are trying to run this, make sure to use a virtual environment! :) 
#note: the following commands are for windows

#activate with this command: virtual_environment/Scripts/activate
#to run the script do: python mockup_script.py
#you can see the returned JSON on http://localhost:8080/api/users
@app.route("/api/users", methods = {'GET'})

def users():
    return jsonify(
        {
            "users": [
                'emily',
                'tony',
                'marlea',
                'lisa'
            ]
        }
    )

if __name__ == "__main__":
    app.run(debug=True, port=8080)