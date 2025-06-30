from fastapi import APIRouter, Request
from app.services.administration import Administration

router = APIRouter(prefix="/s4_admin/black_phone", tags=["black_phone"])
service = Administration()

@router.post("/add/")
async def add_black_phone(request: Request):     
    post_body = await request.body()
    return service.add_black_phone(post_body)

@router.delete("/delete/")
async def delete_black_phone(request: Request):
    post_body = await request.body()
    return service.delete_black_phone(post_body)

@router.get("/list/")
async def get_black_phone_list():
    return service.get_black_phone_list()

