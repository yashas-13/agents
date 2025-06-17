from fastapi import FastAPI
from .forecast_routes import router as forecast_router
from .inventory_routes import router as inventory_router
from .chat_routes import router as chat_router

app = FastAPI()

app.include_router(forecast_router)
app.include_router(inventory_router)
app.include_router(chat_router)

