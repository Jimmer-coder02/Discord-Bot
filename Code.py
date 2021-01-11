import discord
from discord.ext import commands, tasks
import random
from random import choice
from discord.voice_client import VoiceClient
import youtube_dl
import asyncio

youtube_dl.utils.bug_reports_message = lambda: ''

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

client = commands.Bot(command_prefix = '.')



@client.event
async def on_ready():
    print('Bot online')
    

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left a server.')



@client.command(name='clear', help='This command clears messages')
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


@client.command(name='kick', help='This command kicks a player')
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)


@client.command(name='ban', help='This command bans a player')
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned{member.mention}')


@client.command(name='unban', help='This command unbans a player')
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users: 
        user = ban_entry.user 

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

@client.command(name='ping', help='This command returns the latency')
async def ping(ctx):
    await ctx.send(f'**Pong!** Latency: {round(client.latency * 1000)}ms')

@client.command(name='hello', help='This command returns a random welcome message')
async def hello(ctx):
    responses = ['Top of the morning to you lad!', 'Hello, how are you?', 'Hi', '**Wasssuup!**']
    await ctx.send(choice(responses))

@client.command(name='join', help='This command makes the bot join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return
    
    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()


@client.command(name='leave', help='This command stops makes the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()


@client.command(name='8ball', help='This command returns a random answer')
async def ball(ctx):
    responses2 = ['Yes', 'No', 'Probably', 'It is certain.', 'Signs point to yes.', 'Yes – definitely.','Without a doubt.',' Most likely.','Dont count on it.','My reply is no.', 'Very doubtful.', ' My sources say no.', 'Outlook not so good.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.' ]
    await ctx.send(choice(responses2))


    




client.run('Your Token')    
