import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))


def spotify_search(artis=None, track=None, playlist=None, catagory=None):
    if artis and track:
        results = spotify.search(q='artist:' + artis + ' track:' + track, type='track', market='DE')
        items = results['tracks']['items']
        if len(items) > 0:
            track = items[0]
            print(track)
            return {"track": track['name'], "uri": track['uri']}

    elif artis:
        results = spotify.search(q='artist:' + artis, type='artist', market='DE')
        items = results['artists']['items']
        print(items)
        if len(items) > 0:
            artist = items[0]
            return {"artist": artist['name'], "uri": artist['uri']}

    elif track:
        results = spotify.search(q='track:' + track, type='track', market='DE')
        items = results['tracks']['items']
        if len(items) > 0:
            track = items[0]
            print(track)
            return {"track": track['name'], "uri": track["uri"]}


print(spotify_search(artis="Billy Talent", track="Red Flag"))
