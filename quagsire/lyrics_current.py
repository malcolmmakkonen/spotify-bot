import spotipy
import lyricsgenius as lg
import time
import json
from lyricsgenius import Genius

spotify_client_id='a35cd566798044a8989fb02e07a7e2b9'
spotify_secret='0e1097570fd54c298970ccb5bdc4103f'
spotify_redirect_uri='https://google.com'
genius_access_token='CLkXAcvasmhwTphGOlTnFZ-01EYprzHCaoR8o3K-TvH-TgJCkU_NqJgcRvlqiNpz'

async def lyrics_current_func(message):
    scope = 'user-read-currently-playing'

    # spotifyOauth is a class
    oauth_object = spotipy.SpotifyOAuth(client_id=spotify_client_id, 
                                        client_secret=spotify_secret,
                                        redirect_uri=spotify_redirect_uri, 
                                        scope=scope)

    token_dict = oauth_object.get_access_token()
    token = token_dict['access_token']

    await message.channel.send("debug")
    # spotify object
    spotify_object=spotipy.Spotify(auth=token)

    # genius object
    genius_object=lg.Genius(genius_access_token)

    current = spotify_object.currently_playing()
    status = current['currently_playing_type']

    # to see json
    print(json.dumps(current, sort_keys=False, indent=4))

    if status == 'track':
        artist_name=current['item']['album']['artists'][0]['name']
        song_title = current['item']['name'] 

        length = current['item']['duration_ms']
        progress = current['progress_ms']
        time_left = int(((length-progress)/1000))

        # finds song
        song = genius_object.search_song(title=song_title, artist=artist_name)
        lyrics = song.lyrics

        print(lyrics)
        await message.channel.send(lyrics)

        time.sleep(time_left)

    elif status == 'ad': 
        time.sleep(30)