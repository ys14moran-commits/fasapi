from fastapi import FastAPI, status
from database import engine, Base
from routers import clientes_router, facturas_router, transacciones_router

# Crear tablas al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Facturación",
    description="Gestión de Clientes, Facturas y Transacciones",
    version="1.0.0",
)

# Incluir los routers
app.include_router(clientes_router)
app.include_router(facturas_router)
app.include_router(transacciones_router)

@app.get("/")
def root():
    return {"message": "API de Facturación funcionando correctamente"}