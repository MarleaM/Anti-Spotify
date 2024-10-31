'''
this file is imported from em's ML project (Fall 2023)
'''

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

import csv 
import math
import random

"""
gets data from saved data.csv file containing only Spotify's playlist data
@params: none
@returns: array of labels, track identifications, and track data
  arr[0] = dictionary storing playlist name keyed on playlist ID
  arr[1] = dictionary storing song title and its artist(s) keyed on track ID 
  arr[2] = pandas dataframe storing audio features data
"""
def getSpotifyData():

    sp = accessSpotify()

    # convert spotify data csv to pandas dataframe
    import pandas as pd
    df = pd.read_csv('data.csv')
    
    # initialize dictionaries 
    dictPlaylists = {}
    dictTracks = {}

    # populates playlist dictionary 
    playlistIDs = df.pid.unique()
    for pid in playlistIDs:
        pName = sp.user_playlist(user='spotify', playlist_id=pid, fields='name')
        dictPlaylists[pid] = pName['name']
        print(pid, dictPlaylists[pid])

    # populates tracks dictioonary
    trackIDs = df.tid.unique()
    for tid in trackIDs:
         track = sp.track(tid)
         dictTracks[tid] = track['name']
         print(tid, dictTracks[tid])

    print(df)

    """

    # populates tracks dictionary
    with open('data/tid.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        # authorize access to Spotify API
        sp = accessSpotify()

        # writes column labels
        head = ['tid', 'name', 'artist']
        writer.writerow(head)

        # saves and writes data for each track in playlist in CSV
        trackIDs = df.tid.unique()
        for tid in trackIDs:
            field = {}
            field['id'] = tid
            track = sp.track(tid)
            tName = track['name']
            
            artistArr = track['artists']   # get track artist(s)
            tArtists = []
            for a in artistArr:
                tArtists.append(a['name'])
            strArtists = ', '.join(map(str, tArtists))

            field['name'] = tName
            field['artist'] = strArtists
            writer.writerow(field)
            print(field)
"""
    return df


"""
writes CSV file by querying Spotify API
@params: none
@returns: none
"""
def makeCSV():
    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        # authorize access to Spotify API
        sp = accessSpotify()

        # get all of spotify's playlists
        playlists = ['37i9dQZF1DXcF6B6QPhFDv', '37i9dQZF1DWU2LcZVHsTdv', '37i9dQZF1DWV0gynK7G6pD', 
                     '37i9dQZF1DX2oc5aN4UDfD', '37i9dQZF1DXd9rSDyQguIk', '37i9dQZF1DX2GKumqRIZ7g', 
                     '37i9dQZF1DWWOaP4H0w5b0', '3xATMCiEtBqwncDGfBCIu5', '37i9dQZF1DX5dpn9ROb26T']

        # finds smallest playlist size
        n = 19

        # writes column labels
        field = ['tid', 'loudness', 'tempo', 'time_siganture', 'key', 'major/minor', 
                 'duration', 'instrumentalness', 'speechiness', 'acousticness', 'danceability', 
                 'liveness', 'energy', 'valence', 'pid']
        writer.writerow(field)

        # playlists already loaded in data file
        # processed = ['37i9dQZF1DXcBWIGoYBM5M', '37i9dQZF1DX0XUsuxWHRQd', '37i9dQZF1DX1lVhptIYRda', 
        #              '37i9dQZF1DX10zKzsJ2jva', '37i9dQZF1DX4JAvHpjipBk', '37i9dQZF1DX4sWSpwq3LiO', 
        #              '37i9dQZF1DX4SBhb3fqCJd', '37i9dQZF1DWXRqgorJj26U', '37i9dQZF1DX4dyzvuaRJ0n', 
        #              '37i9dQZF1DXcF6B6QPhFDv', '37i9dQZF1DXcRXFNfZr7Tp', '37i9dQZF1DX4o1oenSJRJd',
        #              '37i9dQZF1DXbTxeAdrVG2l', '37i9dQZF1DWTJ7xPn4vNaz', '37i9dQZF1DXaKIA8E7WcJj',
        #              '37i9dQZF1DWSV3Tk4GO2fq', '37i9dQZF1DWTwnEm1IYyoj', '37i9dQZF1DX2A29LI7xHn1',
        #              '37i9dQZF1DX2RxBh64BHjQ', '37i9dQZF1DWT6SJaitNDax', '37i9dQZF1DX0HRj9P7NxeE',
        #              '37i9dQZF1DWTggY0yqBxES', '37i9dQZF1DX0Tkc6ltcBfU', '37i9dQZF1DWUVpAXiEPK8P', 
        #              '37i9dQZF1DWSvKsRPPnv5o', '37i9dQZF1DXan38dNVDdl4', '37i9dQZF1DWYkaDif7Ztbp',
        #              '37i9dQZF1DWY4xHQp97fN6', '37i9dQZF1DWVA1Gq4XHa6U', '37i9dQZF1DX4UtSsGT1Sbe']


        # saves and writes data for each track in playlist in CSV
        for pid in playlists:
            try:
                dictTracks = {}

                tracks = sp.user_playlist_tracks('spotify', playlist_id=pid)
                allTracks = getAllTracks(sp, pid, tracks, dictTracks)
                tData = extractRandom(allTracks, n)

                for t in tData:
                    writer.writerow(t)
            except:
                continue



"""
grants access to Spotify API
@params: none
@returns: spotify access token as spotipy object
"""
def accessSpotify():
    # access token from API
    cid = 'f826b0b85a004f62a3172ba1f1ee5376'
    secret = 'a9363022c66f4ffd8d3e0151216bba23'

    # get access token
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

"""
grabs all user playlists
@params: sp - spotipy object
        usrname - given spotify username
@returns: dictionary object with all of user's playlist info
"""
def getUserPlaylists(sp, name):
    try:
        sp.user(name)
    except:
        print("[Error] invalid username")

    return sp.user_playlists(name)

"""
determines number of tracks to pull from each playlist
@params: playlists - dictionary object containing information on user's public playlists
@returns: integer value representing number of datapoints in any one class
"""
def getMinSize(playlists):
    minPlaylistSize = 20000

    # finds size of smallest playlist
    for p in playlists['items']:
        num = p['tracks']['total']
        if num < minPlaylistSize:
            minPlaylistSize = num
    
    # return number of songs we will load from each playlist
    return math.floor(minPlaylistSize*0.75)    

"""
gets all track data from any given playlist
@params: sp - spotipy object with spotify access token
         pid - unique playlist ID
         tracks - dictionary containing information from all tracks in playlist
         dictTracks - dictionary with already loaded tracks to update with this 
                      playlist's tracks
@returns: dictionary of dictionaries containing all track data from given playlist
"""
def getAllTracks(sp, pid, tracks, dictTracks):

    allTracks = {}
    print("getting all track data...")

    for t in tracks['items']:
        tid = t['track']['id']          # get track id and name
        tName = t['track']['name']

        print(tid, tName)
        
        artistArr = t['track']['artists']   # get track artist(s)
        tArtists = []
        for a in artistArr:
            tArtists.append(a['name'])
        strArtists = ', '.join(map(str, tArtists))
        
        dictTracks[tid] = (tName, strArtists)  # save to dictionary

    return sp.user_playlists(name)

"""
determines number of tracks to pull from each playlist
@params: playlists - dictionary object containing information on user's public playlists
@returns: integer value representing number of datapoints in any one class
"""
def getMinSize(playlists):
    minPlaylistSize = 20000

    # finds size of smallest playlist
    for p in playlists['items']:
        num = p['tracks']['total']
        if num < minPlaylistSize:
            minPlaylistSize = num
    
    # return number of songs we will load from each playlist
    return math.floor(minPlaylistSize*0.75)    

"""
gets all track data from any given playlist
@params: sp - spotipy object with spotify access token
         pid - unique playlist ID
         tracks - dictionary containing information from all tracks in playlist
         dictTracks - dictionary with already loaded tracks to update with this 
                      playlist's tracks
@returns: dictionary of dictionaries containing all track data from given playlist
"""
def getAllTracks(sp, pid, tracks, dictTracks):

    allTracks = {}
    print("getting all track data...")

    for t in tracks['items']:

        tid = t['track']['id']          # get track id and name
        tName = t['track']['name']

        print(tid, tName)
        
        artistArr = t['track']['artists']   # get track artist(s)
        tArtists = []
        for a in artistArr:
            tArtists.append(a['name'])
        strArtists = ', '.join(map(str, tArtists))
        
        dictTracks[tid] = (tName, strArtists)  # save to dictionary

        print("getting row data...")

        # build row data
        analysis = sp.audio_analysis(tid)
        features = sp.audio_features(tid)
        
        tr = {
            # song info
            'tid': tid,
            
            # objective (?) data
            "loudness": analysis['track']['loudness'],
            "tempo": analysis['track']['tempo'],
            "time_signature": analysis['track']['time_signature'],
            "key": analysis['track']['key'],    
            "major/minor": analysis['track']['mode'],  # major = 1, minor = 0
            "duration": features[0]['duration_ms'],
            "instrumentalness": features[0]['instrumentalness'],
            "speechiness": features[0]['speechiness'],

            # subjective (?) data
            "acousticness": features[0]['acousticness'],
            "danceability": features[0]['danceability'],
            "liveness": features[0]['liveness'],
            "energy": features[0]['energy'],
            "valence": features[0]['valence'],

            # label
            "pid": pid
        }
    
        allTracks[tr['tid']] = tr
    
    print(allTracks)

    return allTracks

"""
ensures classes are evenly distributed
@params: tracks - dictionary containing data for each track in playlist
         n - number of tracks included in pandas dataframe from each playlist
@returns: dictionary contianing track data for n random songs
"""
def extractRandom(tracks, n):

    ret = []

    # shuffle dictionary data in tracks
    keys = list(tracks.keys())
    random.shuffle(keys)

    print("\nshuffled keys: ", keys)
    
    # build new dictionary from first n keys
    print("\nNEW DICTIONARY")
    print("--------------------")
    for i in range(n):
        tData = []

        tid = keys[i]  
        tData.append(tid)

        d = tracks[tid]     # gets dictionary keyed on track id

        tData.append(d['loudness'])
        tData.append(d['tempo'])
        tData.append(d['time_signature'])
        tData.append(d['key'])
        tData.append(d['major/minor'])
        tData.append(d['duration'])
        tData.append(d['instrumentalness'])
        tData.append(d['speechiness'])
        tData.append(d['acousticness'])
        tData.append(d['danceability'])
        tData.append(d['liveness'])
        tData.append(d['energy'])
        tData.append(d['valence'])
        tData.append(d['pid'])

        ret.append(tData)
    
    print("ALL RET")
    print("--------")
    for r in ret:
        print(r)
    
    return ret

"""
@params: data - dictionary containing track info
"""
def findDuplicates(tData, pdData, playlists, tracks):

    # iterate over tData to check if each tid is already in pdData
    for t in tData:
        tid = t.get(t['tid'])

        try:
            pdData.get(tid) # check if tid already in pandas dataframe

            tName = tracks.get(tid[0])
            pName = playlists.get(t['pid'])

            print("%s already in playlist %s" % (tName, pName))
        except:
            continue

def moreTrackData():

    # convert spotify data csv to pandas dataframe
    import pandas as pd
    df = pd.read_csv("data/data.csv")

    # access spotify
    sp = accessSpotify()

    # new data to add to pandas
    pop = []
    yr = []

    # query tracks, add data
    tids = df["tid"]
    tids = tids[:5]
    
    tracks = sp.tracks(tids)
    print(tracks)

    for t in tracks:
        p = t['popularity']
        print(p)

        r = t['album']['release_date']
        print(r)

        # populate lists
        pop.append(p)
        yr.append(r)

        break

makeCSV()
