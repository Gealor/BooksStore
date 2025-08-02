from fastapi import FastAPI
import uvicorn

from core.config import settings
from api import router as main_router

main_app = FastAPI()

main_app.include_router(
    main_router,
)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
