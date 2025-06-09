from fastapi import APIRouter

from core.config import settings
from .auth.jwt_auth import router as auth_router
from .users.views import router as user_router
from .books.views import router as book_router

router = APIRouter(
    prefix = settings.api.prefix,
)

router.include_router(
    auth_router,
)

router.include_router(
    user_router,
)

router.include_router(
    book_router,
)