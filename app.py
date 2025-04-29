# --- import ของ Bot
import discord
import random
import requests
from discord.ext import commands, tasks
import os
import asyncio

# --- import ของ FastAPI
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# ============================ BOT CONFIG ============================

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1257722979463467074

API_URL = '/random'

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

# ============================ FASTAPI CONFIG ============================

# สร้างตารางใน DB
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://my-love-gacha.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Message(BaseModel):
    content: str

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

@app.post("/add")
def add_message(message: Message, db: Session = Depends(get_db)):
    db_message = models.LoveMessage(content=message.content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return {"message": "เพิ่มข้อความเรียบร้อยแล้ว"}

@app.post("/add_many")
def add_many_messages(messages: list[Message], db: Session = Depends(get_db)):
    db_messages = [models.LoveMessage(content=m.content) for m in messages]
    db.add_all(db_messages)
    db.commit()
    return {"message": f"เพิ่ม {len(db_messages)} ข้อความเรียบร้อยแล้ว"}

@app.get("/random")
def get_random_message(db: Session = Depends(get_db)):
    messages = db.query(models.LoveMessage).all()
    if not messages:
        return {"message": "ยังไม่มีข้อความในฐานข้อมูล"}
    message = random.choice(messages)
    return {"message": message.content}

@app.get("/count")
def count_messages(db: Session = Depends(get_db)):
    count = db.query(models.LoveMessage).count()
    return {"count": count}

# ============================ RUN BOT พร้อม FASTAPI ============================

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot.start(TOKEN))
