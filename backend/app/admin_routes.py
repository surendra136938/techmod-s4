from fastapi import FastAPI
from app.s4_admin.algorithm_config import router as algorithm_config_router
from app.s4_admin.bad_word import router as bad_word_router
from app.s4_admin.lead_weights import router as lead_weights_router

def admin_routers(app: FastAPI) -> None:
    """
    Registers all admin routers with the FastAPI application.
    """
    # Include the algorithm configuration router
    app.include_router(algorithm_config_router)
    # Include the bad word router
    app.include_router(bad_word_router)
    # Include the lead weights router
    app.include_router(lead_weights_router)

