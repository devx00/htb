class HTBException(Exception):
    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.message

class HTBFurtherAuthRequired(HTBException):
    def __init__(self):
        super().__init__("Two Factor Authentication is enabled and \
            must be completed before continuing")


class HTBRequestException(HTBException):
    def __init__(self, response):
        self.response = response
        if response is None:
            self.code = 0
            super().__init__("(0) - No Response Available")
            return
        self.code = response.status_code
        try:
            body = response.json()
            message = body["error"] if "error" in body \
                else body["message"]
        except Exception:
            message = "Could not parse error message."
        super().__init__(message)
