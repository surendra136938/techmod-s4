from fastapi import APIRouter, Request
from app.services.administration import Administration

router = APIRouter(prefix="/s4_admin/black_email", tags=["black_email"])
service = Administration()

@router.post("/add/")
async def add_algorithm_config(request: Request):     
    post_body = await request.body()
    return service.add_black_email(post_body)

@router.delete("/delete/")
async def delete_algorithm_config(request: Request):
    post_body = await request.body()
    return service.delete_black_email(post_body)

@router.get("/list/")
async def get_algorithm_config():
    return service.get_black_email_list()

