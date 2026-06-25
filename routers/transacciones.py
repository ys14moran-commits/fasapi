from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Factura, FacturaSimple, Transaccion, TransaccionSimple
from schemas import (
    TransaccionBase, TransaccionCreate, TransaccionUpdate, TransaccionResponse,
    TransaccionSimpleCreate, TransaccionSimpleUpdate, TransaccionSimpleResponse
)

router = APIRouter(prefix="/transacciones", tags=["Transacciones"])

# =============================================
# TRANSACCIONES ORIGINALES
# =============================================

@router.get("/", response_model=List[TransaccionResponse])
def listar_transacciones(db: Session = Depends(get_db)):
    """Retorna todas las transacciones."""
    return db.query(Transaccion).all()


@router.get("/{transaccion_id}", response_model=TransaccionResponse)
def obtener_transaccion(transaccion_id: int, db: Session = Depends(get_db)):
    """Retorna una transacción por ID."""
    transaccion = db.query(Transaccion).filter(Transaccion.id == transaccion_id).first()
    if not transaccion:
        raise HTTPException(status_code=404, detail=f"Transacción {transaccion_id} no encontrada")
    return transaccion


@router.post("/", response_model=TransaccionResponse, status_code=status.HTTP_201_CREATED)
def crear_transaccion(transaccion: TransaccionCreate, db: Session = Depends(get_db)):
    """Crea una nueva transacción dentro de una factura."""
    factura = db.query(Factura).filter(Factura.id == transaccion.factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail=f"Factura {transaccion.factura_id} no encontrada")
    db_transaccion = Transaccion(**transaccion.model_dump())
    db.add(db_transaccion)
    db.commit()
    db.refresh(db_transaccion)
    return db_transaccion


@router.post("/factura/{factura_id}", response_model=TransaccionResponse, status_code=status.HTTP_201_CREATED)
def crear_transaccion_por_factura(
    factura_id: int,
    transaccion: TransaccionBase,
    db: Session = Depends(get_db)
):
    """
    Crea una nueva transacción para una factura existente.
    Verifica que la factura existe antes de crear la transacción.
    """
    factura = db.query(Factura).filter(Factura.id == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail=f"Factura {factura_id} no encontrada")
    
    db_transaccion = Transaccion(
        cantidad=transaccion.cantidad,
        vr_unitario=transaccion.vr_unitario,
        descripcion=transaccion.descripcion,
        factura_id=factura_id
    )
    db.add(db_transaccion)
    db.commit()
    db.refresh(db_transaccion)
    return db_transaccion


@router.post("/factura/{factura_id}/cliente/{cliente_id}", response_model=TransaccionResponse, status_code=status.HTTP_201_CREATED)
def crear_transaccion_con_validacion(
    factura_id: int,
    cliente_id: int,
    transaccion: TransaccionBase,
    db: Session = Depends(get_db)
):
    """
    Crea una nueva transacción verificando que tanto la factura como el cliente existan,
    y que la factura pertenezca al cliente.
    """
    from models import Cliente  # Import local para evitar circular
    
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail=f"Cliente {cliente_id} no encontrado")
    
    factura = db.query(Factura).filter(
        Factura.id == factura_id,
        Factura.cliente_id == cliente_id
    ).first()
    if not factura:
        raise HTTPException(
            status_code=404, 
            detail=f"Factura {factura_id} no encontrada para el cliente {cliente_id}"
        )
    
    db_transaccion = Transaccion(
        cantidad=transaccion.cantidad,
        vr_unitario=transaccion.vr_unitario,
        descripcion=transaccion.descripcion,
        factura_id=factura_id
    )
    db.add(db_transaccion)
    db.commit()
    db.refresh(db_transaccion)
    return db_transaccion


@router.put("/{transaccion_id}", response_model=TransaccionResponse)
def actualizar_transaccion(transaccion_id: int, datos: TransaccionUpdate, db: Session = Depends(get_db)):
    """Actualiza una transacción."""
    transaccion = db.query(Transaccion).filter(Transaccion.id == transaccion_id).first()
    if not transaccion:
        raise HTTPException(status_code=404, detail=f"Transacción {transaccion_id} no encontrada")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(transaccion, campo, valor)
    db.commit()
    db.refresh(transaccion)
    return transaccion


@router.delete("/{transaccion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_transaccion(transaccion_id: int, db: Session = Depends(get_db)):
    """Elimina una transacción por ID."""
    transaccion = db.query(Transaccion).filter(Transaccion.id == transaccion_id).first()
    if not transaccion:
        raise HTTPException(status_code=404, detail=f"Transacción {transaccion_id} no encontrada")
    db.delete(transaccion)
    db.commit()


# =============================================
# TRANSACCIONES SIMPLE
# =============================================

@router.get("/simple", response_model=List[TransaccionSimpleResponse], tags=["Transacciones Simple"])
def listar_transacciones_simple(db: Session = Depends(get_db)):
    """Retorna todas las transacciones simples."""
    return db.query(TransaccionSimple).all()


@router.get("/simple/{transaccion_id}", response_model=TransaccionSimpleResponse, tags=["Transacciones Simple"])
def obtener_transaccion_simple(transaccion_id: int, db: Session = Depends(get_db)):
    """Retorna una transacción simple por ID."""
    transaccion = db.query(TransaccionSimple).filter(TransaccionSimple.id == transaccion_id).first()
    if not transaccion:
        raise HTTPException(status_code=404, detail=f"Transacción simple {transaccion_id} no encontrada")
    return transaccion


@router.post("/simple", response_model=TransaccionSimpleResponse, status_code=status.HTTP_201_CREATED, tags=["Transacciones Simple"])
def crear_transaccion_simple(transaccion: TransaccionSimpleCreate, db: Session = Depends(get_db)):
    """Crea una nueva transacción simple asociada a una factura simple."""
    factura = db.query(FacturaSimple).filter(FacturaSimple.id == transaccion.factura_simple_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail=f"Factura simple {transaccion.factura_simple_id} no encontrada")
    
    db_transaccion = TransaccionSimple(**transaccion.model_dump())
    db.add(db_transaccion)
    db.commit()
    db.refresh(db_transaccion)
    return db_transaccion


@router.put("/simple/{transaccion_id}", response_model=TransaccionSimpleResponse, tags=["Transacciones Simple"])
def actualizar_transaccion_simple(transaccion_id: int, datos: TransaccionSimpleUpdate, db: Session = Depends(get_db)):
    """Actualiza una transacción simple."""
    transaccion = db.query(TransaccionSimple).filter(TransaccionSimple.id == transaccion_id).first()
    if not transaccion:
        raise HTTPException(status_code=404, detail=f"Transacción simple {transaccion_id} no encontrada")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(transaccion, campo, valor)
    db.commit()
    db.refresh(transaccion)
    return transaccion


@router.delete("/simple/{transaccion_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Transacciones Simple"])
def eliminar_transaccion_simple(transaccion_id: int, db: Session = Depends(get_db)):
    """Elimina una transacción simple por ID."""
    transaccion = db.query(TransaccionSimple).filter(TransaccionSimple.id == transaccion_id).first()
    if not transaccion:
        raise HTTPException(status_code=404, detail=f"Transacción simple {transaccion_id} no encontrada")
    db.delete(transaccion)
    db.commit()