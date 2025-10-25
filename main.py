import discord
from discord.ext import commands, tasks
import os
import asyncio
from dotenv import load_dotenv
import datetime
load_dotenv()
token = os.getenv("token")

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='>', intents=intents)

@bot.event
async def on_ready():
    print('------')

voice_sessions = dict()

@bot.event
async def on_message(message):
    log = bot.get_channel(1431724171548688598)
    if message.author == bot.user:
        return
    
    embed = discord.Embed(
        title="📨 Новое сообщение",
        color=discord.Color.blue(),
        timestamp=message.created_at
    )
    embed.add_field(name="Отправитель", value=message.author.mention, inline=True)
    embed.add_field(name="Канал", value=f"<#{message.channel.id}>", inline=True)
    
    if message.content:
        embed.add_field(name="Содержание", value=f"```\n{message.content}\n```", inline=False)
    
    if message.attachments:
        embed.add_field(name="Вложения", value=f"Количество: {len(message.attachments)}", inline=False)
        await log.send(embed=embed)
        for attachment in message.attachments:
            await log.send(attachment.url)
    else:
        await log.send(embed=embed)

@bot.event
async def on_voice_state_update(member, before, after):
    log = bot.get_channel(1431724205824671856)
    
    if before.channel != after.channel:
        if before.channel is None and after.channel is not None:
            embed = discord.Embed(
                title="🔊 Вход в голосовой канал",
                color=discord.Color.green(),
                timestamp=datetime.datetime.now()
            )
            embed.add_field(name="Пользователь", value=member.mention, inline=True)
            embed.add_field(name="Канал", value=after.channel.name, inline=True)
            
            temp = await log.send(embed=embed)
            voice_sessions.update({member : [temp, after.channel, datetime.datetime.now()]})
            return
            
        elif before.channel is not None and after.channel is None:
            duration = datetime.datetime.now() - voice_sessions.get(member)[2]
            
            embed = discord.Embed(
                title="🔇 Выход из голосового канала",
                color=discord.Color.red(),
                timestamp=datetime.datetime.now()
            )
            embed.add_field(name="Пользователь", value=member.mention, inline=True)
            embed.add_field(name="Канал", value=before.channel.name, inline=True)
            embed.add_field(name="Время пребывания", value=str(duration)[:7], inline=False)
            
            await voice_sessions.get(member)[0].reply(embed=embed)
            thread = voice_sessions.get(member)[0].thread
            if thread:
                await thread.edit(archived=True, locked=True)
            return
            
        elif before.channel is not None and after.channel is not None:
            if voice_sessions.get(member)[0].thread:
                thread = voice_sessions.get(member)[0].thread
            else:
                thread = await voice_sessions.get(member)[0].create_thread(name=f"{member.name} история", auto_archive_duration=60)
            
            embed = discord.Embed(
                title="↔️ Переход между каналами",
                color=discord.Color.orange(),
                timestamp=datetime.datetime.now()
            )
            embed.add_field(name="Пользователь", value=member.mention, inline=False)
            embed.add_field(name="Из канала", value=before.channel.name, inline=True)
            embed.add_field(name="В канал", value=after.channel.name, inline=True)
            
            await thread.send(embed=embed)
            return

    if voice_sessions.get(member)[0].thread:
        thread = voice_sessions.get(member)[0].thread
    else:
        thread = await voice_sessions.get(member)[0].create_thread(name=f"{member.name} история", auto_archive_duration=60)

    embed = discord.Embed(
        title="🎙️ Изменение голосового состояния",
        color=discord.Color.purple(),
        timestamp=datetime.datetime.now()
    )
    embed.add_field(name="Пользователь", value=member.mention, inline=True)
    embed.add_field(name="Канал", value=after.channel.name, inline=True)
    
    changes = []
    
    if before.mute != after.mute:
        if after.mute:
            changes.append("🔇 Был замучен модератором")
        else:
            changes.append("🔊 Был размучен модератором")
    
    if before.self_mute != after.self_mute:
        if after.self_mute:
            changes.append("🔇 Сам замутил микрофон")
        else:
            changes.append("🔊 Сам размутил микрофон")
    
    if before.deaf != after.deaf:
        if after.deaf:
            changes.append("🔇 Был оглушен модератором")
        else:
            changes.append("🔊 Был разоглушен модератором")
    
    if before.self_deaf != after.self_deaf:
        if after.self_deaf:
            changes.append("🔇 Сам отключил звук")
        else:
            changes.append("🔊 Сам включил звук")
    
    if before.self_video != after.self_video:
        if after.self_video:
            changes.append("📹 Включил видео")
        else:
            changes.append("📹 Выключил видео")
    
    if before.self_stream != after.self_stream:
        if after.self_stream:
            changes.append("🎬 Начал стримить")
        else:
            changes.append("🎬 Закончил стримить")
    
    if changes:
        embed.add_field(name="Изменения", value="\n".join(changes), inline=False)
        await thread.send(embed=embed)

bot.run(token)