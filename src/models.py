from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ItemBase(BaseModel):
    nome: str
    idade: int

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    nome: Optional[str] = None
    idade: Optional[int] = None

class Item(ItemBase):
    id: int
    
    class Config:
        orm_mode = True

class ResponseMessage(BaseModel):
    message: str