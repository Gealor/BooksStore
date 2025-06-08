from fastapi import Depends, FastAPI, Request, Response
import uvicorn

from core.config import settings

main_app = FastAPI()

if __name__=="__main__":
    uvicorn.run(
        "main:main_app",
        host = settings.run.host,
        port = settings.run.port,
        reload = True,
    )