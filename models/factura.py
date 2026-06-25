from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Factura(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="facturas")
    transacciones = relationship("Transaccion", back_populates="factura", cascade="all, delete-orphan")


class FacturaSimple(Base):
    __tablename__ = "facturas_simple"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    
    transacciones_simple = relationship(
        "TransaccionSimple", 
        back_populates="factura_simple", 
        cascade="all, delete-orphan"
    )