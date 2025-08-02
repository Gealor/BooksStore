from sqlalchemy.orm import Session

from core.models.books import Book
from core.models.borrowed_books import BorrowedBook
from core.schemas.borrowed_books import BorrowedBookUpdate
from core.schemas.exceptions import BookAlreadyReturnException, BookNotFoundException, MaxNumberBorrowedBooksException, UserMissingBookException, ZeroCopiesException
from repositories.book_repository import BookRepository
from repositories.borrowed_book_repository import BorrowedBookRepository
from services.book_service import BookService
from core.config import settings

class BorrowedBookService:

    @staticmethod
    def lending_book(book_id: int, user_id: int, session: Session) -> BorrowedBook:
        repo = BorrowedBookRepository(session=session)
        borrowed_books_user = repo.get_active_borrowed_books_by_user_id(user_id=user_id)
        if len(borrowed_books_user) == settings.business.max_active_books:
            raise MaxNumberBorrowedBooksException
        record = repo.create_borrowed_book_record(book_id=book_id, reader_id=user_id)
        BookService.reduce_number_of_copies(book_id=book_id, session=session)
    
        return record
    

    @staticmethod
    def return_book(borrowed_id: int, auth_user_id: int, session: Session) -> BorrowedBookUpdate:
        repo = BorrowedBookRepository(session=session)
        borrowed_book = repo.get_borrowed_book_by_id(borrowed_id)

        if borrowed_book is None:
            raise BookNotFoundException
        
        if borrowed_book.reader_id!=auth_user_id:
            raise UserMissingBookException
        
        if borrowed_book.return_date is not None:
            raise BookAlreadyReturnException
        
        new_data = BorrowedBookUpdate()

        repo.update_borrowed_book_record(
            record=borrowed_book,
            record_update=new_data,
        )

        BookService.increase_number_of_copies(book_id=borrowed_book.book_id, session=session)

        return new_data



        
        

