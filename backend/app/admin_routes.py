from app.s4_admin.algorithm_config import router as algorithm_config_router
from app.s4_admin.bad_word import router as bad_word_router
from app.s4_admin.black_email import router as black_email_router
from app.s4_admin.black_ip import router as black_ip_router
from app.s4_admin.black_phone import router as black_phone_router
from app.s4_admin.lead_weights import router as lead_weights_router

def admin_routers(app):
    """
    Include all routers in the FastAPI app
    """
    # Include the algorithm configuration router
    app.include_router(algorithm_config_router)
    # Include the bad word router
    app.include_router(bad_word_router)
    # Include the black email router
    app.include_router(black_email_router)
    # Include the black IP router
    app.include_router(black_ip_router)
    # Include the black phone router
    app.include_router(black_phone_router)
    # Include the lead weights router
    app.include_router(lead_weights_router)

