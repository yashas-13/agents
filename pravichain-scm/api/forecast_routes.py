"""API routes for demand forecast."""

from fastapi import APIRouter
from agents.forecast import main as run_forecast

router = APIRouter()


@router.post('/forecast')
def forecast_endpoint():
    run_forecast()
    return {"status": "forecast completed"}
