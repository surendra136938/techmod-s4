from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.services.administration import Administration

router = APIRouter(prefix="/s4_admin/algorithm_config", tags=["algorithm_config"])
service = Administration()

@router.post("/add/")
async def add_algorithm_config(request: Request) -> JSONResponse:
    """
    Creates new algorithm configuration for spam detection rules.
    """     
    post_body = await request.body()
    return service.add_algorithm_config(post_body)

@router.delete("/delete/")
async def delete_algorithm_config(request: Request) -> JSONResponse:
    """
    Deletes algorithm configuration by ID.
    """
    post_body = await request.body()
    return service.delete_algorithm_config(post_body)

@router.post("/detail/")
async def get_single_algorithm_config(request: Request) -> JSONResponse:
    """
    Retrieves specific algorithm configuration details by ID.
    """
    post_body = await request.body()
    return service.get_single_algorithm_config(post_body)

@router.get("/list/")
async def get_algorithm_config() -> JSONResponse:
    """
    Retrieves all algorithm configurations for spam detection.
    """
    return service.get_algorithm_config()

@router.put("/update/")
async def update_algorithm_config(request: Request) -> JSONResponse:
    """
    Updates existing algorithm configuration with new parameters.
    """
    post_body = await request.body()
    return service.update_algorithm_config(post_body)
