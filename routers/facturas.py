from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Cliente, Factura, FacturaSimple, Transaccion, TransaccionSimple
from schemas import (
    FacturaCreate, FacturaCreateWithTransacciones, FacturaUpdate, FacturaResponse,
    FacturaSimpleCreate, FacturaSimpleUpdate, FacturaSimpleResponse,
    TransaccionSimpleCreate
)

router = APIRouter(prefix="/facturas", tags=["Facturas"])

# =============================================
# FACTURAS ORIGINALES (con cliente)
# =============================================

@router.get("/", response_model=List[FacturaResponse])
def listar_facturas(db: Session = Depends(get_db)):
    """Retorna todas las facturas."""
    return db.query(Factura).all()


@router.get("/{factura_id}", response_model=FacturaResponse)
def obtener_factura(factura_id: int, db: Session = Depends(get_db)):
    """Retorna una factura por ID, incluyendo sus transacciones."""
    factura = db.query(Factura).filter(Factura.id == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail=f"Factura {factura_id} no encontrada")
    return factura


@router.post("/", response_model=FacturaResponse, status_code=status.HTTP_201_CREATED)
def crear_factura(factura: FacturaCreateWithTransacciones, db: Session = Depends(get_db)):
    """
    Crea una nueva factura asociada a un cliente.
    Opcionalmente puede crear una o varias transacciones junto con la factura.
    """
    # Verificar que el cliente existe
    cliente = db.query(Cliente).filter(Cliente.id == factura.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail=f"Cliente {factura.cliente_id} no encontrado")
    
    # Crear la factura
    db_factura = Factura(fecha=factura.fecha, cliente_id=factura.cliente_id)
    db.add(db_factura)
    db.commit()
    db.refresh(db_factura)
    
    # Si se enviaron transacciones, crearlas
    if factura.transacciones:
        for transaccion_data in factura.transacciones:
            db_transaccion = Transaccion(
                cantidad=transaccion_data.cantidad,
                vr_unitario=transaccion_data.vr_unitario,
                descripcion=transaccion_data.descripcion,
                factura_id=db_factura.id
            )
            db.add(db_transaccion)
        db.commit()
        db.refresh(db_factura)
    
    return db_factura


@router.put("/{factura_id}", response_model=FacturaResponse)
def actualizar_factura(factura_id: int, datos: FacturaUpdate, db: Session = Depends(get_db)):
    """Actualiza una factura."""
    factura = db.query(Factura).filter(Factura.id == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail=f"Factura {factura_id} no encontrada")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(factura, campo, valor)
    db.commit()
    db.refresh(factura)
    return factura


@router.delete("/{factura_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_factura(factura_id: int, db: Session = Depends(get_db)):
    """Elimina una factura y sus transacciones (cascade)."""
    factura = db.query(Factura).filter(Factura.id == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail=f"Factura {factura_id} no encontrada")
    db.delete(factura)
    db.commit()


# =============================================
# FACTURAS SIMPLE (sin cliente)
# =============================================

@router.get("/simple", response_model=List[FacturaSimpleResponse], tags=["Facturas Simple"])
def listar_facturas_simple(db: Session = Depends(get_db)):
    """Retorna todas las facturas simples."""
    return db.query(FacturaSimple).all()


@router.get("/simple/{factura_id}", response_model=FacturaSimpleResponse, tags=["Facturas Simple"])
def obtener_factura_simple(factura_id: int, db: Session = Depends(get_db)):
    """Retorna una factura simple por ID."""
    factura = db.query(FacturaSimple).filter(FacturaSimple.id == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail=f"Factura simple {factura_id} no encontrada")
    return factura


@router.post("/simple", response_model=FacturaSimpleResponse, status_code=status.HTTP_201_CREATED, tags=["Facturas Simple"])
def crear_factura_simple(factura: FacturaSimpleCreate, db: Session = Depends(get_db)):
    """Crea una nueva factura simple."""
    db_factura = FacturaSimple(**factura.model_dump())
    db.add(db_factura)
    db.commit()
    db.refresh(db_factura)
    return db_factura


@router.put("/simple/{factura_id}", response_model=FacturaSimpleResponse, tags=["Facturas Simple"])
def actualizar_factura_simple(factura_id: int, datos: FacturaSimpleUpdate, db: Session = Depends(get_db)):
    """Actualiza una factura simple."""
    factura = db.query(FacturaSimple).filter(FacturaSimple.id == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail=f"Factura simple {factura_id} no encontrada")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(factura, campo, valor)
    db.commit()
    db.refresh(factura)
    return factura


@router.delete("/simple/{factura_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Facturas Simple"])
def eliminar_factura_simple(factura_id: int, db: Session = Depends(get_db)):
    """Elimina una factura simple y sus transacciones."""
    factura = db.query(FacturaSimple).filter(FacturaSimple.id == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail=f"Factura simple {factura_id} no encontrada")
    db.delete(factura)
    db.commit()