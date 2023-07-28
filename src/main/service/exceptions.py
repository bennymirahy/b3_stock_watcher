class BrapiBaseException(Exception):
    pass


class BrapiConnectionError(BrapiBaseException):
    pass


class BrapiTooManyRequestsError(BrapiBaseException):
    pass


class BrapiTimeoutException(BrapiBaseException):
    pass


class BrapiException(BrapiBaseException):
    pass
