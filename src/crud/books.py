from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import selectinload, Session

from auth import tools as auth_tools
from core.models import Book
from core.schemas.books import BookCreate, BookRead



def get_all_books(
    session : Session,
) -> Sequence[BookRead]:
    stmt = select(Book).order_by(Book.id)

    result = session.scalars(stmt)
    return result.all()

def get_book_by_id(
    book_id : int,
    session : Session,
) -> BookRead | None:
    stmt = select(Book).where(Book.id == book_id)
    result = session.scalar(stmt)

    return result

def get_books_by_name(
        book_name : str, 
        session : Session,
) -> Sequence[BookRead] | BookRead | None:
    stmt = select(Book).where(Book.title == book_name)
    result = session.scalars(stmt)

    return result.all() if len(result)>1 else result.first()

def get_books_by_author(
    author : str,
    session : Session,
) -> Sequence[BookRead]:
    stmt = select(Book).where(Book.author == author)
    result = session.scalars(stmt)

    return result.all()

def create_book(
    user_create : BookCreate,
    session : Session,
) -> BookRead:
    
    book = Book(**user_create.model_dump())
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

def delete_book_by_id(
    book_id : int,
    session : Session,
) -> int | None:
    stmt = select(Book).options(selectinload(Book.borrowed_books)).where(Book.id == book_id)
    result = session.execute(stmt)
    user = result.scalar_one_or_none()
    if user:
        session.delete(user)
        session.commit()
    return user.id if user else None
    

def update_book_data(
    book : Book,
    new_data : dict,
    session : Session,
) -> None:
    for key, value in new_data.items():
        setattr(book, key, value)
        
    session.commit()

