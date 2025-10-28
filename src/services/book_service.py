from sqlalchemy.orm import Session

from core.schemas.books import BookCreate, BookDelete, BookRead, BookUpdate
from repositories.book_repository import BookRepository
from core.models.books import Book
from core.schemas.exceptions import (
    BookNotFoundException,
    IncreaseNumberOfCopiesException,
    InvalidDataError,
    ReduceNumberOfCopiesException,
    ZeroCopiesException,
)


class BookService:
    def __init__(self, session: Session):
        self.session = session
    
    def get_all_books(self) -> list[BookRead]:
        books = BookRepository(session=self.session).get_all_books()
        return books

    
    def create_book(self, book_create: BookCreate) -> Book:
        book = BookRepository(session=self.session).create_book(book_create)
        return book

    
    def update_book_by_id(
        self, book_id: int, book_update: BookUpdate,
    ) -> BookUpdate:
        repo = BookRepository(session=self.session)
        found_book = repo.get_book_by_id(book_id)
        if found_book is None:
            raise BookNotFoundException

        values_dict = book_update.model_dump(exclude_unset=True)
        repo.update_book_data(found_book.id, values_dict)

        return book_update

    
    def delete_book_by_id(self, book_id: int) -> BookDelete:
        deleted_id = BookRepository(session=self.session).delete_book_by_id(book_id)
        if deleted_id is None:
            raise BookNotFoundException
        return {
            "deleted": deleted_id,
        }

    
    def get_book_by_id(self, book_id: int) -> Book | None:
        book = BookRepository(session=self.session).get_book_by_id(book_id=book_id)
        return book

    
    def reduce_number_of_copies(self, book_id: int) -> None:
        repo = BookRepository(session=self.session)
        book = repo.get_book_by_id(book_id=book_id)

        if book is None:
            raise BookNotFoundException

        if book.number_copies == 0:
            raise ZeroCopiesException

        new_data = {"number_copies": book.number_copies - 1}
        try:
            repo.update_book_data(book_id=book.id, new_data=new_data)
        except InvalidDataError:
            raise ReduceNumberOfCopiesException

    
    def increase_number_of_copies(self, book_id: int) -> None:
        repo = BookRepository(session=self.session)
        book = repo.get_book_by_id(book_id=book_id)

        if book is None:
            raise BookNotFoundException

        new_data = {"number_copies": book.number_copies + 1}
        try:
            repo.update_book_data(book_id=book.id, new_data=new_data)
        except InvalidDataError:
            raise IncreaseNumberOfCopiesException
