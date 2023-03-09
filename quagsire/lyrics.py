import lyricsgenius as lg
import json
import re
import Levenshtein
from lyricsgenius import Genius

def check_similarity(name_lower, str_cmpr, similarity_threshold=0.8):
    distance = Levenshtein.distance(name_lower, str_cmpr)
    similarity = 1 - (distance / max(len(name_lower), len(str_cmpr)))
    return similarity >= similarity_threshold

async def lyrics_func(message, client, access_token):
    genius_access_token=access_token

    await message.channel.send("what song?")
    user_response = await client.wait_for('message', timeout=20)
    song_str = str(user_response.content)

    await message.channel.send("who's the artist?")
    user_response = await client.wait_for('message', timeout=20)
    artist_str = str(user_response.content)
    
    # genius object
    genius_object=lg.Genius(genius_access_token)
    
    # finds song(s)
    # song = genius_object.search_song(title=song_str, artist=artist_str)
    song = genius_object.search_songs(song_str)
    

    song_infos = []
    key_update = 0
    for i in range(5):
        song_title = song['hits'][i]['result']['title']
        song_id = song['hits'][i]['result']['id']
        artist_name = song['hits'][i]['result']['artist_names']
        full_title = song['hits'][i]['result']['full_title']
        full_title = full_title.lower()

        artist_name_lower = artist_name.lower()
        song_name_lower = song_title.lower()

        # in case user spells name wrong
        if check_similarity(artist_name_lower, artist_str) or re.search(artist_str, full_title) or (check_similarity(song_name_lower, song_str) and check_similarity(artist_name_lower, artist_str)):
            song_info = str(song_title + " - " + artist_name)
            song_infos.append(song_info)
            key_update = i 
            break


    # for single choice prompting
    await message.channel.send("is this the song? ")
    await message.channel.send("".join(song_infos))

    user_response = await client.wait_for('message', timeout=20)
    
    # for single choice prompting
    choice = str(user_response.content)
    chars = set('yes')
    if any((c in chars) for c in choice):
        song_title = song['hits'][key_update]['result']['title']
        artist_name = song['hits'][key_update]['result']['artist_names']
    
    else:
        print("Not found.")
        # key_update = 0
        # for i in range(20):
        #     song_title = song['hits'][i]['result']['title']
        #     song_id = song['hits'][i]['result']['id']
        #     artist_name = song['hits'][i]['result']['artist_names']
        #     full_title = song['hits'][i]['result']['full_title']
        #     full_title = full_title.lower()

        #     artist_name_lower = artist_name.lower()
        #     if artist_name_lower == artist_str or re.search(artist_str, full_title):
            
        #         song_info = str(i + " )   " + song_title + " - " + artist_name)
        #         song_infos.append(song_info)
        #         key_update = i 
                
        # await message.channel.send("Which song did you want ?\n".join(song_infos))

    genius = Genius(genius_access_token)
    song = genius.search_song(title=song_title, artist=artist_name) # need title and artist

    if song is not None:
        song_info = f"{song_title} - {artist_name} ({song.url})"
        await message.channel.send(song_info)
    else:
        await message.channel.send(f"sorry i could not find lyrics for {song_title} by {artist_name}")



# DEBUGGING TOOLS
# print(f'{username} wants the lyrics for {song_str} by {artist_str}')
# print(f'{i+1} ) {song_title} - {artist_name} id: {song_id}')
# print('\nInformation: ')
# print(song['hits'][choice]['result']['id'])
# print(song['hits'][choice]['result']['artist_names'])

# JSON LOG
# print(json.dumps(song, sort_keys=False, indent=4))