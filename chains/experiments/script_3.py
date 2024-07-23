from fastapi import APIRouter

router = APIRouter()

@router.get("/orders", tags=["script3"])
async def get_orders():
    return {"message": "Orders from script3"}

@router.post("/orders", tags=["script3"])
async def create_order(order: dict):
    return {"message": "Order created in script3", "order": order}
