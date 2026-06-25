from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

lista_clientes = [
    {"id": 1, "nombre": "Lady", "email": "lady@gmail.com", "edad": 22},
    {"id": 2, "nombre": "Luis", "email": "luis@gmail.com", "edad": 19},
    {"id": 3, "nombre": "Ana", "email": "ana@gmail.com", "edad": 23}
]

@app.get("/clientes")
def listar_clientes():
    return lista_clientes

@app.get("/clientes/{cliente_id}")
def obtener_cliente(cliente_id: int):
    for cliente in lista_clientes:
        if cliente["id"] == cliente_id:
            return cliente
    return {"error": "Cliente no encontrado"}