from .clientes import router as clientes_router
from .facturas import router as facturas_router
from .transacciones import router as transacciones_router

__all__ = ['clientes_router', 'facturas_router', 'transacciones_router']