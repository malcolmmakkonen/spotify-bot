import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
import asyncio
from lyrics import lyrics_func
from lyrics_current import lyrics_current_func
from rec_songs import recommend_func

intents = discord.Intents.all()
intents.members = True
intents.typing = True
intents.reactions = True

TOKEN = os.getenv('TOKEN')
spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
spotify_secret = os.getenv('SPOTIFY_SECRET')
spotify_redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
genius_access_token=os.getenv('GENIUS_ACCESS_TOKEN')

client = commands.Bot(command_prefix='!', intents=intents)

def run_discord_bot():
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    BOT_MENTION = "<@1082859197420552212>"

    @client.event
    async def on_guild_join(guild):
        # Find the first text channel with the name "general"
        channel = discord.utils.get(guild.text_channels, name='general')

        # Send a message to the channel
        if channel is not None:
            await channel.send('sup nerds')

    @client.event
    async def on_message(message):

        if message.author.bot: 
            return 

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        if message.content.startswith('!hello'):
            await message.channel.send("Hello!")

        if message.content.startswith('!lyricscurrent'):
            await lyrics_current_func(message)

        if message.content.startswith('!lyrics'):
            await lyrics_func(message, client, genius_access_token)
            
        if message.content.startswith('!recommend'):
            await recommend_func(message)

    async def main():
        await client.start(TOKEN)

    asyncio.run(main())


# FOR SPOTIFY
# spotifyOauth is a class
# oauth_object = spotipy.SpotifyOAuth(client_id=spotify_client_id, 
#                                     client_secret=spotify_secret,
#                                     redirect_uri=spotify_redirect_uri, 
#                                     scope=scope)

# token_dict = oauth_object.get_access_token()
# token = token_dict['access_token']
# # debugging access_token
# # print(token_dict['access_token'])

# # spotify object
# spotify_object=spotipy.Spotify(auth=token)


# user_response = await client.wait_for('message', timeout=20.0, check=check)
        
#         # split user response into song and artist
#         song, artist = map(str.strip, user_response.content.split("by"))
        
#         # search for songs by artist
#         genius = lg.Genius(genius_access_token)
#         songs = genius.search_songs(song, artist)
        
#         # create an embed message with the top 5 search results
#         embed = discord.Embed(title=f"Search results for '{song}' by '{artist}'", color=discord.Color.blurple())
        
#         for i, song in enumerate(songs[:5], start=1):
#             embed.add_field(name=f"{i}. {song.title}", value=song.artist, inline=False)
        
#         embed.set_footer(text="Enter a number from 1-5 to select a song.")
        
#         # send embed message
#         await message.channel.send(embed=embed)
        
#         # wait for user to select a song
#         user_response = await client.wait_for('message', timeout=20.0, check=check)
#         selection = int(user_response.content)
        
#         # retrieve lyrics for selected song
#         selected_song = songs[selection - 1]
#         lyrics = selected_song.lyrics.replace("Translations\n", "")
        
#         # split the lyrics into chunks of 2000 characters or less
#         lyrics_chunks = [lyrics[i:i+2000] for i in range(0, len(lyrics), 2000)]
        
#         # send each chunk as a separate message
#         for chunk in lyrics_chunks:
#             await message.channel.send(chunk)
    
#     except asyncio.TimeoutError:
#         await message.channel.send("Sorry, you took too long to respond.")



# OLD CODE
# if message.content.startswith('!lyrics'):
#             await message.channel.send("What song?")
        
#             user_response = await client.wait_for('message', timeout=20)
#             song_str = str(user_response.content)

#             await message.channel.send("Who's the artist?")
#             user_response = await client.wait_for('message', timeout=20)
#             artist_str = str(user_response.content)

#             # debugging 
#             print(f'You wanted the lyrics for {song_str} by {artist_str}')
            
#             # genius object
#             genius_object=lg.Genius(genius_access_token)
            
#             # finds song
#             song = genius_object.search_song(title=song_str, artist=artist_str)
#             if song is None:
#                 await message.channel.send("Sorry, I couldn't find the lyrics for that song.")
#             else:
#                 # retrieve the lyrics
#                 lyrics = song.lyrics
#                 print(lyrics)