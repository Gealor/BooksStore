class InvalidDataError(Exception):
    pass


class BookNotFoundException(Exception):
    pass


class ZeroCopiesException(Exception):
    pass


class MaxNumberBorrowedBooksException(Exception):
    pass


class ReduceNumberOfCopiesException(Exception):
    pass


class IncreaseNumberOfCopiesException(Exception):
    pass


class UserMissingBookException(Exception):
    pass


class BookAlreadyReturnException(Exception):
    pass


class BaseUserException(Exception):
    pass


class UserNotFoundException(BaseUserException):
    pass


class SelfDeleteException(BaseUserException):
    pass


class ListUsersNotFoundException(BaseUserException):
    pass


class BaseBooksException(Exception):
    pass


class ListBooksNotFoundException(BaseBooksException):
    pass


class EmailAlreadyExistsException(Exception):
    pass