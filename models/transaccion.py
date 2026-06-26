from pydantic import BaseModel

class Transaccion(BaseModel):
    id: int
    cantidad: int
    vr_unitario: float
    descripcion: str
    factura_id: int

class TransaccionBase(BaseModel):
    cantidad: int
    vr_unitario: float
    descripcion: str

class TransaccionResponse(BaseModel):
    id: int
    cantidad: int
    vr_unitario: float
    descripcion: str
    factura_id: int
    total: float = 0.0