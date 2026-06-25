from pydantic import BaseModel, EmailStr
from typing import List, Optional
from .factura import FacturaResponse

class ClienteBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None

class ClienteResponse(ClienteBase):
    id: int
    facturas: List[FacturaResponse] = []

    class Config:
        from_attributes = True