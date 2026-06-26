from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI(
    title="API Facturación",
    description="Gestión de Clientes, Facturas y Transacciones",
    version="1.0.0"
)


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

class TransaccionBase(BaseModel):
    cantidad: int
    vr_unitario: float
    descripcion: str

class FacturaCreate(BaseModel):
    fecha: date
    cliente_id: int
    transacciones: List[TransaccionBase] = []

class TransaccionResponse(BaseModel):
    id: int
    cantidad: int
    vr_unitario: float
    descripcion: str
    factura_id: int
    total: float = 0.0


lista_clientes = [
    Cliente(id=1, nombre="Ladi", email="ladi5@gmail.com", edad=22),
    Cliente(id=2, nombre="Luis", email="luis2@gmail.com", edad=19),
    Cliente(id=3, nombre="Ana", email="ana5@gmail.com", edad=23)
]

lista_facturas = []
lista_transacciones = []

@app.get("/clientes", response_model=List[Cliente])
def listar_clientes():
    """Lista todos los clientes"""
    return lista_clientes

@app.get("/clientes/{cliente_id}", response_model=Cliente)
def obtener_cliente(cliente_id: int):
    """Obtiene un cliente por ID"""
    for cliente in lista_clientes:
        if cliente.id == cliente_id:
            return cliente
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Cliente {cliente_id} no encontrado"
    )

@app.post("/clientes", response_model=Cliente, status_code=status.HTTP_201_CREATED)
def crear_cliente(cliente: Cliente):
    """Crea un nuevo cliente"""
    # Verificar si el ID ya existe
    for c in lista_clientes:
        if c.id == cliente.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un cliente con ID {cliente.id}"
            )
    lista_clientes.append(cliente)
    return cliente

@app.put("/clientes/{cliente_id}", response_model=Cliente)
def actualizar_cliente(cliente_id: int, datos: dict):
    """Actualiza un cliente existente"""
    for i, cliente in enumerate(lista_clientes):
        if cliente.id == cliente_id:
            # Actualizar solo los campos enviados
            if "nombre" in datos:
                cliente.nombre = datos["nombre"]
            if "email" in datos:
                cliente.email = datos["email"]
            if "edad" in datos:
                cliente.edad = datos["edad"]
            return cliente
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Cliente {cliente_id} no encontrado"
    )

@app.delete("/clientes/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente(cliente_id: int):
    """Elimina un cliente"""
    for i, cliente in enumerate(lista_clientes):
        if cliente.id == cliente_id:
            lista_clientes.pop(i)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Cliente {cliente_id} no encontrado"
    )


@app.get("/facturas", response_model=List[Factura])
def listar_facturas():
    """Lista todas las facturas"""
    return lista_facturas

@app.get("/facturas/{factura_id}", response_model=Factura)
def obtener_factura(factura_id: int):
    """Obtiene una factura por ID"""
    for factura in lista_facturas:
        if factura.id == factura_id:
            return factura
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Factura {factura_id} no encontrada"
    )

@app.post("/facturas", response_model=Factura, status_code=status.HTTP_201_CREATED)
def crear_factura(factura_data: FacturaCreate):
    """
    Crea una nueva factura con transacciones opcionales.
    Verifica que el cliente exista antes de crear.
    """
    
    cliente_existe = False
    for cliente in lista_clientes:
        if cliente.id == factura_data.cliente_id:
            cliente_existe = True
            break
    
    if not cliente_existe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente {factura_data.cliente_id} no encontrado"
        )
    
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

@app.put("/facturas/{factura_id}", response_model=Factura)
def actualizar_factura(factura_id: int, datos: dict):
    """Actualiza una factura existente"""
    for factura in lista_facturas:
        if factura.id == factura_id:
            if "fecha" in datos:
                factura.fecha = datos["fecha"]
            if "cliente_id" in datos:
                # Verificar que el nuevo cliente existe
                cliente_existe = False
                for c in lista_clientes:
                    if c.id == datos["cliente_id"]:
                        cliente_existe = True
                        break
                if not cliente_existe:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Cliente {datos['cliente_id']} no encontrado"
                    )
                factura.cliente_id = datos["cliente_id"]
            return factura
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Factura {factura_id} no encontrada"
    )

@app.delete("/facturas/{factura_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_factura(factura_id: int):
    """Elimina una factura y sus transacciones"""
    for i, factura in enumerate(lista_facturas):
        if factura.id == factura_id:
            # Eliminar transacciones asociadas
            global lista_transacciones
            lista_transacciones = [t for t in lista_transacciones if t.factura_id != factura_id]
            lista_facturas.pop(i)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Factura {factura_id} no encontrada"
    )

@app.get("/transacciones", response_model=List[TransaccionResponse])
def listar_transacciones():
    """Lista todas las transacciones con su total calculado"""
    transacciones_con_total = []
    for trans in lista_transacciones:
        trans_dict = trans.dict()

        trans_dict["total"] = trans.cantidad * trans.vr_unitario
        transacciones_con_total.append(TransaccionResponse(**trans_dict))
    return transacciones_con_total

@app.get("/transacciones/{transaccion_id}", response_model=Transaccion)
def obtener_transaccion(transaccion_id: int):
    """Obtiene una transacción por ID"""
    for trans in lista_transacciones:
        if trans.id == transaccion_id:
            return trans
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Transacción {transaccion_id} no encontrada"
    )

@app.post("/transacciones", response_model=Transaccion, status_code=status.HTTP_201_CREATED)
def crear_transaccion(transaccion: Transaccion):
    """Crea una nueva transacción"""
    # Verificar que la factura existe
    factura_existe = False
    for f in lista_facturas:
        if f.id == transaccion.factura_id:
            factura_existe = True
            break
    
    if not factura_existe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Factura {transaccion.factura_id} no encontrada"
        )
    
    lista_transacciones.append(transaccion)
    return transaccion

@app.put("/transacciones/{transaccion_id}", response_model=Transaccion)
def actualizar_transaccion(transaccion_id: int, datos: dict):
    """Actualiza una transacción existente"""
    for trans in lista_transacciones:
        if trans.id == transaccion_id:
            if "cantidad" in datos:
                trans.cantidad = datos["cantidad"]
            if "vr_unitario" in datos:
                trans.vr_unitario = datos["vr_unitario"]
            if "descripcion" in datos:
                trans.descripcion = datos["descripcion"]
            if "factura_id" in datos:
                # Verificar que la nueva factura existe
                factura_existe = False
                for f in lista_facturas:
                    if f.id == datos["factura_id"]:
                        factura_existe = True
                        break
                if not factura_existe:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Factura {datos['factura_id']} no encontrada"
                    )
                trans.factura_id = datos["factura_id"]
            return trans
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Transacción {transaccion_id} no encontrada"
    )

@app.delete("/transacciones/{transaccion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_transaccion(transaccion_id: int):
    """Elimina una transacción"""
    for i, trans in enumerate(lista_transacciones):
        if trans.id == transaccion_id:
            lista_transacciones.pop(i)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Transacción {transaccion_id} no encontrada"
    )

# =============================================
# ENDPOINT DE INICIO
# =============================================

@app.get("/")
def root():
    return {
        "message": "API de Facturación funcionando",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {
        "status": "OK",
        "clientes": len(lista_clientes),
        "facturas": len(lista_facturas),
        "transacciones": len(lista_transacciones)
    }