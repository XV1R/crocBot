import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy import SpotifyClientCredentials
import os
from pybot import token


CLIENT_ID = token[1]
CLIENT_SECRET = token[2]
REDIRECT_URI= token[3]


# def playlists(spotify_user,user):
#    user = ctx.author
#     if len(args) < 1:
#         await ctx.send("Empty username; please enter a spotify username!")
#         return
#     print(args)
#     # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI))


#     auth_man = SpotifyClientCredentials(client_id=CLIENT_ID,client_secret=CLIENT_SECRET)
#     sp = spotipy.Spotify(auth_manager=auth_man)
#     spotify_user = str(args[0]).strip()

#     playlists = sp.user_playlists(spotify_user)

#     while playlists:
#         for i, playlist in enumerate(playlists['items']):
#             # print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
#             await ctx.send(f"{user} follows {playlist['name']}")
#         if playlists['next']:
#             playlists = sp.next(playlists)
#         else:
#             playlists = None

def playlists(spotify_user,user):
    auth_man = SpotifyClientCredentials(client_id=CLIENT_ID,client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_man)

    playlists = sp.user_playlists(spotify_user)

    return (playlists,sp)

def related(uri):
    auth_man = SpotifyClientCredentials(client_id=CLIENT_ID,client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_man)

    #artist = sp.artist(uri)
    return sp.artist_related_artists(uri)



