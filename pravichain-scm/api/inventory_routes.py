"""API routes for inventory optimization."""

from fastapi import APIRouter
from agents.inventory import main as run_inventory

router = APIRouter()


@router.post('/inventory/optimize')
def inventory_optimize_endpoint():
    run_inventory()
    return {"status": "inventory optimized"}
