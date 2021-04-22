import os
import discord
from discord.ext import commands
import DiscordUtils

bot = commands.AutoShardedBot(command_prefix="m ")
bot.remove_command('help')
music = DiscordUtils.Music()

@bot.command()
async def join(ctx):
      await ctx.author.voice.channel.connect() 
      await ctx.send('**Succsesfully Joined!!** Now Play Some Music <a:party:834824007860617270>')
      
@bot.command()
async def leave(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    if player: player.delete()
    await ctx.voice_client.disconnect()
    await ctx.send('All Good Things Must Come To An End <a:bye:834762050403172393>') 

@bot.command()
async def play(ctx, *, url):
    await ctx.send('<a:loading:834824011719639060> searching for the song........')
    player = music.get_player(guild_id=ctx.guild.id)
    if not player:
        player = music.create_player(ctx, ffmpeg_error_betterfix=True)
    if not ctx.voice_client.is_playing():
        await player.queue(url, search=True)
        song = await player.play()
        await ctx.send(f"Now Playing: **{song.name}** <a:np:834824012370149376>")
    else:
        song = await player.queue(url, search=True)
        await ctx.send(f"Queued: **{song.name}** <a:np:834824012370149376>")

@bot.command()
async def pause(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.pause()
    await ctx.send(f"Paused: **{song.name}** <a:remove:834824007604895764>")

@bot.command()
async def resume(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.resume()
    await ctx.send(f"Resumed: **{song.name}** <a:loading:834824007681179698> ")


@bot.command()
async def loop(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.toggle_song_loop()
    if song.is_looping:
        await ctx.send(f"Enabled loop for : **{song.name}** <a:loading:834824007681179698>")
    else:
        await ctx.send(f"Disabled loop for: **{song.name}** <a:loading:834824007681179698>")

@bot.command()
async def queue(ctx):
    embedVar = discord.Embed(title="Queue <a:loading:834824007681179698>",value=None,color=0x00ff00)
    player = music.get_player(guild_id=ctx.guild.id)
    i=0
    for song in player.current_queue():
      embedVar.add_field(name=f'Song Number: {i}',value=f'{song.name}',inline=False)
      i+=1
    await ctx.send(embed=embedVar)
    

@bot.command()
async def np(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = player.now_playing()
    await ctx.send('Now Playing : **'+song.name+'** <a:np:834824012370149376>')

@bot.command()
async def skip(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    data = await player.skip(force=True)
    await ctx.send(f"Skipped **{data[0].name}** <:skip:834824011367972875>")

@bot.command()
async def remove(ctx, index):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.remove_from_queue(int(index))

    await ctx.send(f"Removed {song.name} from queue <a:remove:834824007604895764>")

@bot.group(invoke_without_command=True)
async def help(message):
  embedVar = discord.Embed(title="Help Commands For Musician Bot", description="Here is the list of help commands!", color=0x00ff00)
  embedVar.add_field(name="m join", value="To Join The VC", inline=False)
  embedVar.add_field(name="m leave", value="Leaves The VC", inline=False)
  embedVar.add_field(name="m play [URL/video_name]", value='plays a song add song name/URl after command', inline=False)
  embedVar.add_field(name="m pause", value="Pauses the Current song", inline=False)
  embedVar.add_field(name="m resume", value="To Resueme the current song", inline=False)
  embedVar.add_field(name="m loop", value="To Loop Current Song", inline=False)
  embedVar.add_field(name="m np", value="Shows The Current Playing Song", inline=False)
  embedVar.add_field(name="m skip", value="Skip The Current Song", inline=False)
  embedVar.add_field(name="m remove [song_index]", value="Removes a song (mention index of song from queue)", inline=False)
  embedVar.add_field(name="Credits", value = "[Realhardik18](https://realhardik18.github.io/) | [Doodle Anna](https://discord.com/oauth2/authorize?client_id=815923574200074241&permissions=8&scope=bot)", inline=False)
  embedVar.add_field(name="Add", value="To add this bot in your server click [here](https://discord.com/oauth2/authorize?client_id=834456455225540698&permissions=0&scope=bot)", inline=False)
  await message.channel.send(embed=embedVar)

bot.run(my_secret)

