from fastapi import APIRouter, Request
from app.services.administration import Administration

router = APIRouter(prefix="/s4_admin/black_ip", tags=["black_ip"])
service = Administration()

@router.post("/add/")
async def add_black_ip(request: Request):     
    post_body = await request.body()
    return service.add_black_ip(post_body)

@router.delete("/delete/")
async def delete_black_ip(request: Request):
    post_body = await request.body()
    return service.delete_black_ip(post_body)

@router.get("/list/")
async def get_blacklist_ip():
    return service.get_blacklist_ip()

