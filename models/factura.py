from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from models.transaccion import TransaccionBase

class Factura(BaseModel):
    id: int
    fecha: date
    cliente_id: int

class FacturaCreate(BaseModel):
    fecha: date
    cliente_id: int
    transacciones: List[TransaccionBase] = []