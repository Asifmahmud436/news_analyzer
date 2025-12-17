from fastapi import FastAPI, Depends, HTTPException
from database import engine, SessionLocal
from models import News
from schema import NewsBase, NewsCreate, NewsResponse
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()







origins = [
    "http://localhost:3000",    # React default
    "http://localhost:5173",    # Vite default
    "https://your-app.vercel.app" # Production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)