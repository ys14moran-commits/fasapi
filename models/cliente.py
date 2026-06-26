from pydantic import BaseModel
from typing import Optional

class Cliente(BaseModel):
    id: int
    nombre: str
    email: str
    edad: int

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    edad: Optional[int] = None