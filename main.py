from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

import models
import schemas
from database import engine, get_db

# Crear tablas al iniciar
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Facturación",
    description="Gestión de Clientes, Facturas y Transacciones",
    version="1.0.0",
)


# ══════════════════════════════════════════════════════════
#  CLIENTES
# ══════════════════════════════════════════════════════════

@app.get("/clientes", response_model=List[schemas.ClienteResponse], tags=["Clientes"])
def listar_clientes(db: Session = Depends(get_db)):
    """Retorna todos los clientes."""
    return db.query(models.Cliente).all()


@app.get("/clientes/{cliente_id}", response_model=schemas.ClienteResponse, tags=["Clientes"])
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Retorna un cliente por ID."""
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail=f"Cliente {cliente_id} no encontrado")
    return cliente


@app.post("/clientes", response_model=schemas.ClienteResponse, status_code=status.HTTP_201_CREATED, tags=["Clientes"])
def crear_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    """Crea un nuevo cliente."""
    existe = db.query(models.Cliente).filter(models.Cliente.email == cliente.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe un cliente con ese email")
    db_cliente = models.Cliente(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


@app.put("/clientes/{cliente_id}", response_model=schemas.ClienteResponse, tags=["Clientes"])
def actualizar_cliente(cliente_id: int, datos: schemas.ClienteUpdate, db: Session = Depends(get_db)):
    """Actualiza los datos de un cliente."""
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail=f"Cliente {cliente_id} no encontrado")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(cliente, campo, valor)
    db.commit()
    db.refresh(cliente)
    return cliente


@app.delete("/clientes/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Clientes"])
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Elimina un cliente por ID."""
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail=f"Cliente {cliente_id} no encontrado")
    db.delete(cliente)
    db.commit()


# ══════════════════════════════════════════════════════════
#  FACTURAS
# ══════════════════════════════════════════════════════════

@app.get("/facturas", response_model=List[schemas.FacturaResponse], tags=["Facturas"])
def listar_facturas(db: Session = Depends(get_db)):
    """Retorna todas las facturas."""
    return db.query(models.Factura).all()


@app.get("/facturas/{factura_id}", response_model=schemas.FacturaResponse, tags=["Facturas"])
def obtener_factura(factura_id: int, db: Session = Depends(get_db)):
    """Retorna una factura por ID, incluyendo sus transacciones."""
    factura = db.query(models.Factura).filter(models.Factura.id == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail=f"Factura {factura_id} no encontrada")
    return factura


@app.post("/facturas", response_model=schemas.FacturaResponse, status_code=status.HTTP_201_CREATED, tags=["Facturas"])
def crear_factura(factura: schemas.FacturaCreate, db: Session = Depends(get_db)):
    """Crea una nueva factura asociada a un cliente."""
    cliente = db.query(models.Cliente).filter(models.Cliente.id == factura.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail=f"Cliente {factura.cliente_id} no encontrado")
    db_factura = models.Factura(**factura.model_dump())
    db.add(db_factura)
    db.commit()
    db.refresh(db_factura)
    return db_factura


@app.put("/facturas/{factura_id}", response_model=schemas.FacturaResponse, tags=["Facturas"])
def actualizar_factura(factura_id: int, datos: schemas.FacturaUpdate, db: Session = Depends(get_db)):
    """Actualiza una factura."""
    factura = db.query(models.Factura).filter(models.Factura.id == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail=f"Factura {factura_id} no encontrada")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(factura, campo, valor)
    db.commit()
    db.refresh(factura)
    return factura


@app.delete("/facturas/{factura_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Facturas"])
def eliminar_factura(factura_id: int, db: Session = Depends(get_db)):
    """Elimina una factura y sus transacciones (cascade)."""
    factura = db.query(models.Factura).filter(models.Factura.id == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail=f"Factura {factura_id} no encontrada")
    db.delete(factura)
    db.commit()


# ══════════════════════════════════════════════════════════
#  TRANSACCIONES
# ══════════════════════════════════════════════════════════

@app.get("/transacciones", response_model=List[schemas.TransaccionResponse], tags=["Transacciones"])
def listar_transacciones(db: Session = Depends(get_db)):
    """Retorna todas las transacciones."""
    return db.query(models.Transaccion).all()


@app.get("/transacciones/{transaccion_id}", response_model=schemas.TransaccionResponse, tags=["Transacciones"])
def obtener_transaccion(transaccion_id: int, db: Session = Depends(get_db)):
    """Retorna una transacción por ID."""
    transaccion = db.query(models.Transaccion).filter(models.Transaccion.id == transaccion_id).first()
    if not transaccion:
        raise HTTPException(status_code=404, detail=f"Transacción {transaccion_id} no encontrada")
    return transaccion


@app.post("/transacciones", response_model=schemas.TransaccionResponse, status_code=status.HTTP_201_CREATED, tags=["Transacciones"])
def crear_transaccion(transaccion: schemas.TransaccionCreate, db: Session = Depends(get_db)):
    """Crea una nueva transacción dentro de una factura."""
    factura = db.query(models.Factura).filter(models.Factura.id == transaccion.factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail=f"Factura {transaccion.factura_id} no encontrada")
    db_transaccion = models.Transaccion(**transaccion.model_dump())
    db.add(db_transaccion)
    db.commit()
    db.refresh(db_transaccion)
    return db_transaccion


@app.put("/transacciones/{transaccion_id}", response_model=schemas.TransaccionResponse, tags=["Transacciones"])
def actualizar_transaccion(transaccion_id: int, datos: schemas.TransaccionUpdate, db: Session = Depends(get_db)):
    """Actualiza una transacción."""
    transaccion = db.query(models.Transaccion).filter(models.Transaccion.id == transaccion_id).first()
    if not transaccion:
        raise HTTPException(status_code=404, detail=f"Transacción {transaccion_id} no encontrada")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(transaccion, campo, valor)
    db.commit()
    db.refresh(transaccion)
    return transaccion


@app.delete("/transacciones/{transaccion_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Transacciones"])
def eliminar_transaccion(transaccion_id: int, db: Session = Depends(get_db)):
    """Elimina una transacción por ID."""
    transaccion = db.query(models.Transaccion).filter(models.Transaccion.id == transaccion_id).first()
    if not transaccion:
        raise HTTPException(status_code=404, detail=f"Transacción {transaccion_id} no encontrada")
    db.delete(transaccion)
    db.commit()
