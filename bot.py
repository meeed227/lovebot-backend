# bot.py
import discord
import random
import requests
from discord.ext import commands, tasks
import os

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = '';

API_URL = '/random'  # ชี้ไปที่ FastAPI

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def fetch_random_message():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()['message']
    except Exception as e:
        print(f"Error fetching message: {e}")
    return "ขออภัย บอทมีปัญหา 😢"

@bot.event
async def on_ready():
    print(f'✅ Bot ติดแล้ว: {bot.user}')
    send_love.start()

@tasks.loop(minutes=300)
async def send_love():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        message = fetch_random_message()
        await channel.send(message)

@bot.command()
async def บอกรัก(ctx):
    message = fetch_random_message()
    await ctx.send(message)

bot.run(TOKEN)
