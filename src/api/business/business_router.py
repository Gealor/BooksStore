from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth.tools_auth import validate_user
from core.config import settings
from core.models import db_helper
from core.schemas.borrowed_books import (
    BorrowedBookRead,
    BorrowedBookUpdate,
)
from core.schemas.users import UserRead
from core.schemas.exceptions import (
    BookAlreadyReturnException,
    BookNotFoundException,
    IncreaseNumberOfCopiesException,
    MaxNumberBorrowedBooksException,
    ReduceNumberOfCopiesException,
    UserMissingBookException,
    ZeroCopiesException,
)
from services.borrowed_books_service import BorrowedBookService

router = APIRouter(
    prefix=settings.api.business.prefix,
    tags=["Business"],
)


@router.post("/lending-book")
def lending_book(
    book_id: int,
    session: Annotated[Session, Depends(db_helper.session_getter)],
    user: UserRead = Depends(validate_user),
) -> BorrowedBookRead:
    try:
        result = BorrowedBookService(session=session).lending_book(
            book_id=book_id, user_id=user.id
        )
    except BookNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    except ZeroCopiesException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not available"
        )
    except MaxNumberBorrowedBooksException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Maximum number of books borrowed : {settings.business.max_active_books}",
        )
    except ReduceNumberOfCopiesException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data",
        )

    return result


@router.patch("/return-book")
def return_book(
    borrowed_id: int,
    session: Annotated[Session, Depends(db_helper.session_getter)],
    user: UserRead = Depends(validate_user),
) -> BorrowedBookUpdate:
    try:
        result = BorrowedBookService(session=session).return_book(
            borrowed_id=borrowed_id, auth_user_id=user.id,
        )
    except BookNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    except UserMissingBookException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found in your library",
        )
    except BookAlreadyReturnException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Book already return",
        )
    except IncreaseNumberOfCopiesException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data",
        )
    return result
