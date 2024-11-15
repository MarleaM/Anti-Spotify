# How to get Anti_Spotify Working on your Local Environment

blah blah blah git clone stuff

Make sure to do the setup steps in this order.

## Backend

### Virtual Envrionment

We recomend setting up a virtual environment for installing your python dependencies.
CD into backend, your path should look something like:
```python
 ~/your_folder_for_git_clones/OSS_Project/backend
```

Run this command to setup your virtual environment:
```python
python3 -m venv name_for_your_virtual_environment #for this example, we called it virtual_environment
```
When the environemt is done setting up, run this command to activate it:

windows: 
```python
virtual_environment/Scripts/activate
```

mac:

```python
source/virtual_environment/bin/activate
```

Now, you must install the packages:

```python
pip install Flask
pip install Flask_CORS
```
Then, run the script:
```python
python mockup_script.py
```

Now, your backend virtual environment is set up.

### Spotify API Set-up

To make Web API calls, you need to have an access Token from Spoftiy. 

#### 1) Set Up Your Account

First, create an account at the Spotify Developer Dashboard: https://developer.spotify.com/dashboard

#### 2) Create an App
Go on your Dashboard (https://developer.spotify.com/dashboard), click on "Create an app" button

#### 3) Request an Access Token
Access token is a string containing the credentials that allow you to make API calls to Spotify's database and retrieve song data (e.g artists, albums or tracks) or user's data (e.g your profile or your playlists).

- Go to the Dashboard
- Click on the name of the app you have just created (My App)
- Click on the Settings button
- The Client ID can be found here. The Client Secret can be found behind the View client secret link.

#### 4)  Link Your Access Token with Anti-Spotify Backend
Now, replace <> with your device details and run the command below to set up a file in your folder:
```
 cd /<your_folder_for_git_clones>/OSS_Project/backend/
 touch .env
```
You should see an empty .env file being created in the "backend" folder

In the .env file, replace <> with your Spotify acess tocken details and paste in the following content:
```
SPOTIFY_CLIENT_ID=<paste your client ID here>
SPOTIFY_CLIENT_SECRET=<paste your client secret here>
```

Now, your backend should be up and ready! 




## Frontend
To set up your frontend, you will need to download node.js. It can be found here: https://nodejs.org/en

Now, cd into frontend. Your path should look like this:
```
 ~/your_folder_for_git_clones/OSS_Project/frontend
```

run this command to download the dependencies:
```
npm install
```

now, to activate, do npm run dev:
```
npm run dev
``` 

Now, you should be ready!

ctrl + click on the link in your terminal, and you will be able to access the site.

