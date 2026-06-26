from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from fastapi import FastAPI
from routers import clientes_router
from fastapi import FastAPI
from routers import clientes_router, facturas_router, transacciones_router


app = FastAPI()

app.include_router(clientes_router)
app.include_router(clientes_router)
app.include_router(facturas_router)
app.include_router(transacciones_router)

@app.get("/")
def root():
    return {"message": "API funcionando"}

class Cliente(BaseModel):
    id: int
    nombre: str
    email: str
    edad: int

class Factura(BaseModel):
    id: int
    fecha: date
    cliente_id: int

class Transaccion(BaseModel):
    id: int
    cantidad: int
    vr_unitario: float
    descripcion: str
    factura_id: int

lista_clientes = []
lista_facturas = []
lista_transacciones = []

@app.get("/clientes", response_model=List[Cliente])
def listar_clientes():
    return lista_clientes

@app.get("/clientes/{cliente_id}", response_model=Cliente)
def obtener_cliente(cliente_id: int):
    for cliente in lista_clientes:
        if cliente.id == cliente_id:
            return cliente
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

@app.post("/clientes", response_model=Cliente, status_code=status.HTTP_201_CREATED)
def crear_cliente(cliente: Cliente):
    lista_clientes.append(cliente)
    return cliente

@app.get("/facturas", response_model=List[Factura])
def listar_facturas():
    return lista_facturas

@app.post("/facturas", response_model=Factura, status_code=status.HTTP_201_CREATED)
def crear_factura(factura: Factura):
    lista_facturas.append(factura)
    return factura

@app.get("/transacciones", response_model=List[Transaccion])
def listar_transacciones():
    return lista_transacciones

@app.post("/transacciones", response_model=Transaccion, status_code=status.HTTP_201_CREATED)
def crear_transaccion(transaccion: Transaccion):
    lista_transacciones.append(transaccion)
    return transaccion
@app.get("/facturas/{factura_id}", response_model=Factura)
def obtener_factura(factura_id: int):
    for factura in lista_facturas:
        if factura.id == factura_id:
            return factura
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada")

class TransaccionBase(BaseModel):
    cantidad: int
    vr_unitario: float
    descripcion: str

class FacturaCreate(BaseModel):
    fecha: date
    cliente_id: int
    transacciones: List[TransaccionBase] = []

@app.post("/facturas", response_model=Factura, status_code=status.HTTP_201_CREATED)
def crear_factura(factura_data: FacturaCreate):
    # Verificar que el cliente existe
    cliente_existe = False
    for cliente in lista_clientes:
        if cliente.id == factura_data.cliente_id:
            cliente_existe = True
            break
    if not cliente_existe:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    nueva_factura = Factura(
        id=len(lista_facturas) + 1,
        fecha=factura_data.fecha,
        cliente_id=factura_data.cliente_id
    )
    lista_facturas.append(nueva_factura)
    
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

class TransaccionResponse(BaseModel):
    id: int
    cantidad: int
    vr_unitario: float
    descripcion: str
    factura_id: int
    total: float = 0.0

@app.get("/transacciones", response_model=List[TransaccionResponse])
def listar_transacciones():
    transacciones_con_total = []
    for trans in lista_transacciones:
        trans_dict = trans.dict()
        trans_dict["total"] = trans.cantidad * trans.vr_unitario
        transacciones_con_total.append(TransaccionResponse(**trans_dict))
    return transacciones_con_total