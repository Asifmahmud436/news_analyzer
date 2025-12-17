from pydantic import BaseModel
from datetime import datetime
from typing import List

class NewsBase(BaseModel):
    headline: str
    body : str
    
class NewsCreate(NewsBase):
    pass

class NewsResponse(NewsBase):
    id : int
    categories : List[str]
    created_at : datetime
    updated_at : datetime
    class Config:
        from_attributes = True