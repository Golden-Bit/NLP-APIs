from fastapi import APIRouter

router = APIRouter()

@router.get("/items", tags=["script1"])
async def get_items():
    return {"message": "Items from script1"}

@router.post("/items", tags=["script1"])
async def create_item(item: dict):
    return {"message": "Item created in script1", "item": item}
