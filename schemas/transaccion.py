from pydantic import BaseModel
from typing import Optional

# =============================================
# TRANSACCION ORIGINAL (con factura_id)
# =============================================
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


# =============================================
# TRANSACCION SIMPLE (con factura_simple_id)
# =============================================
class TransaccionSimpleBase(BaseModel):
    cantidad: int
    vr_unitario: float
    descripcion: str

class TransaccionSimpleCreate(TransaccionSimpleBase):
    factura_simple_id: int

class TransaccionSimpleUpdate(BaseModel):
    cantidad: Optional[int] = None
    vr_unitario: Optional[float] = None
    descripcion: Optional[str] = None

class TransaccionSimpleResponse(TransaccionSimpleBase):
    id: int
    factura_simple_id: int
    total: float = 0.0

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        instance = super().from_orm(obj)
        instance.total = obj.cantidad * obj.vr_unitario
        return instance