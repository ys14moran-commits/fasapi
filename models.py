from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    telefono = Column(String, nullable=True)

    facturas = relationship("Factura", back_populates="cliente")


class Factura(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="facturas")
    transacciones = relationship("Transaccion", back_populates="factura", cascade="all, delete-orphan")


class Transaccion(Base):
    __tablename__ = "transacciones"

    id = Column(Integer, primary_key=True, index=True)
    cantidad = Column(Integer, nullable=False)
    vr_unitario = Column(Float, nullable=False)
    descripcion = Column(String, nullable=False)
    factura_id = Column(Integer, ForeignKey("facturas.id"), nullable=False)

    factura = relationship("Factura", back_populates="transacciones")
