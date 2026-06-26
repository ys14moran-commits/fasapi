from fastapi import APIRouter, HTTPException, status
from typing import List
from models.transaccion import Transaccion, TransaccionResponse

router = APIRouter(prefix="/transacciones", tags=["Transacciones"])

# Datos en memoria (global)
lista_transacciones = []

@router.get("/", response_model=List[TransaccionResponse])
def listar_transacciones():
    transacciones_con_total = []
    for trans in lista_transacciones:
        trans_dict = trans.dict()
        trans_dict["total"] = trans.cantidad * trans.vr_unitario
        transacciones_con_total.append(TransaccionResponse(**trans_dict))
    return transacciones_con_total

@router.get("/{transaccion_id}", response_model=Transaccion)
def obtener_transaccion(transaccion_id: int):
    for trans in lista_transacciones:
        if trans.id == transaccion_id:
            return trans
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transacción no encontrada")

@router.post("/", response_model=Transaccion, status_code=status.HTTP_201_CREATED)
def crear_transaccion(transaccion: Transaccion):
    from routers.facturas import lista_facturas
    
    # Verificar factura
    factura_existe = any(f.id == transaccion.factura_id for f in lista_facturas)
    if not factura_existe:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    lista_transacciones.append(transaccion)
    return transaccion