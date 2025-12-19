from fastapi import FastAPI, Depends, HTTPException
from database import engine, SessionLocal, Base
from models import News,User
from schema import NewsCreate, NewsResponse, UserCreate, UserOut
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from ai import get_news_category
from jose import jwt,JWTError
from .auth import SECRET_KEY, ALGORITHM

News.__table__.create(bind=engine, checkfirst=True)
User.__table__.create(bind=engine, checkfirst=True)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from fastapi.responses import HTMLResponse

def get_current_user(token: str, db: Session):
    try: 
        payload = jwt.decode(token , SECRET_KEY,algorithms=ALGORITHM)
        user_id = payload.get('sub')
    except JWTError:
        raise HTTPException(status_code=401)

    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=401)

    return User

@app.get('/', response_class=HTMLResponse)
def hello():
    return """
    <html>
        <head>
            <title>News Analyzer API</title>
            <style>
                body { 
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
                    display: flex; align-items: center; justify-content: center; 
                    height: 100vh; margin: 0; background: #f0f2f5; color: #1c1e21;
                }
                .card { 
                    background: white; padding: 2rem; border-radius: 12px; 
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1); max-width: 400px; text-align: center;
                }
                h1 { color: #0070f3; margin-bottom: 10px; }
                p { line-height: 1.5; color: #666; }
                .status { 
                    display: inline-block; padding: 4px 12px; background: #e7f5ed; 
                    color: #0ca678; border-radius: 20px; font-size: 0.8rem; font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div class="card">
                <div class="status">● System Online</div>
                <h1>News Analyzer</h1>
                <p>An AI-powered engine that analyzes news and categorizes it into meaningful insights.</p>
                <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                <small style="color: #999;">v1.0.0 • Powered by Gemini AI</small>
            </div>
        </body>
    </html>
    """

@app.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return 

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