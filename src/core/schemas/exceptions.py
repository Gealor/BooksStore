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
