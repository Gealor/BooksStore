from contextlib import asynccontextmanager, contextmanager
import logging
from fastapi import FastAPI
import uvicorn

from core.config import settings
from api import router as main_router


log = logging.getLogger(__name__)
log_uvicorn = logging.getLogger("uvicorn.error")
logging.basicConfig(
    level=settings.log.level,
    format=settings.log.LOG_DEFAULT_FORMAT,
    datefmt=settings.log.datefmt,
)

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
