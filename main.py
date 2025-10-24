import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import datetime
load_dotenv()
token = os.getenv("token")

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='>', intents=intents)

@bot.event
async def on_ready():
    print('------')

l = dict()

@bot.event
async def on_message(message):
    log = bot.get_channel(1431252035696590872)
    if message.author == bot.user:
        return
    await log.send(f"{message.author.mention} sended message at {message.created_at.strftime("%Y-%m-%d %H:%M:%S")} that contained '{message.content}'")
    

@bot.event
async def on_voice_state_update(member, before, after):
    log = bot.get_channel(1431252035696590872)
    if before.channel is None and after.channel is not None:
        temp = await log.send(f'{member.mention} присоединился к каналу: {member.voice.channel}. Время входа: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        l.update({member : temp})
        print(l)
    elif before.channel is not None and after.channel is None:
        await log.send(f'{member.mention} покинул канал: {before.channel}. Время пребывания: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - {member.joined_at.strftime("%Y-%m-%d %H:%M:%S")}.')
    elif before.channel is not None and after.channel is not None:
        await log.send(f'{member.mention} перешел в канал: {after.channel} из {before.channel}.')

bot.run(token)
