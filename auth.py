from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv

SECRET_KEY = os.getenv("SECRET_KEY") 
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({'exp':expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)