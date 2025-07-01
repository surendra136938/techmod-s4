from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.services.administration import Administration

router = APIRouter(prefix="/s4_admin/bad_word", tags=["bad_word"])
service = Administration()

@router.post("/add/")
async def add_bad_word(request: Request) -> JSONResponse:
    """
    Adds new bad word to spam filtering dictionary.
    """     
    post_body = await request.body()
    return service.add_bad_word(post_body)

@router.delete("/delete/")
async def delete_bad_word(request: Request) -> JSONResponse:
    """
    Deletes bad words from spam filtering dictionary by IDs.
    """
    post_body = await request.body()
    return service.delete_bad_word(post_body)

@router.get("/list/")
async def get_bad_words_list() -> JSONResponse:
    """
    Retrieves list of all bad words used for spam filtering.
    """
    return service.get_bad_words_list()
