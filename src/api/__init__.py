from fastapi import APIRouter

from core.config import settings
from core.schemas.users import UserBase
from .auth.auth_router import router as auth_router
from .users.user_router import router as user_router
from .books.book_router import router as book_router
from .business.business_router import router as business_router

from .path_query_body_test import router as random_shit_router

router = APIRouter(
    prefix=settings.api.prefix,
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

router.include_router(
    business_router,
)


router.include_router(
    random_shit_router,
)
