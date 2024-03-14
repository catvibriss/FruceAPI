class UnauthorizedError(Exception):
    pass

class NoPermissionError(Exception):
    pass

class InvalidRequestError(Exception):
    pass

class MusicNotFoundError(Exception):
    pass

class AlreadyHaveFreeServer(Exception):
    pass

class NotMoneyOnBalance(Exception):
    pass