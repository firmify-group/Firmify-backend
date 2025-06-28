import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from src.api.controller.api_router import api_router
from config import settings as cf
from src.api.controller.router.manager import router as manager_router
from src.api.controller.router.objection import router as objection_router
from src.api.controller.router.office import router as office_router

def create_app() -> FastAPI:
    app = FastAPI(
        title =  cf.PROJECT_NAME,
    
    )

    if cf.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in cf.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Include the routers
    app.include_router(api_router)
    app.include_router(manager_router)
    app.include_router(objection_router)
    app.include_router(office_router)



    
    return app

app = create_app()

if __name__ == "__main__":
    host = "localhost"
    port = 8000
    uvicorn.run(app, host=host, port=port)