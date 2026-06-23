from pydantic import BaseModel, EmailStr
from datetime import date
from typing import List, Optional


# ──────────────────────────────────────────
# Transaccion
# ──────────────────────────────────────────
class TransaccionBase(BaseModel):
    cantidad: int
    vr_unitario: float
    descripcion: str


class TransaccionCreate(TransaccionBase):
    factura_id: int


class TransaccionUpdate(BaseModel):
    cantidad: Optional[int] = None
    vr_unitario: Optional[float] = None
    descripcion: Optional[str] = None


class TransaccionResponse(TransaccionBase):
    id: int
    factura_id: int
    total: float = 0.0

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        instance = super().from_orm(obj)
        instance.total = obj.cantidad * obj.vr_unitario
        return instance


# ──────────────────────────────────────────
# Factura
# ──────────────────────────────────────────
class FacturaBase(BaseModel):
    fecha: date
    cliente_id: int


class FacturaCreate(FacturaBase):
    pass


class FacturaUpdate(BaseModel):
    fecha: Optional[date] = None
    cliente_id: Optional[int] = None


class FacturaResponse(FacturaBase):
    id: int
    transacciones: List[TransaccionResponse] = []

    class Config:
        from_attributes = True


# ──────────────────────────────────────────
# Cliente
# ──────────────────────────────────────────
class ClienteBase(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None


class ClienteResponse(ClienteBase):
    id: int
    facturas: List[FacturaResponse] = []

    class Config:
        from_attributes = True
