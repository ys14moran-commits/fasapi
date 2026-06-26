from fastapi import APIRouter, HTTPException, status
from typing import List
from models.cliente import Cliente, ClienteUpdate

router = APIRouter(prefix="/clientes", tags=["Clientes"])

lista_clientes = []

@router.get("/", response_model=List[Cliente])
def listar_clientes():
    return lista_clientes

@router.get("/{cliente_id}", response_model=Cliente)
def obtener_cliente(cliente_id: int):
    for cliente in lista_clientes:
        if cliente.id == cliente_id:
            return cliente
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

@router.post("/", response_model=Cliente, status_code=status.HTTP_201_CREATED)
def crear_cliente(cliente: Cliente):
    lista_clientes.append(cliente)
    return cliente

@router.put("/{cliente_id}", response_model=Cliente)
def actualizar_cliente(cliente_id: int, datos: ClienteUpdate):
    for cliente in lista_clientes:
        if cliente.id == cliente_id:
            if datos.nombre is not None:
                cliente.nombre = datos.nombre
            if datos.email is not None:
                cliente.email = datos.email
            if datos.edad is not None:
                cliente.edad = datos.edad
            return cliente
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente(cliente_id: int):
    for i, cliente in enumerate(lista_clientes):
        if cliente.id == cliente_id:
            lista_clientes.pop(i)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")