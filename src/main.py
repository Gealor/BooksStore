from contextlib import asynccontextmanager, contextmanager
import logging
from fastapi import FastAPI
import uvicorn

from core.config import settings
from api import router as main_router
from core.logger import log, log_uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Start Books Store application...")
    log_uvicorn.info("Start Books Store application...")
    yield
    log.info("Shutdown Books Store application...")
    log_uvicorn.info("Shutdown Books Store application...")

main_app = FastAPI(lifespan=lifespan)

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
