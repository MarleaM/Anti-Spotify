# How to get Anti_Spotify Working on your Local Environment

blah blah blah git clone stuff

### Backend

We recomend setting up a virtual environment for installing your python dependencies.
CD into backend, your path should look something like:
'''
 ~/your_folder_for_git_clones/OSS_Project/backend
'''

Run this command to setup your virtual environment:
'''
python3 -m venv name_for_your_virtual_environment #for this example, we called it virtual_environment
'''
When the environemt is done setting up, run this command to activate it:

windows: 
'''
virtual_environment/Scripts/activate
'''

mac:

'''
source/virtual_environment/bin/activate
'''

Now, you must install the packages:

'''
pip install Flask
pip install flask_cors
'''
Then, run the script:
'''
python mockup_script.py
'''

Now, your backend is set up and ready.


### Frontend
To set up your frontend, you will need to download node.js. It can be found here: https://nodejs.org/en

Now, cd into frontend. Your path should look like this:
'''
 ~/your_folder_for_git_clones/OSS_Project/frontend

'''

run this command to download the dependencies:
"""
npm install
"""

now, to activate, do npm run dev:
'''
npm run dev
''' 

Now, you should be ready!



