from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from pydantic import BaseModel
import random
from fastapi.middleware.cors import CORSMiddleware

# สร้างตารางใน DB
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ Add this section
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
