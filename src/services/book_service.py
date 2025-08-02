from typing import Optional
from sqlalchemy import Sequence
from sqlalchemy.orm import Session

from core.schemas.books import BookCreate, BookDelete, BookRead, BookUpdate
from repositories.book_repository import BookRepository
from core.models.books import Book
from core.schemas.exceptions import BookNotFoundException, IncreaseNumberOfCopiesException, InvalidDataError, ReduceNumberOfCopiesException, ZeroCopiesException


class BookService:
    @staticmethod
    def get_all_books(session: Session) -> list[BookRead]:
        books = BookRepository(session=session).get_all_books()
        return books

    @staticmethod
    def create_book(book_create: BookCreate, session: Session) -> Book:
        book = BookRepository(session=session).create_book(book_create)
        return book

    @staticmethod
    def update_book_by_id(
        book_id: int, book_update: BookUpdate, session: Session
    ) -> BookUpdate:
        repo = BookRepository(session=session)
        found_book = repo.get_book_by_id(book_id)
        if found_book is None:
            raise BookNotFoundException

        values_dict = book_update.model_dump(exclude_unset=True)
        repo.update_book_data(found_book, values_dict)

        return book_update

    @staticmethod
    def delete_book_by_id(book_id: int, session: Session) -> BookDelete:
        deleted_id = BookRepository(session=session).delete_book_by_id(book_id)
        if deleted_id is None:
            raise BookNotFoundException
        return {
            "deleted": deleted_id,
        }
    
    @staticmethod
    def get_book_by_id(book_id: int, session: Session) -> Book | None:
        book = BookRepository(session=session).get_book_by_id(book_id=book_id)
        return book
    
    @staticmethod
    def reduce_number_of_copies(book_id: int, session: Session) -> None:
        repo = BookRepository(session=session)
        book = repo.get_book_by_id(book_id=book_id)

        if book is None:
            raise BookNotFoundException
        
        if book.number_copies==0:
            raise ZeroCopiesException
        
        new_data = {"number_copies": book.number_copies - 1}
        try:
           repo.update_book_data(book=book, new_data=new_data)
        except InvalidDataError:
            raise ReduceNumberOfCopiesException
        
    @staticmethod
    def increase_number_of_copies(book_id: int, session: Session) -> None:
        repo = BookRepository(session=session)
        book = repo.get_book_by_id(book_id=book_id)

        if book is None:
            raise BookNotFoundException
        
        new_data = {"number_copies": book.number_copies + 1}
        try:
           repo.update_book_data(book=book, new_data=new_data)
        except InvalidDataError:
            raise IncreaseNumberOfCopiesException
        