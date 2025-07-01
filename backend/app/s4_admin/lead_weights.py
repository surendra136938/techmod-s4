from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.services.administration import Administration

router = APIRouter(prefix="/s4_admin/lead_weights", tags=["lead_weights"])
service = Administration()

@router.put("/update/")
async def update_weight(request: Request) -> JSONResponse:
    """
    Updates weight value for specific lead type in spam detection.
    """     
    post_body = await request.body()
    return service.update_weight(post_body)

@router.get("/list/")
async def get_lead_weights() -> JSONResponse:
    """
    Retrieves all lead type weights used in spam detection algorithms.
    """
    return service.get_lead_weights()
