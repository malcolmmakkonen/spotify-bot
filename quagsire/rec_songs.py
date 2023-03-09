import spotipy
import json
import os
import bot
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

spotify_client_id='a35cd566798044a8989fb02e07a7e2b9'
spotify_secret='0e1097570fd54c298970ccb5bdc4103f'
SPOTIPY_REDIRECT_URI = 'http://localhost:8000/callback'
# spotify_redirect_uri='https://google.com'
scope = 'user-library-read user-top-read'
# scope="user-library-read,user-top-read,user-read-playback-state,user-modify-playback-state"

async def recommend_func(message):
    auth_manager = SpotifyOAuth(client_id=spotify_client_id,
                                client_secret=spotify_secret,
                                redirect_uri=SPOTIPY_REDIRECT_URI,
                                scope=scope)

    sp = spotipy.Spotify(auth_manager=auth_manager)

    # get the authorization URL
    auth_url = auth_manager.get_authorize_url()

    # send the auth URL to the user
    await message.channel.send(f"click the link to authorize your Spotify account: \n{auth_url}")

    # wait for the user to authorize the app
    response = await bot.wait_for('message', check=lambda m: m.author == message.author)

    auth_manager.get_access_token(response.content)

    # use the access token to make API calls
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # gets users top 5 tracks in 1 months
    results = sp.current_user_top_tracks(limit=5, offset=0, time_range='short_term')
    track_ids = [track['id'] for track in results['items']]
    names = [track['name'] for track in results['items']]
    artists = [', '.join([artist['name'] for artist in track['artists']]) for track in results['items']]

    # get 25 recommended tracks based on seed tracks
    rec_results = sp.recommendations(seed_tracks=track_ids, limit=25)

    bot_message = "quagsire recommends these songs :)\n"
    # all the songs recommended 
    for track in rec_results['tracks']:
        bot_message += f"{track['name']} - {', '.join([artist['name'] for artist in track['artists']])}\n"
    
    await message.channel.send(bot_message)






# DEBUGGING TOOLS

# to search for an artist and get id
# artist_name = 'The Weeknd'
# results = sp.search(q="artist:" + artist_name, type='artist')
# artist_id = results['artists']['items'][0]['id']
# print(json.dumps(results, sort_keys=False, indent=4))

# print('Artist:', artist_name)
# print('ID:', artist_id)

# print recommended tracks with name, artist, and URL
# for track in rec_tracks:
#     print(f"Name: {track['name']}")
#     print(f"Artist: {track['artists'][0]['name']}")
#     print(f"URL: {track['external_urls']['spotify']}\n")


# print(json.dumps(results, sort_keys=False, indent=4))

# for name,id,artist in zip(names,track_ids,artists):
#     print(f'{name} - {artist} song id: {id}')

# print("ids: \n")
# for id in track_ids:
#     print(id)

# OLD CODE FOR AUTHORIZATION
# auth_manager = SpotifyClientCredentials(client_id=spotify_client_id,
#                                             client_secret=spotify_secret,)


#     sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
#                                                 client_id=spotify_client_id,
#                                                 client_secret=spotify_secret,
#                                                 redirect_uri=SPOTIPY_REDIRECT_URI))