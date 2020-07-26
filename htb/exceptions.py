class HTBException(Exception):

    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return f"[{self.__name__}]: {self.message}"


class FurtherAuthRequired(HTBException):
    pass


class HTBRequestException(HTBException):

    def __init__(self, message, code):
        super().__init__(f"({code}) - {message}")


class UnauthorizedException(HTBRequestException):

    def __init__(self, message="Unauthenticated"):
        super().__init__(message, 401)


statuscodes = {
    401: UnauthorizedException
}


def httpcode_exception(code):
    if code in statuscodes:
        exception = statuscodes[code]
        return exception()
