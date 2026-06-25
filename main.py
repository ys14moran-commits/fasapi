from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Cliente(BaseModel):
    id: int
    nombre: str
    email: str
    edad: int

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    edad: Optional[int] = None

# Datos en memoria
lista_clientes = [
    Cliente(id=1, nombre="Lady", email="lady@gmail.com", edad=22),
    Cliente(id=2, nombre="Luis", email="luis@gmail.com", edad=19),
    Cliente(id=3, nombre="Ana", email="ana@gmail.com", edad=23)
]

@app.get("/clientes", response_model=List[Cliente])
def listar_clientes():
    return lista_clientes

@app.get("/clientes/{cliente_id}", response_model=Cliente)
def obtener_cliente(cliente_id: int):
    for cliente in lista_clientes:
        if cliente.id == cliente_id:
            return cliente
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

@app.put("/clientes/{cliente_id}", response_model=Cliente)
def actualizar_cliente(cliente_id: int, datos: ClienteUpdate):
    for cliente in lista_clientes:
        if cliente.id == cliente_id:
            # Actualizar solo los campos enviados
            if datos.nombre is not None:
                cliente.nombre = datos.nombre
            if datos.email is not None:
                cliente.email = datos.email
            if datos.edad is not None:
                cliente.edad = datos.edad
            return cliente
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")