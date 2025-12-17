from pydantic import BaseModel, Field
from datetime import datetime

class NewsBase(BaseModel):
    headline: str
    body : str
    category : str
    created_at : datetime = Field(default_factory=datetime.now())
    updated_at : datetime = Field(default_factory=datetime.now())
        
class NewsCreate(NewsBase):
    pass

class NewsResponse(NewsBase):
    id : int
    class Config:
        from_attributes = True