from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from .transaccion import TransaccionResponse, TransaccionBase

# =============================================
# FACTURA ORIGINAL (con cliente)
# =============================================
class FacturaBase(BaseModel):
    fecha: date
    cliente_id: int

class FacturaCreate(FacturaBase):
    pass

class FacturaCreateWithTransacciones(FacturaBase):
    transacciones: Optional[List[TransaccionBase]] = []

class FacturaUpdate(BaseModel):
    fecha: Optional[date] = None
    cliente_id: Optional[int] = None

class FacturaResponse(FacturaBase):
    id: int
    transacciones: List[TransaccionResponse] = []

    class Config:
        from_attributes = True


# =============================================
# FACTURA SIMPLE (sin cliente)
# =============================================
class FacturaSimpleBase(BaseModel):
    fecha: date

class FacturaSimpleCreate(FacturaSimpleBase):
    pass

class FacturaSimpleUpdate(BaseModel):
    fecha: Optional[date] = None

class FacturaSimpleResponse(FacturaSimpleBase):
    id: int
    transacciones: List[TransaccionResponse] = []

    class Config:
        from_attributes = True