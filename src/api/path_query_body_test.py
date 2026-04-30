from fastapi import APIRouter

from core.schemas.users import UserBase

router = APIRouter()


@router.post("/something/{id}")
async def something(
    id: int, # параметр пути
    name: str, # параметр запроса 
    body: UserBase, # тело запроса
):
    return {
        "id": id,
        "name": name,
        "body": body,
    }

@router.get("/something/{id}")
async def something(
    id: int, # параметр пути
    name: str, # параметр запроса 
    body: UserBase, # тело запроса, но GET метод НЕ ИМЕЕТ тело запроса
):
    return {
        "id": id,
        "name": name,
        "body": body,
    }