from fastapi import APIRouter

router = APIRouter()

@router.get("/users", tags=["script2"])
async def get_users():
    return {"message": "Users from script2"}

@router.post("/users", tags=["script2"])
async def create_user(user: dict):
    return {"message": "User created in script2", "user": user}
