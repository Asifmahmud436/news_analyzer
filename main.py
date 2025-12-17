from fastapi import FastAPI, Depends, HTTPException
from database import engine, SessionLocal
from models import News
from schema import NewsBase, NewsCreate, NewsResponse
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from ai import get_news_category

app = FastAPI()

News.__table__.create(bind=engine, checkfirst=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/news')
def get_news(db : Session = Depends(get_db)):
    db_products = db.query(News).all()
    return db_products

@app.get("/news/{news_id}")
def get_a_news(news_id : int, db : Session = Depends(get_db)):
    db_news = db.query(News).filter(News.id == news_id).first()
    if db_news:
        return db_news
    raise HTTPException(status_code=404,detail="News not found")

@app.post("/news", response_model=NewsResponse)
def add_news(news: NewsCreate, db : Session = Depends(get_db)):
    db_item = News(headline = news.headline, body = news.body)
    db_item.categories = get_news_category(db_item.body)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.put('/news/{news_id}')
def update_news(news_id : int,given_news: NewsCreate ,db : Session = Depends(get_db)):
    db_product = db.query(News).filter(News.id == news_id).first()
    if db_product:
        db_product.body = given_news.body
        db_product.headline = given_news.headline
        db_product.categories = given_news.categories
        db.commit()
        return "Product added successfully"
    else:
        raise HTTPException(status_code=404, detail='Product not found')

@app.delete("/news")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(News).filter(News.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return 'Product deleted successfully'
    else:
        raise HTTPException(status_code=404, detail="Product not found")



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