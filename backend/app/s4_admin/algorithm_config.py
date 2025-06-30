from fastapi import APIRouter, Request
from app.services.administration import Administration

router = APIRouter(prefix="/s4_admin/algorithm_config", tags=["algorithm_config"])
service = Administration()

@router.post("/add/")
async def add_algorithm_config(request: Request):     
    post_body = await request.body()
    return service.add_algorithm_config(post_body)

@router.delete("/delete/")
async def delete_algorithm_config(request: Request):
    post_body = await request.body()
    return service.delete_algorithm_config(post_body)

@router.post("/detail/")
async def get_single_algorithm_config(request: Request):
    post_body = await request.body()
    return service.get_single_algorithm_config(post_body)

@router.get("/list/")
async def get_algorithm_config():
    return service.get_algorithm_config()

@router.put("/update/")
async def update_algorithm_config(request: Request):
    post_body = await request.body()
    return service.update_algorithm_config(post_body)
