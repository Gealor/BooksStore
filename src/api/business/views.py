from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.auth.tools.tools_auth import get_current_active_auth_user
from core.config import settings
from core.models import db_helper
from core.schemas.borrowed_books import BorrowedBookCreate, BorrowedBookRead, BorrowedBookUpdate
from core.schemas.users import UserRead
from .tools import utils
from crud import books as books_crud
from crud import borrowed_books as bb_crud

router = APIRouter(
    prefix = settings.api.business.prefix,
    tags = ['Business'],
)


@router.post('/lending-book')
def lending_book(
    book_id : int,
    session : Annotated[Session, Depends(db_helper.session_getter)],
    user : UserRead = Depends(get_current_active_auth_user),
) -> BorrowedBookCreate:
    book = books_crud.get_book_by_id(book_id, session)
    user_id = user.id
    try:
        utils.check_record_found(book)
        utils.check_number_copies(book)
        utils.check_number_of_active_books_user(user_id, settings.business.max_active_books, session)
    except HTTPException as e:
        raise e
    
    try:
        utils.reduce_number_of_copies(book, session)
    except HTTPException as e:
        raise e

    new_record = BorrowedBookCreate(book_id=book_id, reader_id=user_id)

    record = bb_crud.create_borrowed_book_record(new_record, session)

    return record


@router.patch('/return-book')
def return_book(
    borrowed_id : int,
    session : Annotated[Session, Depends(db_helper.session_getter)],
    user : UserRead = Depends(get_current_active_auth_user),
) -> BorrowedBookUpdate:
    record = bb_crud.get_borrowed_book_by_id(borrowed_id, session)
    book_id = record.book_id
    try:
        utils.check_record_found(record)
        utils.check_return_book(record)
    except HTTPException as e:
        raise e
    
    new_data = BorrowedBookUpdate()

    new_record = bb_crud.update_borrowed_book_record(record, new_data, session)
    
    book = books_crud.get_book_by_id(book_id, session)
    try:
        utils.increase_number_of_copies(book, session)
    except HTTPException as e:
        raise e
    
    return new_data








