from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Transaccion(Base):
    __tablename__ = "transacciones"
    id = Column(Integer, primary_key=True, index=True)
    cantidad = Column(Integer, nullable=False)
    vr_unitario = Column(Float, nullable=False)
    descripcion = Column(String, nullable=False)
    factura_id = Column(Integer, ForeignKey("facturas.id"), nullable=False)
    factura = relationship("Factura", back_populates="transacciones")