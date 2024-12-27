# How to get OffBeets Working on your Local Environment

First, make sure you have forked and cloned the repo into your desired directory. Then, follow the setup steps in this order.

## Backend

### Spotify API Set-up

First, to run the backend script and make Web API calls, you need to have an access token from Spotify. 

#### 1) Set Up Your Account

First, create an account at the Spotify Developer Dashboard: https://developer.spotify.com/dashboard

#### 2) Create an App
Go on your Dashboard (https://developer.spotify.com/dashboard) and click on the "Create an app" button

#### 3) Request an Access Token
An access token is a string containing the credentials that allow you to make API calls to Spotify's database and retrieve song data (e.g artists, albums or tracks) or user's data (e.g your profile or your playlists).

- Go to the Dashboard
- Click on the name of the app you have just created (My App)
- Click on the Settings button
- The Client ID can be found here. The Client Secret can be found behind the View client secret link.

#### 4)  Link Your Access Token with OffBeets Backend
Now, replace <> with your device details and run the command below to set up a file in your folder:

```python
 cd /<your_folder_for_git_clones>/OffBeets/backend/
 touch .env
```
You should see an empty .env file being created in the "backend" folder

In the .env file, replace <> with your Spotify acess tocken details and paste in the following content:

```python
SPOTIFY_CLIENT_ID=<paste your client ID here>
SPOTIFY_CLIENT_SECRET=<paste your client secret here>
```

Now, your Spotify access tocken is set up!


### Virtual Environment

We recommend setting up a virtual environment for installing your python dependencies.
CD into backend. Your path should look like this:
```python
 ~/your_folder_for_git_clones/OffBeets/backend
```

Run this command to setup your virtual environment:
```bash
make install
```

Then, run the script:
```bash
make install
```
Wait for a few moments, and you should see a "Debugger PIN". That means your backend is up and ready! 

To clean the virtual environment and cache files: 
```bash
make clean
```

## Frontend
To set up your frontend, you will need to download node.js. It can be found here: https://nodejs.org/en

Now, cd into frontend. Your path should look like this:
```
 ~/your_folder_for_git_clones/OffBeets/frontend
```

Run this command to download the dependencies:
```
npm install
```

To activate, run the following command:
```
npm run dev
``` 

Now, you should be ready!

Ctrl + click on the link in your terminal, and you will be able to access the site.

