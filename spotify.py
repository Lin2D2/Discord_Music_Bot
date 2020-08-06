import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')


class Spotify:
    def __init__(self):
        self.spotify = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        )

    def spotify_search(self, artis=None, track=None, album=None, playlist=None, catagory=None):
        if artis and track:
            results = self.spotify.search(q='artist:' + artis + ' track:' + track, type='track', market='DE')
            items = results['tracks']['items']
            if len(items) > 0:
                track = items[0]
                return {"track": track['name'], "uri": track['uri']}

        elif artis and album:
            results = self.spotify.search(q='artist:' + artis + ' album:' + album, type='album', market='DE')
            items = results['albums']['items']
            if len(items) > 0:
                album = items[0]
                return {"album": album['name'], "uri": album['uri']}

        elif artis:
            results = self.spotify.search(q='artist:' + artis, type='artist', market='DE')
            items = results['artists']['items']
            if len(items) > 0:
                artist = items[0]
                return {"artist": artist['name'], "uri": artist['uri']}

        elif track:
            results = self.spotify.search(q='track:' + track, type='track', market='DE')
            items = results['tracks']['items']
            if len(items) > 0:
                track = items[0]
                return {"track": track['name'], "uri": track["uri"], "image": track['album']["images"][0]["url"]}

        elif album:
            results = self.spotify.search(q='album:' + artis, type='album', market='DE')
            items = results['album']['items']
            if len(items) > 0:
                album = items[0]
                return {"album": album['name'], "uri": album['uri']}

        elif playlist:
            results = self.spotify.search(q='' + playlist, type='playlist')
            items = results['playlists']['items']
            if len(items) > 0:
                playlist = items[0]
                return {"playlist": playlist['name'], "uri": playlist['uri']}

    def get_playlist_content(self, playlist_id):
        results = self.spotify.playlist(playlist_id, fields="tracks,next")
        tracks = results['tracks']
        items = []

        def extract(source):
            for playlist_items in source["items"]:
                items.append({
                    "track": playlist_items['track']['name'],
                    "artists": [(lambda artis: artis["name"])(artis) for artis in playlist_items['track']['artists']],
                    "uri": playlist_items['track']["uri"],
                    "image": playlist_items['track']['album']["images"][0]["url"]
                }
                )

        extract(tracks)
        while tracks['next']:
            tracks = self.spotify.next(tracks)
            extract(tracks)
        return items


# spotify = Spotify()
# result = spotify.spotify_search(playlist="N7xtMix")
# playlist_i = result["uri"]
# print(spotify.get_playlist_content(playlist_i))
