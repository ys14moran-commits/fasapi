from fastapi import APIRouter, HTTPException, status
from typing import List
from models.factura import Factura, FacturaCreate
from models.transaccion import Transaccion

router = APIRouter(prefix="/facturas", tags=["Facturas"])

# Datos en memoria (global)
lista_facturas = []
lista_transacciones = []

@router.get("/", response_model=List[Factura])
def listar_facturas():
    return lista_facturas

@router.get("/{factura_id}", response_model=Factura)
def obtener_factura(factura_id: int):
    for factura in lista_facturas:
        if factura.id == factura_id:
            return factura
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada")

@router.post("/", response_model=Factura, status_code=status.HTTP_201_CREATED)
def crear_factura(factura_data: FacturaCreate):
    from routers.clientes import lista_clientes
    
    # Verificar cliente
    cliente_existe = any(c.id == factura_data.cliente_id for c in lista_clientes)
    if not cliente_existe:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Crear factura
    nueva_factura = Factura(
        id=len(lista_facturas) + 1,
        fecha=factura_data.fecha,
        cliente_id=factura_data.cliente_id
    )
    lista_facturas.append(nueva_factura)
    
    # Crear transacciones
    for trans_data in factura_data.transacciones:
        nueva_trans = Transaccion(
            id=len(lista_transacciones) + 1,
            cantidad=trans_data.cantidad,
            vr_unitario=trans_data.vr_unitario,
            descripcion=trans_data.descripcion,
            factura_id=nueva_factura.id
        )
        lista_transacciones.append(nueva_trans)
    
    return nueva_factura