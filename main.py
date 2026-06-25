from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI()

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